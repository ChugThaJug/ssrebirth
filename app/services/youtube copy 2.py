# Update imports at the top of the file
from io import BytesIO
import os
import json
import cv2
from datetime import datetime
import logging
from typing import Dict, List, Optional, Any, Tuple
import asyncio
from youtube_transcript_api import YouTubeTranscriptApi
from fastapi import HTTPException
import yt_dlp

from app.core.settings import settings
from app.core.enums import ProcessingMode, ChapterSource
from app.services.openai import OpenAIService
from app.services.transcription import TranscriptionService
from app.models.youtube import YouTubeResult, ProcessingStats, Chapter
from app.services.chapters import ChaptersService

logger = logging.getLogger(__name__)

class YouTubeService:
    def __init__(self):
        self.openai_service = OpenAIService()
        self.transcription_service = TranscriptionService()
        self.chapters_service = ChaptersService()
        self._ensure_directories()

    def _ensure_directories(self):
        """Ensure all required directories exist."""
        dirs = [
            settings.CACHE_DIR,
            settings.DOWNLOAD_DIR,
            settings.SCREENSHOTS_DIR,
            settings.OUTPUT_DIR
        ]
        for directory in dirs:
            os.makedirs(directory, exist_ok=True)

    async def get_transcript(self, video_id: str, languages: List[str] = ["en"]) -> List[Dict[str, Any]]:
        """Fetch transcript from YouTube video."""
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
            return [{'start': s['start'], 'text': s['text']} for s in transcript]
        except Exception as e:
            logger.warning(f"Failed to get YouTube transcript, falling back to Replicate: {str(e)}")
            try:
                transcript = await self.transcription_service.transcribe_video(video_id)
                return transcript
            except Exception as e2:
                logger.error(f"Both transcript methods failed: {str(e2)}")
                raise HTTPException(
                    status_code=500,
                    detail="Failed to get transcript from both YouTube and Replicate"
                )

    async def get_cached_result(self, video_id: str, cache_type: str) -> Optional[Dict]:
        """Get cached processing result."""
        try:
            cache_file = os.path.join(settings.CACHE_DIR, f"{video_id}_{cache_type}.json")
            if not os.path.exists(cache_file):
                return None
                
            with open(cache_file, 'r') as f:
                data = json.load(f)
                
            # Validate cache data structure
            if cache_type == "final":
                required_keys = ["video_id", "chapters", "stats"]
                if not all(key in data for key in required_keys):
                    logger.warning(f"Invalid cache data structure in {cache_file}")
                    return None
                    
            return data
                
        except Exception as e:
            logger.error(f"Error reading cache file {cache_file}: {str(e)}")
            return None

    async def save_cache(self, video_id: str, cache_type: str, data: Dict):
        """Save processing result to cache."""
        try:
            cache_file = os.path.join(settings.CACHE_DIR, f"{video_id}_{cache_type}.json")
            
            # Convert Pydantic models to dict
            if hasattr(data, 'model_dump'):
                data = data.model_dump()
            elif hasattr(data, 'dict'):
                data = data.dict()
                
            # Ensure video_id is included in final results
            if cache_type == "final" and "video_id" not in data:
                data["video_id"] = video_id
                
            with open(cache_file, 'w') as f:
                json.dump(data, f, indent=4)
                
            logger.debug(f"Saved cache file: {cache_file}")
                
        except Exception as e:
            logger.error(f"Error saving cache file for {video_id}: {str(e)}")
            raise

    async def process_simple(self, video_id: str) -> Tuple[List[Dict], int, int, float]:
        """Process transcript in simple mode (no chunking)."""
        transcript = await self.get_transcript(video_id)
        
        # Combine all text into one string
        full_text = " ".join([t["text"] for t in transcript])
        
        # Process with OpenAI in one go
        response = await self.openai_service.process_chunk(full_text)
        
        # Create single paragraph with full content
        processed_text = [{
            "paragraph_number": 0,
            "paragraph_text": response.choices[0].message.content,
            "start_time": float(transcript[0]["start"])  # Ensure float type
        }]
        
        # Get token usage from response
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        price = self.openai_service.calculate_price(input_tokens, output_tokens)
        
        return processed_text, input_tokens, output_tokens, price

    async def process_detailed(self, video_id: str) -> Tuple[List[Dict], int, int, float]:
        """Process transcript in detailed mode (with chunking)."""
        transcript = await self.get_transcript(video_id)
        
        # Process with chunking
        processed_chunks, input_tokens, output_tokens, price = await self.openai_service.transcript_to_paragraphs(transcript)
        
        # Ensure each chunk has a start_time
        for i, chunk in enumerate(processed_chunks):
            # If the chunk doesn't have a start_time, assign from transcript
            if "start_time" not in chunk:
                # Find the corresponding transcript segment
                chunk_start_idx = i * settings.CHUNK_SIZE
                transcript_idx = min(chunk_start_idx, len(transcript) - 1)
                chunk["start_time"] = float(transcript[transcript_idx]["start"])
        
        return processed_chunks, input_tokens, output_tokens, price

    async def process_detailed_with_screenshots(
        self,
        video_id: str,
        screenshot_interval: int = 60
    ) -> Tuple[List[Dict], List[str], int, int, float]:
        """Process transcript in detailed mode with screenshots."""
        # Get transcript and process text
        processed_text, input_tokens, output_tokens, price = await self.process_detailed(video_id)
        
        # Verify all paragraphs have start_time
        for para in processed_text:
            if "start_time" not in para:
                logger.error("Missing start_time in paragraph")
                raise ValueError("Paragraph processing failed: missing timestamp data")
        
        # Determine screenshot timestamps
        timestamps = []
        for para in processed_text:
            current_time = float(para["start_time"])
            if len(timestamps) == 0 or current_time - timestamps[-1] >= screenshot_interval:
                timestamps.append(current_time)
        
        # Limit number of screenshots
        if len(timestamps) > settings.MAX_SCREENSHOTS_PER_VIDEO:
            step = len(timestamps) // settings.MAX_SCREENSHOTS_PER_VIDEO
            timestamps = timestamps[::step][:settings.MAX_SCREENSHOTS_PER_VIDEO]
        
        # Capture frames
        screenshots = await self.capture_video_frames(video_id, timestamps)
        
        # Add screenshot references to processed text
        for para in processed_text:
            nearest_timestamp = min(timestamps, key=lambda x: abs(x - float(para["start_time"])))
            para["screenshot"] = f"{video_id}_{int(nearest_timestamp)}.jpg"
        
        return processed_text, screenshots, input_tokens, output_tokens, price
    
    async def download_video(self, video_id: str) -> str:
        """Download video from YouTube using yt-dlp."""
        output_path = os.path.join(settings.DOWNLOAD_DIR, f"{video_id}.mp4")
        
        # If video already exists, return the path
        if os.path.exists(output_path):
            logger.info(f"Video {video_id} already downloaded")
            return output_path

        try:
            url = f"https://www.youtube.com/watch?v={video_id}"
            
            # Configure yt-dlp options
            ydl_opts = {
                'format': 'best[ext=mp4]',  # Best quality MP4
                'outtmpl': output_path,     # Output template
                'quiet': True,              # Reduce output
                'no_warnings': True,        # Suppress warnings
                'extract_flat': True,       # Don't extract playlists
                'nocheckcertificate': True, # Skip HTTPS certificate validation
                'prefer_ffmpeg': True,      # Prefer ffmpeg for post-processing
                # Add retries
                'retries': 3,
                'fragment_retries': 3,
                'skip_unavailable_fragments': True,
                # Add rate limiting
                'sleep_interval': 1,
                'max_sleep_interval': 5,
                'sleep_interval_requests': 1,
                # Add timeout
                'socket_timeout': 30,
            }

            loop = asyncio.get_event_loop()
            
            async def _download():
                def download_video():
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        try:
                            ydl.download([url])
                        except Exception as e:
                            logger.error(f"yt-dlp download error: {str(e)}")
                            raise

                # Run the download in a thread pool
                await loop.run_in_executor(None, download_video)

            # Download with timeout
            try:
                await asyncio.wait_for(_download(), timeout=300)  # 5 minutes timeout
            except asyncio.TimeoutError:
                raise TimeoutError("Video download timed out after 5 minutes")

            if not os.path.exists(output_path):
                raise FileNotFoundError("Video file not found after download")

            logger.info(f"Successfully downloaded video {video_id}")
            return output_path

        except Exception as e:
            logger.error(f"Error downloading video {video_id}: {str(e)}")
            if os.path.exists(output_path):
                try:
                    os.remove(output_path)  # Clean up partial download
                except:
                    pass
            raise ValueError(f"Failed to download video: {str(e)}")

    async def capture_video_frames(
        self,
        video_id: str,
        timestamps: List[float]
    ) -> List[str]:
        """Capture frames from video at specified timestamps."""
        try:
            # First ensure we have the video
            video_path = os.path.join(settings.DOWNLOAD_DIR, f"{video_id}.mp4")
            if not os.path.exists(video_path):
                logger.info(f"Downloading video {video_id} for frame capture")
                try:
                    video_path = await self.download_video(video_id)
                except Exception as e:
                    logger.error(f"Failed to download video, proceeding without screenshots: {str(e)}")
                    return []  # Return empty list if video download fails

            frames = []
            try:
                cap = cv2.VideoCapture(video_path)
                if not cap.isOpened():
                    logger.error(f"Failed to open video file: {video_path}")
                    return []

                fps = cap.get(cv2.CAP_PROP_FPS)
                logger.debug(f"Video FPS: {fps}")

                for timestamp in timestamps:
                    frame_num = int(timestamp * fps)
                    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
                    ret, frame = cap.read()
                    
                    if ret:
                        frame_path = os.path.join(
                            settings.SCREENSHOTS_DIR,
                            f"{video_id}_{int(timestamp)}.jpg"
                        )
                        cv2.imwrite(frame_path, frame)
                        frames.append(frame_path)
                        logger.debug(f"Captured frame at timestamp {timestamp}")
                    else:
                        logger.warning(f"Failed to capture frame at timestamp {timestamp}")

                return frames
                
            finally:
                if 'cap' in locals():
                    cap.release()

        except Exception as e:
            logger.error(f"Error capturing video frames: {str(e)}")
            return []  # Return empty list instead of raising exception

    async def get_chapters(
        self,
        video_id: str,
        paragraphs: List[Dict],
        chapter_source: ChapterSource
    ) -> Tuple[List[Dict], int, int, float]:
        """Get chapters based on specified source."""
        if chapter_source == ChapterSource.DESCRIPTION:
            chapters = await self.chapters_service.get_video_chapters(video_id)
            if not chapters:
                logger.warning("No chapters found in description, falling back to auto-generation")
                return await self.generate_chapters(paragraphs)
            return chapters, 0, 0, 0
        else:
            return await self.generate_chapters(paragraphs)

    async def generate_chapters(
        self,
        paragraphs: List[Dict]
    ) -> Tuple[List[Dict], int, int, float]:
        """Generate chapters using OpenAI."""
        chapters_data, input_tokens, output_tokens, price = await self.openai_service.generate_toc(paragraphs)
        
        # Standardize chapter format
        standardized_chapters = []
        for chapter in chapters_data:
            # Convert start_paragraph_number to timestamp using paragraph data
            if chapter.get('start_paragraph_number') is not None:
                start_idx = min(chapter['start_paragraph_number'], len(paragraphs) - 1)
                timestamp = paragraphs[start_idx]['start_time']
                
                standardized_chapters.append({
                    'timestamp': float(timestamp),
                    'title': chapter['title']
                })
        
        return standardized_chapters, input_tokens, output_tokens, price

    @staticmethod
    async def structure_chapters(
        paragraphs: List[Dict],
        chapters_data: List[Dict]
    ) -> List[Chapter]:
        """Structure paragraphs into chapters based on chapter data."""
        chapters = []
        total_paragraphs = len(paragraphs)

        if not chapters_data:
            # Create a single chapter if no chapters data
            chapter = Chapter(
                num_chapter=0,
                title="Complete Content",
                start_paragraph_number=0,
                end_paragraph_number=total_paragraphs,
                start_time=paragraphs[0]["start_time"],
                end_time=paragraphs[-1]["start_time"],
                paragraphs=[p["paragraph_text"] for p in paragraphs],
                paragraph_timestamps=[p["start_time"] for p in paragraphs]
            )
            return [chapter]

        # Sort chapters by timestamp
        chapters_data = sorted(chapters_data, key=lambda x: x['timestamp'])

        # Process each chapter
        for i, chapter_data in enumerate(chapters_data):
            timestamp = float(chapter_data["timestamp"])
            
            # Find paragraphs that belong to this chapter
            chapter_paragraphs = []
            chapter_timestamps = []
            
            # Calculate end timestamp
            end_timestamp = float('inf')
            if i < len(chapters_data) - 1:
                end_timestamp = float(chapters_data[i + 1]['timestamp'])

            # Collect paragraphs for this chapter
            for p in paragraphs:
                p_time = float(p["start_time"])
                if p_time >= timestamp and p_time < end_timestamp:
                    chapter_paragraphs.append(p["paragraph_text"])
                    chapter_timestamps.append(p_time)

            # Only create chapter if it has paragraphs
            if chapter_paragraphs:
                chapter = Chapter(
                    num_chapter=len(chapters),
                    title=chapter_data["title"],
                    start_paragraph_number=0,  # We'll use timestamps instead
                    end_paragraph_number=len(chapter_paragraphs),
                    start_time=timestamp,
                    end_time=end_timestamp if end_timestamp != float('inf') else chapter_timestamps[-1],
                    paragraphs=chapter_paragraphs,
                    paragraph_timestamps=chapter_timestamps
                )
                chapters.append(chapter)

        # If no valid chapters were created, create a single chapter
        if not chapters:
            chapter = Chapter(
                num_chapter=0,
                title="Complete Content",
                start_paragraph_number=0,
                end_paragraph_number=total_paragraphs,
                start_time=paragraphs[0]["start_time"],
                end_time=paragraphs[-1]["start_time"],
                paragraphs=[p["paragraph_text"] for p in paragraphs],
                paragraph_timestamps=[p["start_time"] for p in paragraphs]
            )
            chapters = [chapter]

        return chapters

class YouTubeProcessingJob:
    def __init__(
        self,
        job_id: str,
        video_id: str,
        mode: ProcessingMode = ProcessingMode.DETAILED,
        chapter_source: ChapterSource = ChapterSource.AUTO
    ):
        self.job_id = job_id
        self.video_id = video_id
        self.mode = mode
        self.chapter_source = chapter_source
        self.status = "pending"
        self.progress = 0.0
        self.result = None
        self.error = None
        self.youtube_service = YouTubeService()
        self._save_status()

    def _save_status(self):
        """Save job status to cache."""
        status_path = os.path.join(settings.CACHE_DIR, f"{self.job_id}.json")
        status_dict = {
            "job_id": self.job_id,
            "video_id": self.video_id,
            "mode": self.mode.value,
            "chapter_source": self.chapter_source.value,
            "status": self.status,
            "progress": self.progress,
            "error": self.error,
            "result": self.result.dict() if self.result else None
        }
        
        with open(status_path, 'w') as f:
            json.dump(status_dict, f, indent=4)

    

    @staticmethod
    def load(job_id: str) -> "YouTubeProcessingJob":
        """Load job status from cache."""
        status_path = os.path.join(settings.CACHE_DIR, f"{job_id}.json")
        if not os.path.exists(status_path):
            raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
        
        with open(status_path) as f:
            data = json.load(f)
            job = YouTubeProcessingJob(
                data["job_id"],
                data["video_id"],
                ProcessingMode(data["mode"]),
                ChapterSource(data["chapter_source"])
            )
            job.status = data["status"]
            job.progress = data["progress"]
            job.error = data["error"]
            
            if data["result"]:
                job.result = YouTubeResult(**data["result"])
                
            return job
        

    @classmethod
    def get_latest_for_video(cls, video_id: str) -> Optional["YouTubeProcessingJob"]:
        """
        Get the latest processing job for a specific video ID.
        
        Args:
            video_id: The YouTube video ID to search for
            
        Returns:
            Optional[YouTubeProcessingJob]: The most recent job for the video, or None if not found
        """
        try:
            # Get all job files from cache directory
            cache_files = [f for f in os.listdir(settings.CACHE_DIR) if f.endswith('.json')]
            matching_jobs = []

            # Find all jobs for this video ID
            for cache_file in cache_files:
                file_path = os.path.join(settings.CACHE_DIR, cache_file)
                try:
                    with open(file_path, 'r') as f:
                        job_data = json.load(f)
                        if job_data.get("video_id") == video_id:
                            # Parse the timestamp from job_id
                            # Expected format: yt_job_YYYYMMDD_HHMMSS_VIDEO_ID
                            try:
                                timestamp_str = job_data["job_id"].split("_")[2:4]
                                timestamp = datetime.strptime(
                                    "_".join(timestamp_str), 
                                    "%Y%m%d_%H%M%S"
                                )
                                matching_jobs.append((timestamp, job_data))
                            except (IndexError, ValueError):
                                logger.warning(f"Invalid job ID format in {cache_file}")
                                continue
                except Exception as e:
                    logger.error(f"Error reading cache file {cache_file}: {str(e)}")
                    continue

            if not matching_jobs:
                return None

            # Sort by timestamp (newest first) and get the most recent job
            matching_jobs.sort(reverse=True)  # Sort by timestamp
            latest_job_data = matching_jobs[0][1]  # Get the job data

            # Create and return the job instance
            job = cls(
                latest_job_data["job_id"],
                latest_job_data["video_id"],
                ProcessingMode(latest_job_data["mode"]),
                ChapterSource(latest_job_data["chapter_source"])
            )
            job.status = latest_job_data["status"]
            job.progress = latest_job_data["progress"]
            job.error = latest_job_data["error"]
            
            if latest_job_data.get("result"):
                job.result = YouTubeResult(**latest_job_data["result"])

            return job

        except Exception as e:
            logger.error(f"Failed to get latest job for video {video_id}: {str(e)}")
            return None
        
    @classmethod
    async def get_completed_result(cls, video_id: str) -> YouTubeResult:
        """
        Get the completed result for a video, handling all status checks.
        
        Args:
            video_id: The YouTube video ID
            
        Returns:
            YouTubeResult: The processed result
            
        Raises:
            HTTPException: If the result is not available or processing is not complete
        """
        latest_job = cls.get_latest_for_video(video_id)
        
        if not latest_job:
            raise HTTPException(
                status_code=404,
                detail="No processing job found for this video"
            )

        # Map status to appropriate responses
        status_responses = {
            "failed": (400, f"Video processing failed: {latest_job.error or 'Unknown error'}"),
            "pending": (400, "Video processing has not started"),
            "processing": (400, f"Video processing is still in progress ({latest_job.progress:.0%} complete)"),
            "cancelled": (400, "Video processing was cancelled"),
            "completed": None  # Handle separately
        }

        if latest_job.status in status_responses:
            if latest_job.status == "completed":
                if not latest_job.result:
                    raise HTTPException(
                        status_code=404,
                        detail="No results found for completed video"
                    )
                return latest_job.result
            else:
                status_code, detail = status_responses[latest_job.status]
                raise HTTPException(status_code=status_code, detail=detail)
        
        raise HTTPException(
            status_code=400,
            detail=f"Invalid job status: {latest_job.status}"
        )

    @property
    def is_complete(self) -> bool:
        """Check if the job is complete and successful."""
        return self.status == "completed" and self.result is not None

    @property
    def is_processing(self) -> bool:
        """Check if the job is still processing."""
        return self.status == "processing"

    @property
    def is_failed(self) -> bool:
        """Check if the job failed."""
        return self.status == "failed"

    @property
    def is_pending(self) -> bool:
        """Check if the job is pending."""
        return self.status == "pending"


    async def update_progress(self, progress: float, description: str = ""):
        """Update job progress."""
        self.progress = progress
        logger.info(f"Job {self.job_id}: {description} - {progress:.2%}")
        self._save_status()

    async def process(self):
        """Process YouTube video based on selected mode."""
        try:
            self.status = "processing"
            self._save_status()
            
            # Check cache
            cache_key = f"{self.mode.value}_{self.chapter_source.value}_final"
            if cached_result := await self.youtube_service.get_cached_result(
                self.video_id,
                cache_key
            ):
                self.result = YouTubeResult(**cached_result)
                self.status = "completed"
                self.progress = 1.0
                self._save_status()
                return

            # Process based on mode
            await self.update_progress(0.1, "Starting processing")
            
            if self.mode == ProcessingMode.SIMPLE:
                paragraphs, input_tokens, output_tokens, price = await self.youtube_service.process_simple(self.video_id)
                screenshots = []
                await self.update_progress(0.5, "Simple processing completed")
            
            elif self.mode == ProcessingMode.DETAILED:
                paragraphs, input_tokens, output_tokens, price = await self.youtube_service.process_detailed(self.video_id)
                screenshots = []
                await self.update_progress(0.5, "Detailed processing completed")
            
            else:  # DETAILED_WITH_SCREENSHOTS
                paragraphs, screenshots, input_tokens, output_tokens, price = await self.youtube_service.process_detailed_with_screenshots(
                    self.video_id,
                    settings.DEFAULT_SCREENSHOT_INTERVAL
                )
                await self.update_progress(0.6, "Processing with screenshots completed")

            # Get chapters based on source and mode
            if self.mode != ProcessingMode.SIMPLE:
                await self.update_progress(0.7, "Getting chapters")
                chapters_data, ch_input_tokens, ch_output_tokens, ch_price = await self.youtube_service.get_chapters(
                    self.video_id,
                    paragraphs,
                    self.chapter_source
                )
                input_tokens += ch_input_tokens
                output_tokens += ch_output_tokens
                price += ch_price
                
                await self.update_progress(0.8, "Structuring chapters")
                chapters = await YouTubeService.structure_chapters(paragraphs, chapters_data)
            else:
                chapters = [Chapter(
                    num_chapter=0,
                    title="Complete Content",
                    start_paragraph_number=0,
                    end_paragraph_number=1,
                    start_time=paragraphs[0]["start_time"],
                    end_time=paragraphs[0]["start_time"] + 1,
                    paragraphs=[p["paragraph_text"] for p in paragraphs],
                    paragraph_timestamps=[p["start_time"] for p in paragraphs]
                )]

# In YouTubeProcessingJob.process()
    # Replace the screenshots section with:

            # Add screenshots if available
            if screenshots:
                await self.update_progress(0.9, "Adding screenshots to chapters")
                for chapter in chapters:
                    chapter_screenshots = [
                        s for s in screenshots
                        if float(s.split("_")[-1].split(".")[0]) >= chapter.start_time
                        and float(s.split("_")[-1].split(".")[0]) <= chapter.end_time
                    ]
                    # Create new chapter with screenshots
                    chapter_dict = chapter.model_dump()
                    chapter_dict['screenshots'] = chapter_screenshots
                    chapters[chapters.index(chapter)] = Chapter(**chapter_dict)

            # Create final result
            result = YouTubeResult(
                video_id=self.video_id,
                chapters=chapters,
                stats=ProcessingStats(
                    total_input_tokens=input_tokens,
                    total_output_tokens=output_tokens,
                    total_price=price
                )
            )

            self.result = result
            await self.youtube_service.save_cache(
                self.video_id,
                cache_key,
                result.dict()
            )

            self.status = "completed"
            self.progress = 1.0
            self._save_status()

        except Exception as e:
            logger.error(f"Job {self.job_id} failed: {str(e)}")
            self.status = "failed"
            self.error = str(e)
            self._save_status()
            raise

    async def cancel(self):
        """Cancel the processing job."""
        if self.status == "processing":
            self.status = "cancelled"
            self.error = "Job cancelled by user"
            self._save_status()
            return True
        return False

    async def cleanup(self):
        """Clean up any temporary files created during processing."""
        try:
            # Clean up screenshots if they exist
            if self.result and hasattr(self.result, 'chapters'):
                for chapter in self.result.chapters:
                    if hasattr(chapter, 'screenshots'):
                        for screenshot in chapter.screenshots:
                            if os.path.exists(screenshot):
                                os.remove(screenshot)
            
            # Clean up status file
            status_path = os.path.join(settings.CACHE_DIR, f"{self.job_id}.json")
            if os.path.exists(status_path):
                os.remove(status_path)
                
        except Exception as e:
            logger.error(f"Error cleaning up job {self.job_id}: {str(e)}")
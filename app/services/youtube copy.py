# app/services/youtube.py
import os
import json
from datetime import datetime
import logging
from typing import Dict, List, Optional, Any, Tuple
from youtube_transcript_api import YouTubeTranscriptApi
from fastapi import HTTPException

from app.core.settings import settings
from app.services.openai import OpenAIService
from app.services.transcription import TranscriptionService
from app.models.youtube import YouTubeResult, ProcessingStats, Chapter

logger = logging.getLogger(__name__)

class YouTubeService:
    def __init__(self):
        self.openai_service = OpenAIService()
        self.transcription_service = TranscriptionService()
        self._ensure_directories()

    def _ensure_directories(self):
        """Ensure all required directories exist."""
        for directory in [settings.CACHE_DIR]:
            os.makedirs(directory, exist_ok=True)

    async def get_transcript(self, video_id: str, languages: List[str] = ["en"]) -> List[Dict[str, Any]]:
        """Fetch transcript from YouTube video."""
        try:
            # First try YouTube API
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
            return [{'start': s['start'], 'text': s['text']} for s in transcript]
        except Exception as e:
            logger.warning(f"Failed to get YouTube transcript, falling back to Replicate: {str(e)}")
            
            # Fallback to Replicate transcription
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
        cache_file = os.path.join(settings.CACHE_DIR, f"{video_id}_{cache_type}.json")
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                return json.load(f)
        return None

    async def save_cache(self, video_id: str, cache_type: str, data: Dict):
        """Save processing result to cache."""
        cache_file = os.path.join(settings.CACHE_DIR, f"{video_id}_{cache_type}.json")
        
        # Convert Pydantic models to dict before saving
        if hasattr(data, 'dict'):
            data = data.dict()
        
        with open(cache_file, 'w') as f:
            json.dump(data, f, indent=4)

    async def transform_text_segments(self, text_segments: List[Dict], num_words: int = 50) -> List[str]:
        """Transform text segments into fixed word-length chunks."""
        transformed_segments = []
        current_index = 0
        num_segments = len(text_segments)

        for i in range(num_segments):
            current_index = i
            current_segment = text_segments[current_index]
            current_text = current_segment['text']

            combined_text = " ".join(current_text.split()[:num_words])
            number_words_collected = len(current_text.split())

            while number_words_collected < num_words and (current_index + 1) < num_segments:
                current_index += 1
                next_segment = text_segments[current_index]
                next_text = next_segment['text']
                next_words = next_text.split()

                if number_words_collected + len(next_words) <= num_words:
                    combined_text += ' ' + next_text
                    number_words_collected += len(next_words)
                else:
                    words_needed = num_words - number_words_collected
                    combined_text += ' ' + ' '.join(next_words[:words_needed])
                    number_words_collected = num_words

            transformed_segments.append(combined_text)

        return transformed_segments

    @staticmethod
    async def structure_chapters(
        paragraphs: List[Dict],
        table_of_content: List[Dict]
    ) -> List[Chapter]:
        """Structure paragraphs into chapters based on table of contents."""
        chapters = []
        total_paragraphs = len(paragraphs)

        # First, validate and clean up the table of contents
        valid_toc = []
        for entry in table_of_content:
            if entry['start_paragraph_number'] < total_paragraphs:
                valid_toc.append(entry)
            else:
                logger.warning(f"Skipping TOC entry with invalid paragraph number: {entry}")

        if not valid_toc:
            logger.warning("No valid TOC entries found. Creating single chapter.")
            # Create a single chapter if no valid TOC entries
            chapter = Chapter(
                num_chapter=0,
                title="Complete Content",
                start_paragraph_number=0,
                end_paragraph_number=total_paragraphs,
                start_time=paragraphs[0]['start_time'] if paragraphs else 0,
                end_time=paragraphs[-1]['start_time'] if paragraphs else 0,
                paragraphs=[p['paragraph_text'] for p in paragraphs],
                paragraph_timestamps=[p['start_time'] for p in paragraphs]
            )
            return [chapter]

        # Process valid TOC entries
        for i, toc_entry in enumerate(valid_toc):
            try:
                start_idx = toc_entry['start_paragraph_number']
                
                # Determine end index for this chapter
                if i < len(valid_toc) - 1:
                    end_idx = min(valid_toc[i + 1]['start_paragraph_number'], total_paragraphs)
                else:
                    # For the last chapter, check if it would contain too many paragraphs
                    remaining_paragraphs = total_paragraphs - start_idx
                    if remaining_paragraphs > 10:  # Threshold for max paragraphs in a chapter
                        # Create additional chapters for remaining paragraphs
                        chunk_size = 5  # Number of paragraphs per chapter
                        for chunk_start in range(start_idx, total_paragraphs, chunk_size):
                            chunk_end = min(chunk_start + chunk_size, total_paragraphs)
                            chapter_num = len(chapters)
                            
                            # Create chapter title based on first paragraph content
                            first_para = paragraphs[chunk_start]['paragraph_text']
                            chapter_title = f"Part {chapter_num + 1}: {first_para[:50]}..."
                            
                            chapter = {
                                'num_chapter': chapter_num,
                                'title': chapter_title,
                                'start_paragraph_number': chunk_start,
                                'end_paragraph_number': chunk_end,
                                'start_time': paragraphs[chunk_start]['start_time'],
                                'end_time': paragraphs[chunk_end - 1]['start_time'],
                                'paragraphs': [
                                    paragraphs[j]['paragraph_text']
                                    for j in range(chunk_start, chunk_end)
                                ],
                                'paragraph_timestamps': [
                                    paragraphs[j]['start_time']
                                    for j in range(chunk_start, chunk_end)
                                ]
                            }
                            chapters.append(Chapter(**chapter))
                        continue
                    end_idx = total_paragraphs

                # Skip if start index is out of range
                if start_idx >= total_paragraphs:
                    continue

                # Create chapter with safe index access
                chapter = {
                    'num_chapter': len(chapters),
                    'title': toc_entry['title'],
                    'start_paragraph_number': start_idx,
                    'end_paragraph_number': end_idx,
                    'start_time': paragraphs[start_idx]['start_time'],
                    'end_time': paragraphs[min(end_idx - 1, total_paragraphs - 1)]['start_time'],
                    'paragraphs': [
                        paragraphs[j]['paragraph_text']
                        for j in range(start_idx, end_idx)
                        if j < total_paragraphs
                    ],
                    'paragraph_timestamps': [
                        paragraphs[j]['start_time']
                        for j in range(start_idx, end_idx)
                        if j < total_paragraphs
                    ]
                }

                chapters.append(Chapter(**chapter))

            except Exception as e:
                logger.error(f"Error processing chapter {i}: {str(e)}")
                continue

        # If no chapters were created successfully, create a single chapter
        if not chapters:
            logger.warning("Failed to create chapters. Creating single chapter.")
            chapter = Chapter(
                num_chapter=0,
                title="Complete Content",
                start_paragraph_number=0,
                end_paragraph_number=total_paragraphs,
                start_time=paragraphs[0]['start_time'] if paragraphs else 0,
                end_time=paragraphs[-1]['start_time'] if paragraphs else 0,
                paragraphs=[p['paragraph_text'] for p in paragraphs],
                paragraph_timestamps=[p['start_time'] for p in paragraphs]
            )
            return [chapter]

        return chapters


class YouTubeProcessingJob:
    def __init__(self, job_id: str, video_id: str):
        self.job_id = job_id
        self.video_id = video_id
        self.status = "pending"
        self.progress = 0.0
        self.result = None
        self.error = None
        self.youtube_service = YouTubeService()
        self._save_status()

    def _save_status(self):
        """Save job status to cache."""
        status_path = os.path.join(settings.CACHE_DIR, f"{self.job_id}.json")
        
        # Create a dict for JSON serialization
        status_dict = {
            "job_id": self.job_id,
            "video_id": self.video_id,
            "status": self.status,
            "progress": self.progress,
            "error": self.error
        }

        # Handle result serialization
        if self.result is not None:
            if hasattr(self.result, 'dict'):
                status_dict["result"] = self.result.dict()
            else:
                status_dict["result"] = self.result
        else:
            status_dict["result"] = None

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
            
            # Create job instance
            job = YouTubeProcessingJob(data["job_id"], data["video_id"])
            job.status = data["status"]
            job.progress = data["progress"]
            job.error = data["error"]
            
            # Convert result back to Pydantic model if it exists and is not None
            if data["result"] is not None:
                try:
                    if isinstance(data["result"], dict) and "video_id" in data["result"]:
                        job.result = YouTubeResult(**data["result"])
                    else:
                        job.result = data["result"]
                except Exception as e:
                    logger.warning(f"Could not convert result to YouTubeResult model: {e}")
                    job.result = data["result"]
            else:
                job.result = None
                
            return job

    async def update_progress(self, progress: float, description: str = ""):
        """Update job progress."""
        self.progress = progress
        logger.info(f"Job {self.job_id}: {description} - {progress:.2%}")
        self._save_status()

    async def process(self):
        """Process YouTube video with progress tracking."""
        try:
            self.status = "processing"
            self._save_status()

            # Step 1: Check cache
            if cached_result := await self.youtube_service.get_cached_result(
                self.video_id, "final"
            ):
                try:
                    self.result = YouTubeResult(**cached_result)
                except Exception as e:
                    logger.warning(f"Could not convert cached result to YouTubeResult model: {e}")
                    self.result = cached_result
                self.status = "completed"
                self.progress = 1.0
                self._save_status()
                return

            # Step 2: Get transcript
            await self.update_progress(0.1, "Getting transcript")
            transcript = await self.youtube_service.get_transcript(self.video_id)
            if not transcript:
                raise ValueError("Failed to get transcript")
                
            await self.youtube_service.save_cache(self.video_id, "transcript", transcript)

            # Step 3: Process transcript into paragraphs
            await self.update_progress(0.4, "Processing transcript")
            paragraphs, input_tokens, output_tokens, price = await self.youtube_service.openai_service.transcript_to_paragraphs(
                transcript,
                progress_callback=self.update_progress
            )
            
            if not paragraphs:
                raise ValueError("Failed to process transcript into paragraphs")

            # Step 4: Add timestamps
            await self.update_progress(0.6, "Adding timestamps")
            paragraphs_with_timestamps = await self.youtube_service.openai_service.add_timestamps_to_paragraphs(
                transcript, paragraphs
            )

            # Step 5: Generate TOC
            await self.update_progress(0.8, "Generating table of contents")
            toc, toc_input_tokens, toc_output_tokens, toc_price = await self.youtube_service.openai_service.generate_toc(
                paragraphs_with_timestamps
            )

            if not toc:
                logger.warning("Failed to generate TOC, using single chapter")
                toc = [{
                    'start_paragraph_number': 0,
                    'title': 'Complete Content'
                }]

            # Step 6: Structure chapters
            await self.update_progress(0.9, "Structuring chapters")
            chapters = await YouTubeService.structure_chapters(
                paragraphs_with_timestamps, toc
            )

            # Create final result as YouTubeResult model
            result = YouTubeResult(
                video_id=self.video_id,
                chapters=chapters,
                stats=ProcessingStats(
                    total_input_tokens=input_tokens + toc_input_tokens,
                    total_output_tokens=output_tokens + toc_output_tokens,
                    total_price=price + toc_price
                )
            )

            # Save as dict for JSON serialization
            self.result = result.dict()

            # Cache final result
            await self.youtube_service.save_cache(self.video_id, "final", self.result)

            self.status = "completed"
            self.progress = 1.0
            self._save_status()

        except Exception as e:
            logger.error(f"Job {self.job_id} failed: {str(e)}")
            self.status = "failed"
            self.error = str(e)
            self._save_status()
            raise
# app/services/transcription.py
from io import BytesIO
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
from pytube import YouTube
import replicate
from typing import Dict, List
from fastapi import HTTPException
import os
from app.core.settings import settings


logger = logging.getLogger(__name__)

class TranscriptionService:
    def __init__(self):
        self._ensure_replicate_token()

    def _ensure_replicate_token(self):
        """Ensure REPLICATE_API_TOKEN is set"""
        if not settings.has_replicate_token:
            raise ValueError(
                "REPLICATE_API_TOKEN environment variable is not set. "
                "Please set it in your .env file or environment variables."
            )
        # Set for replicate package
        os.environ["REPLICATE_API_TOKEN"] = settings.REPLICATE_API_TOKEN

    async def transcribe_video(self, video_id: str) -> List[Dict]:
        """Main method to transcribe a YouTube video."""
        if not settings.has_replicate_token:
            raise ValueError("Replicate API token not configured")
        
        try:
            start_time = time.time()
            
            # Get video audio
            buffer = await self._get_audio_buffer(video_id)
            
            # Get transcription
            transcription = await self._get_transcription(buffer)
            
            # Format transcription
            formatted_transcription = self._format_transcription(transcription)
            
            end_time = time.time()
            logger.info(f"Transcription completed in {end_time - start_time:.2f} seconds")
            
            return formatted_transcription
            
        except Exception as e:
            logger.error(f"Error transcribing video {video_id}: {str(e)}")
            raise

    async def _get_audio_buffer(self, video_id: str) -> BytesIO:
        """Download YouTube video audio into memory buffer."""
        try:
            yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
            
            # Get best audio stream
            audio_streams = yt.streams.filter(only_audio=True)
            itag = self._get_webm_itag(audio_streams)
            if not itag:
                raise ValueError("No suitable audio stream found")
                
            stream = yt.streams.get_by_itag(itag)
            
            # Download to buffer
            buffer = BytesIO()
            stream.stream_to_buffer(buffer)
            buffer.name = "audio.webm"
            buffer.seek(0)
            
            return buffer
            
        except Exception as e:
            logger.error(f"Error downloading audio for video {video_id}: {str(e)}")
            raise

    def _get_webm_itag(self, audio_streams) -> int:
        """Get itag for webm audio stream."""
        for stream in audio_streams:
            if stream.mime_type == 'audio/webm':
                return stream.itag
        return None

    async def _get_transcription(self, buffer: BytesIO) -> Dict:
        """Get transcription using Replicate's Whisper model."""
        try:
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as executor:
                transcription = await loop.run_in_executor(
                    executor,
                    self._run_replicate,
                    buffer
                )
            return transcription
            
        except Exception as e:
            logger.error(f"Error during transcription: {str(e)}")
            raise

    def _run_replicate(self, buffer: BytesIO) -> Dict:
        """Run Replicate's Whisper model."""
        return replicate.run(
            "vaibhavs10/incredibly-fast-whisper:3ab86df6c8f54c11309d4d1f930ac292bad43ace52d10c80d87eb258b3c9f79c",
            input={
                "audio": buffer,
                "batch_size": 64
            }
        )

    def _format_transcription(self, transcription: Dict) -> List[Dict]:
        """Format Replicate transcription to match required format."""
        formatted = []
        for segment in transcription.get('segments', []):
            formatted.append({
                'start': float(segment.get('start', 0)),
                'text': segment.get('text', '').strip()
            })
        return formatted
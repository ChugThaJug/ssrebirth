# app/services/chapters.py
import re
from typing import List, Dict, Optional
from pytube import YouTube
import logging

logger = logging.getLogger(__name__)

class ChaptersService:
    @staticmethod
    def parse_chapters_from_description(text: str) -> Optional[List[Dict[str, any]]]:
        """
        Parse chapters from video description text.
        Supports common YouTube chapter formats like:
        00:00 Chapter 1
        00:00:00 Chapter 1
        """
        chapters = []
        pattern = r'((?:\d{1,2}:)?(?:\d{1,2}:\d{2}|\d{1,2}:\d{2}:\d{2}))\s+(.*?)(?=\n(?:\d{1,2}:)?(?:\d{1,2}:\d{2}|\d{1,2}:\d{2}:\d{2})|$)'
        matches = re.finditer(pattern, text, re.MULTILINE)
        
        for match in matches:
            time_str, title = match.groups()
            
            # Convert time string to seconds
            time_parts = time_str.split(':')
            if len(time_parts) == 2:  # MM:SS
                minutes, seconds = map(int, time_parts)
                total_seconds = minutes * 60 + seconds
            else:  # HH:MM:SS
                hours, minutes, seconds = map(int, time_parts)
                total_seconds = hours * 3600 + minutes * 60 + seconds
                
            chapters.append({
                "timestamp": total_seconds,
                "title": title.strip()
            })
            
        if not chapters:
            logger.warning("No chapters found in description")
            return None
            
        return chapters

    @staticmethod
    async def get_video_chapters(video_id: str) -> Optional[List[Dict[str, any]]]:
        """
        Attempt to extract chapters from YouTube video description.
        Returns None if no chapters are found.
        """
        try:
            # Create YouTube object
            yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
            
            # Get video description
            description = yt.description
            
            # Parse chapters from description
            chapters = ChaptersService.parse_chapters_from_description(description)
            
            return chapters
            
        except Exception as e:
            logger.error(f"Error getting video chapters: {str(e)}")
            return None
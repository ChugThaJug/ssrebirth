# app/core/settings.py
from pydantic_settings import BaseSettings
import os
from typing import Dict

class Settings(BaseSettings):
    # App settings
    APP_TITLE: str = "Video Processing API"
    APP_DESCRIPTION: str = "API for processing videos and generating structured content"
    APP_VERSION: str = "1.0.0"
    
    # Directory settings
    CACHE_DIR: str = "cache"
    DOWNLOAD_DIR: str = "downloads"
    UPLOAD_DIR: str = "uploads"
    OUTPUT_DIR: str = "processed"

        # Optional: Override default token prices
    INPUT_TOKEN_PRICE: float = 0.0001
    OUTPUT_TOKEN_PRICE: float = 0.0002
    
    # API Keys
    REPLICATE_API_TOKEN: str = os.getenv("REPLICATE_API_TOKEN")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    
    # OpenAI settings
    MODEL: str = "gpt-4o-mini"
    
    # Token prices (per 1M tokens)
    INPUT_TOKEN_PRICE: float = 0.0001
    OUTPUT_TOKEN_PRICE: float = 0.0002
    
    # Processing settings
    MAX_CHARS: int = 100000
    CHUNK_SIZE: int = 1000
    
    # Retry settings
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 1
    
    # Cache settings
    CACHE_RETENTION_DAYS: int = 7

        # Directory settings
    SCREENSHOTS_DIR: str = "screenshots"
    
    # Processing settings
    DEFAULT_SCREENSHOT_INTERVAL: int = 60  # seconds
    MAX_SCREENSHOTS_PER_VIDEO: int = 50
    
    # Processing modes
    PROCESSING_MODES: List[ProcessingMode] = [
        ProcessingMode.SIMPLE,
        ProcessingMode.DETAILED,
        ProcessingMode.DETAILED_WITH_SCREENSHOTS
    ]
    
    CHAPTER_SOURCES: List[ChapterSource] = [
        ChapterSource.AUTO,
        ChapterSource.DESCRIPTION
    ]
    
    class Config:
        env_file = ".env"

    @property
    def has_replicate_token(self) -> bool:
        return bool(self.REPLICATE_API_TOKEN)

# Initialize settings
settings = Settings()

# Create necessary directories
for directory in [
    settings.CACHE_DIR,
    settings.DOWNLOAD_DIR,
    settings.UPLOAD_DIR,
    settings.OUTPUT_DIR,
    settings.SCREENSHOTS_DIR
]:
    os.makedirs(directory, exist_ok=True)
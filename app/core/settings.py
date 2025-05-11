# app/core/settings.py
from pydantic_settings import BaseSettings
from typing import Dict, List, Optional
import os
from app.core.enums import ProcessingMode, ChapterSource

class Settings(BaseSettings):
    """Application settings and configuration."""
    
    # App info
    APP_TITLE: str = "Video Processing API"
    APP_DESCRIPTION: str = "API for processing YouTube videos and generating structured content"
    APP_VERSION: str = "1.0.0"
    
    # API Keys
    REPLICATE_API_TOKEN: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None

    PINECONE_API_KEY: Optional[str] = None


    # Frontend settings
    FRONTEND_URL: str = "http://localhost:5173"  # SvelteKit dev server default port
    
    # CORS Settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",    # SvelteKit dev server
        "http://localhost:4173",    # SvelteKit preview
        "http://localhost:3000",    # Alternative dev port
    ]
    CORS_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    CORS_HEADERS: List[str] = ["*"]
    CORS_EXPOSE_HEADERS: List[str] = []
    ALLOW_CREDENTIALS: bool = True
    
    # Directory settings
    CACHE_DIR: str = "cache"
    DOWNLOAD_DIR: str = "downloads"
    UPLOAD_DIR: str = "uploads"
    OUTPUT_DIR: str = "processed"
    SCREENSHOTS_DIR: str = "screenshots"
    
    # OpenAI settings
    MODEL: str = "gpt-4o-mini"
    MAX_TOKENS: int = 4000
    TEMPERATURE: float = 0.7
    
    # Token prices (per 1M tokens)
    TOKEN_PRICES: Dict[str, Dict[str, float]] = {
        'gpt-4o': {'input': 5/1000000, 'output': 15/1000000},
        'gpt-4o-2024-08-06': {'input': 2.5/1000000, 'output': 10/1000000},
        'gpt-4o-mini-2024-07-18': {'input': 0.15/1000000, 'output': 0.6/1000000},
        'gpt-4o-mini': {'input': 0.15/1000000, 'output': 0.6/1000000},
        'llama3-8b-8192': {'input': 0.05/1000000, 'output': 0.08/1000000},
        'llama3-70b-8192': {'input': 0.59/1000000, 'output': 0.79/1000000},
        'claude-3-5-sonnet-20240620': {'input': 3/1000000, 'output': 15/1000000},
        'claude-3-haiku-20240307': {'input': 0.25/1000000, 'output': 1.25/1000000},
    }
    DEFAULT_TOKEN_PRICE: Dict[str, float] = {
        'input': 0.0001,
        'output': 0.0002
    }
    
    # Processing settings
    MAX_CHARS: int = 100000
    CHUNK_SIZE: int = 1000
    DEFAULT_SCREENSHOT_INTERVAL: int = 60
    MAX_SCREENSHOTS_PER_VIDEO: int = 50
    
    # Available modes and sources
    PROCESSING_MODES: List[str] = [mode.value for mode in ProcessingMode]
    CHAPTER_SOURCES: List[str] = [source.value for source in ChapterSource]
    
    # Retry settings
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 1
    RETRY_BACKOFF: float = 1.5
    
    # Cache settings
    CACHE_RETENTION_DAYS: int = 7
    MAX_CACHE_SIZE_MB: int = 1000
    
    # Download settings
    MAX_VIDEO_LENGTH_MINUTES: int = 180
    MAX_DOWNLOAD_SIZE_MB: int = 1000
    
    # System resource limits
    MAX_CONCURRENT_JOBS: int = 5
    MEMORY_LIMIT_MB: int = 2000
    
    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: str = "app.log"
    LOG_FILE_MAX_BYTES: int = 1024 * 1024
    LOG_FILE_BACKUP_COUNT: int = 5
    
    # API Rate Limiting
    RATE_LIMIT_CALLS: int = 100
    RATE_LIMIT_PERIOD: int = 3600  # 1 hour in seconds
    
    # Job Management
    JOB_TIMEOUT_SECONDS: int = 3600  # 1 hour
    JOB_CLEANUP_INTERVAL: int = 86400  # 24 hours
    MAX_QUEUED_JOBS: int = 100
    
    # Error Handling
    MAX_ERROR_RETRIES: int = 3
    ERROR_RETRY_DELAY: int = 5
    CRITICAL_ERROR_NOTIFICATION: bool = True
    
    # Prompts and templates
    SYSTEM_PROMPTS: Dict[str, str] = {
        "transcript": """Process this transcript into clean, well-structured paragraphs.
        Remove verbal tics, add proper punctuation, and organize the content logically.
        Maintain the original meaning and key information.""",
        
        "chapters": """Create a detailed table of contents for this content.
        Each chapter should represent a distinct topic or section.
        Ensure chapter breakpoints align with natural content transitions.""",
        
        "summary": """Generate a concise summary of the key points discussed.
        Focus on main concepts and important details.
        Maintain the technical accuracy of the content."""
    }

    # Video Processing
    VIDEO_FORMATS: List[str] = ["mp4", "webm", "mkv"]
    MAX_VIDEO_RESOLUTION: str = "1080p"
    MIN_VIDEO_LENGTH_SECONDS: int = 30
    TIMESTAMP_FORMAT: str = "%H:%M:%S"
    ENABLE_AUDIO_PROCESSING: bool = True
    
    # Result Management
    RESULT_EXPIRY_DAYS: int = 30
    MAX_STORED_RESULTS: int = 1000
    ENABLE_RESULT_COMPRESSION: bool = True
    
    # Security
    ENABLE_RATE_LIMITING: bool = True
    ENABLE_IP_BLOCKING: bool = True
    MAX_FAILED_ATTEMPTS: int = 5
    BLOCK_DURATION_MINUTES: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # To allow extra fields without validation errors

    @property
    def has_replicate_token(self) -> bool:
        """Check if Replicate API token is configured."""
        return bool(self.REPLICATE_API_TOKEN)

    @property
    def has_openai_key(self) -> bool:
        """Check if OpenAI API key is configured."""
        return bool(self.OPENAI_API_KEY)

    @property
    def required_dirs(self) -> List[str]:
        """List all required directories."""
        return [
            self.CACHE_DIR,
            self.DOWNLOAD_DIR,
            self.UPLOAD_DIR,
            self.OUTPUT_DIR,
            self.SCREENSHOTS_DIR
        ]

    def get_cors_origins(self) -> List[str]:
        """Get CORS origins considering environment."""
        if os.getenv("ENVIRONMENT") == "production":
            # Add production URLs here
            return self.CORS_ORIGINS + ["https://your-production-url.com"]
        return self.CORS_ORIGINS

    def get_token_price(self, model: str) -> Dict[str, float]:
        """Get token prices for specified model."""
        return self.TOKEN_PRICES.get(model, self.DEFAULT_TOKEN_PRICE)

    def validate_directories(self):
        """Validate and create required directories."""
        for directory in self.required_dirs:
            os.makedirs(directory, exist_ok=True)

    def validate(self):
        """Validate settings and environment."""
        if not self.has_openai_key:
            raise ValueError("OpenAI API key is required")
        
        if not self.has_replicate_token and "replicate" in self.MODEL.lower():
            raise ValueError("Replicate API token is required for Replicate models")
        
        self.validate_directories()

# Initialize settings
settings = Settings()

try:
    # Validate settings on import
    settings.validate()
except Exception as e:
    import logging
    logging.error(f"Settings validation failed: {str(e)}")
    raise
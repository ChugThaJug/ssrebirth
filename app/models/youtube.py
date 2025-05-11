# app/models/youtube.py
from typing import List, Dict, Optional
from pydantic import BaseModel, field_validator, ConfigDict
from app.models.base import BaseProcessingResponse, BaseProcessingStatus




class Chapter(BaseModel):
    num_chapter: int
    title: str
    start_paragraph_number: int
    end_paragraph_number: int
    start_time: float
    end_time: float
    paragraphs: List[str]
    paragraph_timestamps: List[float]
    screenshots: Optional[List[str]] = None  # Added screenshots field
    
    model_config = ConfigDict(strict=True)

    @field_validator('start_paragraph_number')
    @classmethod
    def validate_start_paragraph(cls, v: int) -> int:
        if v < 0:
            raise ValueError("start_paragraph_number must be non-negative")
        return v

    @field_validator('end_paragraph_number')
    @classmethod
    def validate_end_paragraph(cls, v: int, info) -> int:
        if info.data.get('start_paragraph_number') is not None and v <= info.data['start_paragraph_number']:
            raise ValueError("end_paragraph_number must be greater than start_paragraph_number")
        return v

    @field_validator('paragraph_timestamps')
    @classmethod
    def validate_timestamps(cls, v: List[float], info) -> List[float]:
        if len(info.data.get('paragraphs', [])) != len(v):
            raise ValueError("Number of timestamps must match number of paragraphs")
        return v

    @field_validator('paragraphs')
    @classmethod
    def validate_paragraphs_not_empty(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("Paragraphs list cannot be empty")
        if any(not p.strip() for p in v):
            raise ValueError("Paragraphs cannot be empty strings")
        return v

    @field_validator('title')
    @classmethod
    def validate_title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

    @field_validator('start_time', 'end_time')
    @classmethod
    def validate_time(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Time values cannot be negative")
        return v

class ProcessingStats(BaseModel):
    total_input_tokens: int
    total_output_tokens: int
    total_price: float
    
    model_config = ConfigDict(strict=True)

    @field_validator('total_input_tokens', 'total_output_tokens')
    @classmethod
    def validate_tokens_positive(cls, v: int) -> int:
        if v < 0:
            raise ValueError("Token counts cannot be negative")
        return v

    @field_validator('total_price')
    @classmethod
    def validate_price(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Price cannot be negative")
        return round(v, 6)

class YouTubeResult(BaseModel):
    video_id: str
    chapters: List[Chapter]
    stats: ProcessingStats
    
    model_config = ConfigDict(strict=True)

    @field_validator('video_id')
    @classmethod
    def validate_video_id(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("video_id cannot be empty")
        return v.strip()

    @field_validator('chapters')
    @classmethod
    def validate_chapters_not_empty(cls, v: List[Chapter]) -> List[Chapter]:
        if not v:
            raise ValueError("Chapters list cannot be empty")
        return v

    def model_dump(self, *args, **kwargs):
        """Override model_dump method to ensure proper serialization."""
        d = super().model_dump(*args, **kwargs)
        d['stats']['total_price'] = float(d['stats']['total_price'])
        return d

class YouTubeProcessingResponse(BaseProcessingResponse):
    video_id: str
    
    model_config = ConfigDict(strict=True)

    @field_validator('video_id')
    @classmethod
    def validate_video_id(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("video_id cannot be empty")
        return v.strip()

class YouTubeProcessingStatus(BaseProcessingStatus):
    video_id: str
    result: Optional[YouTubeResult] = None
    
    model_config = ConfigDict(strict=True)

    @field_validator('video_id')
    @classmethod
    def validate_video_id(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("video_id cannot be empty")
        return v.strip()

    def model_dump(self, *args, **kwargs):
        """Override model_dump method to ensure proper serialization."""
        d = super().model_dump(*args, **kwargs)
        if d['result'] and 'stats' in d['result']:
            d['result']['stats']['total_price'] = float(d['result']['stats']['total_price'])
        return d
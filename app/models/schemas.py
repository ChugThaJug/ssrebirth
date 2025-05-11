# app/models/schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class UserBase(BaseModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

class VideoBase(BaseModel):
    video_id: str
    processing_mode: str
    chapter_source: str

class VideoCreate(VideoBase):
    user_id: int

class Video(VideoBase):
    id: int
    title: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime
    chapters: Optional[Dict] = None
    stats: Optional[Dict] = None
    error: Optional[str] = None

    class Config:
        from_attributes = True

class ProcessingJobBase(BaseModel):
    job_id: str
    video_id: int
    mode: str
    chapter_source: str

class ProcessingJob(ProcessingJobBase):
    id: int
    status: str
    progress: float
    created_at: datetime
    completed_at: Optional[datetime] = None
    error: Optional[str] = None

    class Config:
        from_attributes = True
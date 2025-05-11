# app/api/routes/youtube.py
from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.models.youtube import (
    YouTubeProcessingResponse,
    YouTubeProcessingStatus,
    YouTubeResult
)
from app.services.youtube import YouTubeService, YouTubeProcessingJob
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/youtube", tags=["youtube"])

youtube_service = YouTubeService()

@router.post("/process/{video_id}", response_model=YouTubeProcessingResponse)
async def process_youtube_video(video_id: str, background_tasks: BackgroundTasks):
    """Start processing a YouTube video."""
    job_id = f"yt_job_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{video_id}"
    job = YouTubeProcessingJob(job_id, video_id)
    
    background_tasks.add_task(job.process)
    
    return YouTubeProcessingResponse(
        job_id=job_id,
        video_id=video_id,
        status="processing"
    )

@router.get("/status/{job_id}", response_model=YouTubeProcessingStatus)
async def get_processing_status(job_id: str):
    """Get the status of a processing job."""
    job = YouTubeProcessingJob.load(job_id)
    return YouTubeProcessingStatus(
        job_id=job_id,
        video_id=job.video_id,
        status=job.status,
        progress=job.progress,
        result=job.result,
        error=job.error
    )
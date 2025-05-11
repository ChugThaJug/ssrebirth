from fastapi import APIRouter, BackgroundTasks, HTTPException, Query
from app.services.youtube import (
    YouTubeService,
    YouTubeProcessingJob,
    ProcessingMode,
    ChapterSource
)
from app.models.youtube import (
    YouTubeProcessingResponse,
    YouTubeProcessingStatus,
    YouTubeResult
)
from datetime import datetime
import logging
from typing import Optional

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/youtube", tags=["youtube"])

youtube_service = YouTubeService()

@router.post("/process/{video_id}")
async def process_youtube_video(
    video_id: str,
    background_tasks: BackgroundTasks,
    mode: ProcessingMode = Query(
        ProcessingMode.DETAILED,
        description="Processing mode: simple (fastest), detailed (with chunking), or detailed_with_screenshots"
    ),
    chapter_source: ChapterSource = Query(
        ChapterSource.AUTO,
        description="Source for chapters: auto (generated) or description (from video description)"
    )
):
    """
    Start processing a YouTube video with specified mode and chapter source.
    
    Args:
        video_id: YouTube video ID
        mode: Processing mode (simple, detailed, detailed_with_screenshots)
        chapter_source: Source for chapters (auto or description)
    """
    job_id = f"yt_job_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{video_id}"
    job = YouTubeProcessingJob(job_id, video_id, mode, chapter_source)
    
    background_tasks.add_task(job.process)
    
    return YouTubeProcessingResponse(
        job_id=job_id,
        video_id=video_id,
        status="processing",
        mode=mode,
        chapter_source=chapter_source
    )

@router.get("/status/{job_id}", response_model=YouTubeProcessingStatus)
async def get_processing_status(job_id: str):
    """Get the status of a processing job."""
    try:
        job = YouTubeProcessingJob.load(job_id)
        return YouTubeProcessingStatus(
            job_id=job_id,
            video_id=job.video_id,
            status=job.status,
            progress=job.progress,
            result=job.result,
            error=job.error,
            mode=job.mode,
            chapter_source=job.chapter_source
        )
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Job not found: {str(e)}"
        )

@router.get("/latest-status")
async def get_latest_status(video_id: str):
    """Get the latest processing status for a video."""
    try:
        # Get the most recent job for this video ID
        latest_job = YouTubeProcessingJob.get_latest_for_video(video_id)
        if not latest_job:
            raise HTTPException(
                status_code=404,
                detail="No processing jobs found for this video"
            )
        
        return YouTubeProcessingStatus(
            job_id=latest_job.job_id,
            video_id=latest_job.video_id,
            status=latest_job.status,
            progress=latest_job.progress,
            result=latest_job.result,
            error=latest_job.error,
            mode=latest_job.mode,
            chapter_source=latest_job.chapter_source
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get latest status: {str(e)}"
        )

@router.get("/result/{video_id}", response_model=YouTubeResult)
async def get_video_result(video_id: str):
    """Get the processed result for a video."""
    try:
        result = await YouTubeProcessingJob.get_completed_result(video_id)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get video result: {str(e)}"
        )

@router.get("/chapters/{video_id}")
async def get_video_chapters(video_id: str):
    """Get chapters from video description if available."""
    try:
        chapters = await youtube_service.chapters_service.get_video_chapters(video_id)
        if not chapters:
            raise HTTPException(
                status_code=404,
                detail="No chapters found in video description"
            )
        return {"chapters": chapters}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get chapters: {str(e)}"
        )
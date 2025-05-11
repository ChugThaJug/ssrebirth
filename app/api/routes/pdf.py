# app/api/routes/pdf.py
from fastapi import APIRouter, File, UploadFile, BackgroundTasks, HTTPException
from app.models.pdf import PDFMetadata, ProcessingResponse, ProcessingStatus
from app.services.pdf import PDFService, ProcessingJob
from app.core.settings import settings
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/pdf", tags=["pdf"])

pdf_service = PDFService()

@router.post("/upload/", response_model=ProcessingResponse)
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        logger.info(f"Successfully uploaded file: {file.filename}")
        return ProcessingResponse(
            job_id="upload",
            filename=file.filename,
            status="uploaded",
            processed_file_path=file_path
        )
    except Exception as e:
        logger.error(f"Upload failed for file {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metadata/{filename}", response_model=PDFMetadata)
async def get_metadata(filename: str):
    file_path = os.path.join(settings.UPLOAD_DIR, filename)
    metadata = pdf_service.get_pdf_metadata(file_path)
    return PDFMetadata(**metadata)

@router.post("/process/{filename}", response_model=ProcessingResponse)
async def process_pdf(filename: str, background_tasks: BackgroundTasks):
    job_id = f"job_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
    job = ProcessingJob(job_id, filename)
    
    async def process_wrapper():
        await job.process()
    
    background_tasks.add_task(process_wrapper)

@router.get("/status/{job_id}", response_model=ProcessingStatus)
async def get_status(job_id: str):
    job = ProcessingJob.load(job_id)
    return ProcessingStatus(
        job_id=job_id,
        status=job.status,
        progress=job.progress,
        result_path=job.result_path,
        error=job.error
    )

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model": settings.MODEL,
        "version": settings.APP_VERSION
    }
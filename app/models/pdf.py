# app/models/pdf.py
from pydantic import BaseModel
from typing import Optional, Dict

class PDFMetadata(BaseModel):
    num_pages: int
    metadata: dict

class ProcessingResponse(BaseModel):
    job_id: str
    filename: str
    status: str
    processed_file_path: Optional[str] = None
    error: Optional[str] = None

class ProcessingStatus(BaseModel):
    job_id: str
    status: str
    progress: float
    result_path: Optional[str] = None
    error: Optional[str] = None
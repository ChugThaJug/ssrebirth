# app/models/base.py
from pydantic import BaseModel
from typing import List, Dict, Optional

class BaseProcessingResponse(BaseModel):
    job_id: str
    status: str
    error: Optional[str] = None

class BaseProcessingStatus(BaseModel):
    job_id: str
    status: str
    progress: float
    error: Optional[str] = None
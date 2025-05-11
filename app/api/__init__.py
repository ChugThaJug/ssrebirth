# app/api/__init__.py
from fastapi import APIRouter

# Import routes
from app.api.routes import youtube, pdf

router = APIRouter()



# Include routes
router.include_router(youtube.router)
router.include_router(pdf.router)
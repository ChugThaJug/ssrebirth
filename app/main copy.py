# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.settings import settings
from app.api.routes import youtube, pdf
from app.utils.cache_cleanup import cleanup_old_cache_files
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

def create_application() -> FastAPI:
    """Create and configure FastAPI application."""
    application = FastAPI(
        title=settings.APP_TITLE,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        # Remove the /api prefix from docs URLs
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )

    # CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Modify in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers with prefix
    application.include_router(
        youtube.router,
        prefix="/api/v1",
        tags=["YouTube Processing"]
    )
    application.include_router(
        pdf.router,
        prefix="/api/v1",
        tags=["PDF Processing"]
    )

    return application

app = create_application()

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info("Starting up Video Processing API")
    cleanup_old_cache_files()
    logger.info("Cache cleanup completed")

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint to check API status."""
    return {
        "message": "Video Processing API is running",
        "version": settings.APP_VERSION,
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

# Run with uvicorn if called directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.settings import settings
from app.api.routes import youtube, pdf
from app.utils.cache_cleanup import cleanup_old_cache_files
import logging
from contextlib import asynccontextmanager
import sys

# Add this at the top, before any other imports
import os
from dotenv import load_dotenv
# Try to load from project root
load_dotenv()
# Also try relative path
load_dotenv(".env")
# Debug - print to see if it's loaded
print(f"OPENAI_API_KEY found: {bool(os.getenv('OPENAI_API_KEY'))}")

# Setup logging with more detailed output
logging.basicConfig(
    level=logging.DEBUG,  # Change to DEBUG for more verbose output
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize application on startup."""
    try:
        logger.info("Starting up Video Processing API")
        logger.info("Beginning cache cleanup...")
        cleanup_old_cache_files()
        logger.info("Cache cleanup completed")
        yield
        logger.info("Shutting down Video Processing API")
    except Exception as e:
        logger.error(f"Error during application lifecycle: {str(e)}", exc_info=True)
        sys.exit(1)  # Exit if there's a critical error

def create_application() -> FastAPI:
    """Create and configure FastAPI application."""
    logger.info("Creating FastAPI application")
    application = FastAPI(
        title=settings.APP_TITLE,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan
    )

    logger.info("Configuring middleware")
    # Configure CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_METHODS,
        allow_headers=settings.CORS_HEADERS,
        expose_headers=settings.CORS_EXPOSE_HEADERS
    )
    
    logger.info("Including routers")
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

    logger.info("Application created successfully")
    return application

logger.info("Initializing application object")
app = create_application()

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint to check API status."""
    return {
        "message": "Video Processing API is running",
        "version": settings.APP_VERSION,
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Uvicorn server with minimal configuration")
    try:
        # Use "main:app" instead of "app.main:app"
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=False,
            log_level="debug"
        )
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}", exc_info=True)
        sys.exit(1)
from fastapi import APIRouter, HTTPException, Depends, Query, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
from .utils import get_video_details, get_youtube_transcript, transcript_to_paragraphs, add_timestamps_to_paragraphs, paragraphs_to_toc, get_chapters, get_result_as_html
from openai import AsyncOpenAI
import os
from .database import get_db
from sqlalchemy.orm import Session
from . import crud, schemas
import logging
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from .core.config import settings

router = APIRouter()
templates = Jinja2Templates(directory="templates")
settings = get_settings()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoRequest(BaseModel):
    video_id: str
    llm_model: str = "gpt-4o-mini-2024-07-18"

class VideoResponse(BaseModel):
    html_content: str
    total_tokens: int
    total_price: float

@router.post("/process_video/", response_model=VideoResponse)
async def process_video(request: VideoRequest, db: Session = Depends(get_db)):
    try:
        logger.info(f"Processing video: {request.video_id}")
        
        # Check if video already exists in the database
        existing_video = crud.get_video(db, video_id=request.video_id)
        if existing_video:
            logger.info(f"Video {request.video_id} already exists in database")
            return VideoResponse(
                html_content=existing_video.summary,
                total_tokens=existing_video.total_tokens,
                total_price=existing_video.total_price
            )

        # Initialize OpenAI client
        client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        if not client.api_key:
            raise ValueError("OpenAI API key is not set")

        # Get YouTube video details
        try:
            video_details = await get_video_details(request.video_id)
        except Exception as e:
            logger.error(f"Error getting YouTube video details: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Failed to get YouTube video details: {str(e)}")

        # Get YouTube transcript
        try:
            transcript = await get_youtube_transcript(request.video_id)
        except Exception as e:
            logger.error(f"Error getting YouTube transcript: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Failed to get YouTube transcript: {str(e)}")

        # Process transcript into paragraphs
        try:
            paragraphs, nb_input_tokens1, nb_output_tokens1, price1 = await transcript_to_paragraphs(
                transcript, client, request.llm_model
            )
        except Exception as e:
            logger.error(f"Error processing transcript: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to process transcript: {str(e)}")

        # Add timestamps to paragraphs
        paragraphs_with_timestamps = add_timestamps_to_paragraphs(transcript, paragraphs)

        # Generate table of contents
        try:
            toc, nb_input_tokens2, nb_output_tokens2, price2 = await paragraphs_to_toc(
                paragraphs_with_timestamps, client, request.llm_model
            )
        except Exception as e:
            logger.error(f"Error generating table of contents: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to generate table of contents: {str(e)}")

        # Get chapters
        chapters = get_chapters(paragraphs_with_timestamps, toc)

        # Generate HTML content
        html_content = get_result_as_html(chapters, request.video_id)

        # Calculate total tokens and price
        total_tokens = nb_input_tokens1 + nb_output_tokens1 + nb_input_tokens2 + nb_output_tokens2
        total_price = price1 + price2

        # Save the processed video to the database
        video_data = schemas.VideoCreate(
            video_id=request.video_id,
            title=video_details['title'],
            author=video_details['channel_title'],
            duration=video_details['duration'],
            description=video_details['description'],
            thumbnail_url=video_details['thumbnail_url'],
            summary=html_content,
            total_tokens=total_tokens,
            total_price=total_price
        )
        try:
            crud.create_video(db, video_data)
        except Exception as e:
            logger.error(f"Error saving video to database: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to save video to database: {str(e)}")

        logger.info(f"Successfully processed video: {request.video_id}")
        return VideoResponse(
            html_content=html_content,
            total_tokens=total_tokens,
            total_price=total_price
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing video: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# Home route
@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# # User registration
# @router.post("/register", response_model=schemas.User)
# def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)

# # User login
# @router.post("/token")
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = crud.authenticate_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = crud.create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

# # # User dashboard
# # @router.get("/dashboard", response_class=HTMLResponse)
# # async def dashboard(request: Request, current_user: schemas.User = Depends(crud.get_current_active_user), db: Session = Depends(get_db)):
# #     user_videos = crud.get_user_videos(db, user_id=current_user.id)
# #     return templates.TemplateResponse("dashboard.html", {"request": request, "user": current_user, "videos": user_videos})

# @router.get("/videos/{video_id}")
# async def read_video(request: Request, video_id: str, db: Session = Depends(get_db)):
#     db_video = crud.get_video(db, video_id=video_id)
#     if db_video is None:
#         raise HTTPException(status_code=404, detail="Video not found")
#     return templates.TemplateResponse("video.html", {"request": request, "video": db_video})

# @router.get("/videos", response_model=List[schemas.Video])
# def list_videos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     videos = crud.get_videos(db, skip=skip, limit=limit)
#     return videos

# @router.get("/recent_videos", response_model=List[schemas.Video])
# def get_recent_videos(limit: int = Query(15, gt=0, le=50), db: Session = Depends(get_db)):
#     videos = crud.get_recent_videos(db, limit=limit)
#     return videos

# @router.delete("/videos/{video_id}", response_model=schemas.Video)
# def delete_video(video_id: str, db: Session = Depends(get_db)):
#     db_video = crud.delete_video(db, video_id=video_id)
#     if db_video is None:
#         raise HTTPException(status_code=404, detail="Video not found")
#     return db_video

# @router.put("/videos/{video_id}", response_model=schemas.Video)
# def update_video(video_id: str, video: schemas.VideoUpdate, db: Session = Depends(get_db)):
#     db_video = crud.update_video(db, video_id=video_id, video=video)
#     if db_video is None:
#         raise HTTPException(status_code=404, detail="Video not found")
#     return db_video

# @router.get("/search_videos", response_model=List[schemas.Video])
# def search_videos(
#     query: str,
#     skip: int = 0,
#     limit: int = 10,
#     db: Session = Depends(get_db)
# ):
#     videos = crud.search_videos(db, query=query, skip=skip, limit=limit)
#     return videos

# # Subscription page
# @router.get("/subscribe", response_class=HTMLResponse)
# async def subscribe_page(request: Request, current_user: schemas.User = Depends(crud.get_current_active_user)):
#     return templates.TemplateResponse("subscribe.html", {"request": request, "user": current_user})

# # Subscription success
# @router.get("/subscription/success", response_class=HTMLResponse)
# async def subscription_success(request: Request, current_user: schemas.User = Depends(crud.get_current_active_user)):
#     return templates.TemplateResponse("subscription_success.html", {"request": request, "user": current_user})


# # ... (keep existing code)

# # Login page
# @router.get("/login", response_class=HTMLResponse)
# async def login_page(request: Request):
#     return templates.TemplateResponse("login.html", {"request": request})

# @router.post("/login")
# async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = crud.authenticate_user(db, form_data.username, form_data.password)
#     if not user:
#         return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"}, status_code=400)
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = crud.create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     response = RedirectResponse(url="/dashboard", status_code=303)
#     response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
#     return response

# # Registration page
# @router.get("/register", response_class=HTMLResponse)
# async def register_page(request: Request):
#     return templates.TemplateResponse("register.html", {"request": request})

# @router.post("/register")
# async def register(
#     request: Request,
#     username: str = Form(...),
#     email: str = Form(...),
#     password: str = Form(...),
#     db: Session = Depends(get_db)
# ):
#     db_user = crud.get_user_by_email(db, email=email)
#     if db_user:
#         return templates.TemplateResponse("register.html", {"request": request, "error": "Email already registered"}, status_code=400)
#     user = schemas.UserCreate(username=username, email=email, password=password)
#     crud.create_user(db=db, user=user)
#     return RedirectResponse(url="/login", status_code=303)

# # Pricing page
# @router.get("/pricing", response_class=HTMLResponse)
# async def pricing_page(request: Request):
#     return templates.TemplateResponse("pricing.html", {"request": request})

# # Subscription page (updated)
# @router.get("/subscribe", response_class=HTMLResponse)
# async def subscribe_page(request: Request, current_user: schemas.User = Depends(crud.get_current_user)):
#     if not current_user:
#         return RedirectResponse(url="/login", status_code=303)
#     return templates.TemplateResponse("subscribe.html", {"request": request, "user": current_user})

# # ... (keep existing code)

# # Logout route
# @router.get("/logout")
# async def logout(request: Request):
#     response = RedirectResponse(url="/", status_code=303)
#     response.delete_cookie("access_token")
#     return response

# # ... (keep the rest of the existing routes)
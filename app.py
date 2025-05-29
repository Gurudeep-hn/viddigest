#!/usr/bin/env python3
"""
VidDigest - YouTube Video Summarizer
A modern web application that transforms YouTube videos into concise summaries
"""
import os
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from src.services.youtube import YouTubeService
from src.services.transcript import TranscriptService  
from src.services.summarizer import VideoSummarizer
from config.settings import get_settings

# Initialize settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="VidDigest",
    description="Transform YouTube videos into concise, actionable summaries",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize services
youtube_service = YouTubeService()
transcript_service = TranscriptService()
summarizer = VideoSummarizer()

# Pydantic models
class VideoRequest(BaseModel):
    video_url: str

class VideoResponse(BaseModel):
    video_id: str
    title: str
    duration: str
    views: str
    channel: str
    summary: str
    key_points: List[str]
    timestamps: List[str]

@app.get("/")
async def read_root(request: Request):
    """Serve the main HTML page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/analyze", response_model=VideoResponse)
async def analyze_video(video_request: VideoRequest):
    """Analyze YouTube video and return summary"""
    try:
        # Extract video ID
        video_id = youtube_service.extract_video_id(video_request.video_url)
        if not video_id:
            raise HTTPException(status_code=400, detail="Invalid YouTube URL")
        
        # Get video info and transcript
        video_info = await youtube_service.get_video_info(video_id)
        transcript = await transcript_service.get_transcript(video_id)
        
        if not transcript:
            raise HTTPException(
                status_code=404, 
                detail="No transcript available. Please try a video with captions."
            )
        
        # Generate summary
        summary_result = await summarizer.summarize(transcript, video_info['title'])
        
        return VideoResponse(
            video_id=video_id,
            title=video_info['title'],
            duration=video_info['duration'],
            views=video_info['views'],
            channel=video_info['channel'],
            summary=summary_result['summary'],
            key_points=summary_result['key_points'],
            timestamps=summary_result['timestamps']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "ai_available": summarizer.is_model_loaded()
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=False  # Disable reload in production
    )
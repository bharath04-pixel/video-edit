"""
AI Video Editor Backend API - UPDATED
Main FastAPI application with all endpoints + root path
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
import os
import shutil
import uuid
from dotenv import load_dotenv
import logging
from services.video_processor import VideoProcessor
from services.ai_service import AIService

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "uploads"))
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "outputs"))
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 536870912))  # 500MB
ALLOWED_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}

# Create directories
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Create FastAPI app
app = FastAPI(
    title="AI Video Editor API",
    version="1.0.0",
    description="Professional AI-powered video editing backend",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS Middleware - Allow all origins (restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
video_processor = VideoProcessor()
ai_service = AIService()


# ==================== ROOT ENDPOINTS ====================

@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "AI Video Editor API",
        "version": "1.0.0",
        "status": "online",
        "endpoints": {
            "health": "/health",
            "info": "/info",
            "documentation": "/docs",
            "upload": "POST /api/upload",
            "process": "POST /api/process",
            "export": "POST /api/export",
            "download": "GET /download/{filename}",
            "cleanup": "POST /api/cleanup/{video_id}"
        },
        "react_app": "http://localhost:3000",
        "website": "http://localhost:8001"
    }


@app.get("/api")
async def api_root():
    """API root documentation"""
    return {
        "message": "Welcome to AI Video Editor API",
        "version": "1.0.0",
        "available_endpoints": [
            "/health - System health check",
            "/info - API information",
            "/api/upload - Upload video",
            "/api/process - Process video with AI",
            "/api/export - Export processed video",
            "/download/{filename} - Download output",
            "/api/cleanup/{video_id} - Clean up files"
        ]
    }


# ==================== HEALTH & INFO ====================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "API is running",
        "version": "1.0.0",
        "max_file_size_mb": MAX_FILE_SIZE // (1024 * 1024)
    }


@app.get("/info")
async def get_info():
    """Get API info and usage statistics"""
    upload_count = len(list(UPLOAD_DIR.glob("*")))
    output_count = len(list(OUTPUT_DIR.glob("*")))
    
    return {
        "api_version": "1.0.0",
        "timestamp": str(__import__("datetime").datetime.now()),
        "uploads": upload_count,
        "outputs": output_count
    }


# ==================== VIDEO UPLOAD ====================

@app.post("/api/upload")
async def upload_video(file: UploadFile = File(...)):
    """Upload video file for processing"""
    try:
        if file.size and file.size > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail=f"File too large. Max: {MAX_FILE_SIZE // (1024 * 1024)}MB")
        
        if not any(file.filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
            raise HTTPException(status_code=400, detail=f"Unsupported format. Allowed: {ALLOWED_EXTENSIONS}")
        
        video_id = str(uuid.uuid4())
        file_path = UPLOAD_DIR / f"{video_id}_{file.filename}"
        
        with open(file_path, "wb") as buffer:
            contents = await file.read()
            buffer.write(contents)
        
        logger.info(f"Video uploaded: {video_id}")
        
        return {
            "video_id": video_id,
            "filename": file.filename,
            "size_mb": len(contents) / (1024 * 1024),
            "status": "uploaded"
        }
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== VIDEO PROCESSING ====================

@app.post("/api/process")
async def process_video(video_id: str = Query(...)):
    """Process video with AI features"""
    try:
        video_files = list(UPLOAD_DIR.glob(f"{video_id}_*"))
        if not video_files:
            raise HTTPException(status_code=404, detail="Video not found")
        
        video_path = video_files[0]
        output_path = OUTPUT_DIR / f"processed_{video_id}.mp4"
        
        logger.info(f"Processing video: {video_id}")
        
        # Process video
        video_processor.process(str(video_path), str(output_path))
        
        # AI detections
        detections = {
            "text": ai_service.detect_text(str(video_path)),
            "faces": ai_service.detect_faces(str(video_path)),
            "objects": ai_service.detect_objects(str(video_path))
        }
        
        return {
            "video_id": video_id,
            "status": "processed",
            "output_file": f"processed_{video_id}.mp4",
            "detections": detections
        }
    except Exception as e:
        logger.error(f"Process error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== VIDEO EXPORT ====================

@app.post("/api/export")
async def export_video(video_id: str = Query(...), format: str = Query("mp4")):
    """Export processed video"""
    try:
        output_files = list(OUTPUT_DIR.glob(f"processed_{video_id}*"))
        if not output_files:
            raise HTTPException(status_code=404, detail="Processed video not found")
        
        logger.info(f"Exporting video: {video_id} as {format}")
        
        return {
            "video_id": video_id,
            "format": format,
            "status": "ready_for_download",
            "filename": f"processed_{video_id}.{format}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== FILE DOWNLOAD ====================

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download processed video"""
    try:
        file_path = OUTPUT_DIR / filename
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        logger.info(f"Downloading file: {filename}")
        return FileResponse(str(file_path), media_type="video/mp4")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== CLEANUP ====================

@app.post("/api/cleanup/{video_id}")
async def cleanup_files(video_id: str):
    """Clean up uploaded and processed files"""
    try:
        # Remove uploaded files
        for file in UPLOAD_DIR.glob(f"{video_id}_*"):
            file.unlink()
        
        # Remove processed files
        for file in OUTPUT_DIR.glob(f"{video_id}_*"):
            file.unlink()
        
        logger.info(f"Cleaned up files for video: {video_id}")
        
        return {
            "video_id": video_id,
            "status": "cleaned"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

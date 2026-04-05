"""
AI Video Editor Backend API
Main FastAPI application with all endpoints
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
    description="Professional AI-powered video editing backend"
)

# CORS Middleware - Allow all origins (restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for downloads
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")
app.mount("/outputs", StaticFiles(directory=str(OUTPUT_DIR)), name="outputs")

# Initialize services
video_processor = VideoProcessor()
ai_service = AIService()

# ============================================================================
# HEALTH & INFO ENDPOINTS
# ============================================================================
# ROOT ENDPOINTS
# ============================================================================

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
        }
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


# ============================================================================
# HEALTH & INFO ENDPOINTS
# ============================================================================

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
async def api_info():
    """API information endpoint"""
    upload_count = len(list(UPLOAD_DIR.glob("*")))
    output_count = len(list(OUTPUT_DIR.glob("*")))
    
    return {
        "api_version": "1.0.0",
        "timestamp": str(__import__('datetime').datetime.now()),
        "uploads": upload_count,
        "outputs": output_count,
        "max_file_size_mb": MAX_FILE_SIZE // (1024 * 1024)
    }

# ============================================================================
# UPLOAD ENDPOINT
# ============================================================================

@app.post("/api/upload")
async def upload_video(file: UploadFile = File(...)):
    """
    Upload a video file
    
    Args:
        file: Video file to upload
    
    Returns:
        {
            "id": "unique_id",
            "filename": "filename.mp4",
            "filepath": "/path/to/file",
            "file_size": 1024000,
            "format": ".mp4"
        }
    """
    try:
        # Validate filename
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        # Check file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type {file_ext} not allowed. Allowed: {ALLOWED_EXTENSIONS}"
            )
        
        # Generate unique ID for video
        video_id = str(uuid.uuid4())
        
        # Create filename with unique ID
        original_name = Path(file.filename).stem
        output_filename = f"{video_id}_{original_name}{file_ext}"
        output_path = UPLOAD_DIR / output_filename
        
        # Save file
        contents = await file.read()
        
        # Check file size
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File size exceeds limit of {MAX_FILE_SIZE / (1024*1024):.0f}MB"
            )
        
        with open(output_path, "wb") as f:
            f.write(contents)
        
        logger.info(f"✓ Video uploaded: {video_id}")
        
        return {
            "status": "success",
            "id": video_id,
            "filename": output_filename,
            "filepath": str(output_path),
            "file_size": len(contents),
            "format": file_ext
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Upload error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

# ============================================================================
# PROCESSING ENDPOINTS
# ============================================================================

@app.post("/api/process")
async def process_video(
    video_id: str = Query(...),
    operation: str = Query(...)
):
    """
    Process video with specified operation
    
    Supported operations:
    - text_detection: Detect text in video frames
    - person_detection: Detect people in video frames
    - extract_metadata: Get video metadata
    
    Args:
        video_id: Unique ID from upload
        operation: Processing operation
    
    Returns:
        Operation-specific results
    """
    try:
        # Find the video file
        video_files = list(UPLOAD_DIR.glob(f"{video_id}_*"))
        if not video_files:
            raise HTTPException(status_code=404, detail="Video not found")
        
        video_path = video_files[0]
        logger.info(f"Processing video {video_id} with operation: {operation}")
        
        # Text Detection
        if operation == "text_detection":
            results = await ai_service.detect_text_in_video(str(video_path))
            return {
                "status": "success",
                "operation": "text_detection",
                "video_id": video_id,
                "results": results,
                "frame_count": len(results.get("frames", []))
            }
        
        # Person Detection
        elif operation == "person_detection":
            results = await ai_service.detect_persons_in_video(str(video_path))
            return {
                "status": "success",
                "operation": "person_detection",
                "video_id": video_id,
                "results": results,
                "person_count": len(results.get("people", []))
            }
        
        # Extract Metadata
        elif operation == "extract_metadata":
            metadata = video_processor.get_metadata(str(video_path))
            return {
                "status": "success",
                "operation": "extract_metadata",
                "video_id": video_id,
                "metadata": metadata
            }
        
        else:
            raise HTTPException(status_code=400, detail=f"Unknown operation: {operation}")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Processing error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

# ============================================================================
# EXPORT ENDPOINT
# ============================================================================

@app.post("/api/export")
async def export_video(video_id: str = Query(...)):
    """
    Export/finalize processed video
    
    Args:
        video_id: Unique ID from upload
    
    Returns:
        {
            "status": "success",
            "download_url": "/download/filename.mp4"
        }
    """
    try:
        # Find output file
        video_files = list(UPLOAD_DIR.glob(f"{video_id}_*"))
        if not video_files:
            raise HTTPException(status_code=404, detail="Video not found")
        
        video_path = video_files[0]
        output_filename = video_path.name.replace(f"{video_id}_", "")
        
        return {
            "status": "success",
            "video_id": video_id,
            "download_url": f"/download/{output_filename}",
            "output_path": f"/outputs/{output_filename}"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Export error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

# ============================================================================
# DOWNLOAD ENDPOINT
# ============================================================================

@app.get("/download/{filename}")
async def download_video(filename: str):
    """
    Download processed video file
    
    Args:
        filename: Name of file to download
    
    Returns:
        Video file as attachment
    """
    try:
        # Check both output and upload directories
        file_path = OUTPUT_DIR / filename
        if not file_path.exists():
            file_path = UPLOAD_DIR / filename
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(
            file_path,
            media_type="video/mp4",
            filename=filename
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Download error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")

# ============================================================================
# CLEANUP ENDPOINT
# ============================================================================

@app.post("/api/cleanup/{video_id}")
async def cleanup_video(video_id: str):
    """
    Clean up temporary files for a video
    
    Args:
        video_id: Video ID to cleanup
    
    Returns:
        Confirmation of cleanup
    """
    try:
        # Delete upload file
        upload_files = list(UPLOAD_DIR.glob(f"{video_id}_*"))
        for f in upload_files:
            f.unlink()
        
        # Delete output files
        output_files = list(OUTPUT_DIR.glob(f"*{video_id}*"))
        for f in output_files:
            f.unlink()
        
        logger.info(f"✓ Cleanup complete for video: {video_id}")
        
        return {
            "status": "success",
            "message": "Cleanup complete"
        }
    
    except Exception as e:
        logger.error(f"✗ Cleanup error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Cleanup failed: {str(e)}")

# ============================================================================
# STARTUP
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

# AI Video Editor - Complete Setup Guide

## Prerequisites

Before starting, ensure you have:

- Python 3.10+ installed
- Node.js 16+ installed
- Flutter 3.0+ installed
- Git installed
- FFmpeg installed
- Docker (optional, for containerized deployment)

## Quick Start (5 minutes)

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
# Edit .env and add your API keys:
# GOOGLE_VISION_API_KEY=your_key_here
# REMOVEBG_API_KEY=your_key_here

# Start backend server
python app/main.py
```

Backend will be available at: http://localhost:8000
API documentation: http://localhost:8000/docs

### 2. Frontend Setup

```bash
# Navigate to frontend (in a new terminal)
cd frontend

# Get Flutter dependencies
flutter pub get

# Run on device/emulator
flutter run
```

### 3. Test the API

```bash
# In a new terminal, navigate to backend
cd backend

# Run test suite
python test_api.py
```

## Architecture Overview

```
┌─────────────────────────────────────────────┐
│        FLUTTER MOBILE APP                   │
│   (Home → Upload → Edit → Preview → Export) │
└────────────────────┬────────────────────────┘
                     │ HTTP REST API
                     ↓
┌─────────────────────────────────────────────┐
│     FASTAPI BACKEND (Python)                │
│   (Upload, Process, Export, Download)       │
└────────────────────┬────────────────────────┘
                     │
        ┌────────────┴────────────┐
        ↓                         ↓
    ┌────────────┐          ┌──────────┐
    │  FFmpeg    │          │ AI APIs  │
    │ (Video Ops)│          │(OpenCV)  │
    └────────────┘          └──────────┘
```

## Features Implemented

### Frontend (Flutter)
- ✅ Home Screen with feature overview
- ✅ Video upload with progress tracking
- ✅ Editor screen with analysis operations
- ✅ Preview screen for video review
- ✅ Material 3 Dark theme design
- ✅ Responsive UI for different screen sizes

### Backend (FastAPI)
- ✅ Video upload endpoint
- ✅ Text detection in videos
- ✅ Person/face detection
- ✅ Metadata extraction
- ✅ Video export functionality
- ✅ CORS enabled for mobile
- ✅ Error handling
- ✅ Logging system

### Video Processing (FFmpeg)
- ✅ Video metadata extraction
- ✅ Frame extraction
- ✅ Text overlay
- ✅ Video resizing
- ✅ Video merging

### AI Integration
- ✅ Face detection using OpenCV
- ✅ Text detection in frames
- ✅ Object detection using edge detection
- ✅ Background removal API integration (optional)

## API Endpoints

### Health Check
```
GET /health
```

### Upload Video
```
POST /api/upload
Content-Type: multipart/form-data

Body:
  file: <video_file>

Response:
{
  "status": "success",
  "id": "unique_video_id",
  "filename": "filename.mp4",
  "file_size": 1024000,
  "format": ".mp4"
}
```

### Process Video
```
POST /api/process?video_id=<id>&operation=<operation>

Operations:
  - text_detection
  - person_detection
  - extract_metadata

Response: Operation-specific results
```

### Export Video
```
POST /api/export?video_id=<id>

Response:
{
  "status": "success",
  "download_url": "/download/filename.mp4"
}
```

### Download Video
```
GET /download/<filename>

Returns: Video file
```

## Testing

Run the test suite:
```bash
cd backend
python test_api.py
```

This will test:
- ✅ Health check
- ✅ API info endpoint
- ✅ Video upload
- ✅ Text detection
- ✅ Person detection
- ✅ Video export
- ✅ Cleanup

## Deployment Options

### Option 1: Docker (Recommended)
```bash
# Build and run
docker-compose up --build

# Backend will be at: http://localhost:8000
```

### Option 2: Cloud Deployment

#### Google Cloud Run
```bash
gcloud run deploy ai-video-editor \
  --source backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Heroku
```bash
heroku login
heroku create your-app-name
git push heroku main
heroku open
```

#### AWS EC2
```bash
# Launch EC2 instance with Ubuntu 20.04
ssh -i key.pem ubuntu@your-instance-ip

# Install dependencies
sudo apt update
sudo apt install python3.10 python3-pip ffmpeg

# Clone and setup
git clone your-repo
cd backend
pip install -r requirements.txt
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app
```

### Option 3: Traditional VPS
```bash
# SSH into your server
ssh user@your-vps-ip

# Install Python, Node, Flutter
python3 --version
node --version
flutter --version

# Install system dependencies
sudo apt install ffmpeg

# Setup backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app &

# Or with systemd for auto-restart
sudo nano /etc/systemd/system/ai-editor.service
# Add service configuration from deployment guide
```

## Building APK for Android

```bash
cd frontend

# Debug APK
flutter build apk --debug

# Release APK
flutter build apk --release

# Output: build/app/outputs/flutter-app.apk
```

## Environment Variables

Create `.env` file in backend directory:

```env
# API Configuration
ENVIRONMENT=development
DEBUG=true

# File Upload
UPLOAD_DIR=uploads
OUTPUT_DIR=outputs
MAX_FILE_SIZE=536870912  # 500MB

# API Keys
GOOGLE_VISION_API_KEY=your_api_key
REMOVEBG_API_KEY=your_api_key

# Server
HOST=0.0.0.0
PORT=8000
WORKERS=4
```

## Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill the process
kill -9 <PID>

# Try again
python app/main.py
```

### FFmpeg not found
```bash
# macOS
brew install ffmpeg

# Windows (Chocolatey)
choco install ffmpeg

# Linux (Ubuntu)
sudo apt install ffmpeg
```

### Flutter can't connect to backend
- Ensure backend is running on localhost:8000
- Check API_BASE_URL in api_service.dart
- Check CORS settings in main.py

### OpenCV errors
```bash
# Reinstall opencv-python
pip uninstall opencv-python
pip install opencv-python==4.8.1.78
```

## Performance Optimization

### Backend
- Use uvicorn with multiple workers: `uvicorn -w 4`
- Enable gzip compression
- Cache API responses
- Use async/await for I/O

### Frontend
- Use `const` constructors
- Implement lazy loading for lists
- Profile with Flutter DevTools
- Use Provider for state management

### Video Processing
- Use appropriate codecs (h264 vs h265)
- Adjust FFmpeg preset: ultrafast, fast, medium, slow
- Limit frame processing
- Use lower resolution for preview

## Getting Help

### Documentation Links
- FastAPI: https://fastapi.tiangolo.com
- Flutter: https://flutter.dev/docs
- FFmpeg: https://ffmpeg.org/ffmpeg.html
- OpenCV: https://docs.opencv.org

### Common Issues
Check backend logs:
```bash
tail -f backend/app.log
```

Check Flutter output:
```bash
flutter run -v
```

## Project Structure

```
ai-video-editor/
├── frontend/                 # Flutter mobile app
│   ├── lib/
│   │   ├── main.dart        # App entry point
│   │   ├── screens/         # UI screens
│   │   ├── services/        # API communication
│   │   └── models/          # Data models
│   ├── pubspec.yaml         # Flutter dependencies
│   └── android/             # Android-specific config
│
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── main.py          # FastAPI app
│   │   ├── services/        # Business logic
│   │   └── config.py        # Configuration
│   ├── requirements.txt      # Python dependencies
│   ├── .env                 # Environment variables
│   └── Dockerfile           # Container config
│
└── docker-compose.yml       # Multi-container orchestration
```

## Next Steps

1. **Customize Features**: Modify VideoProcessor and AIService for your needs
2. **Add Authentication**: Implement JWT or OAuth if needed
3. **Database**: Add PostgreSQL for user management
4. **Caching**: Add Redis for improved performance
5. **Monitoring**: Integrate logs with cloud services
6. **CI/CD**: Setup GitHub Actions for automated testing

Happy coding! 🚀

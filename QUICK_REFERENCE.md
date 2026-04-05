# AI VIDEO EDITOR - QUICK REFERENCE GUIDE

## QUICK COMMANDS CHEAT SHEET

### Backend Commands

```bash
# Navigate to backend
cd backend

# Activate virtual environment (macOS/Linux)
source venv/bin/activate

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add new package
pip install package-name

# Start development server
python app/main.py

# Start production server
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app

# View API documentation
# Then visit: http://localhost:8000/docs

# Check Python version
python --version

# Deactivate virtual environment
deactivate
```

### Flutter Commands

```bash
# Navigate to frontend
cd frontend

# Get dependencies
flutter pub get

# Run on connected device/emulator
flutter run

# Run on specific device
flutter run -d <device_id>

# List connected devices
flutter devices

# Clean build
flutter clean

# Get all dependencies (fresh install)
flutter pub get

# Update dependencies
flutter pub upgrade

# Format code
flutter format lib/

# Analyze code for issues
flutter analyze

# Build APK (debug)
flutter build apk --debug

# Build APK (release)
flutter build apk --release

# Build iOS app
flutter build ios --release
```

### FFmpeg Commands

```bash
# Check FFmpeg version
ffmpeg -version

# Add text overlay
ffmpeg -i input.mp4 \
  -vf "drawtext=text='Hello':fontsize=24:fontcolor=white:x=(w-text_w)/2:y=h-100" \
  -c:v libx264 -preset fast -c:a aac output.mp4

# Replace image in video
ffmpeg -i video.mp4 -i image.jpg \
  -filter_complex "[1:v]scale=640:480[img];[0:v][img]overlay=100:100" \
  -c:a aac output.mp4

# Extract frames
ffmpeg -i input.mp4 -vf fps=1 frame_%04d.jpg

# Extract specific frame
ffmpeg -i input.mp4 -ss 00:00:05 -vframes 1 frame.jpg

# Merge multiple videos
ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.mp4

# Resize video
ffmpeg -i input.mp4 -vf scale=1280:720 output.mp4

# Get video information
ffprobe -v error -show_entries format=duration:stream=width,height input.mp4

# Convert to different codec
ffmpeg -i input.mp4 -c:v libx265 -c:a aac output.mp4
```

### Git Commands

```bash
# Initialize repository
git init

# Configure user
git config user.name "Your Name"
git config user.email "your@email.com"

# Check status
git status

# Add all changes
git add .

# Commit changes
git commit -m "Commit message"

# Push to remote
git push origin main

# Create new branch
git checkout -b branch-name

# Switch branch
git checkout branch-name

# View commit history
git log --oneline

# View changes
git diff
```

---

## API ENDPOINTS REFERENCE

### Base URL
```
http://localhost:8000/api
```

### Health Check
```
GET /health
Response: { "status": "ok", "message": "API is running" }
```

### Upload Video
```
POST /api/upload
Content-Type: multipart/form-data

Parameters:
- file: [video file]

Response:
{
  "status": "success",
  "video_id": "abc123",
  "filename": "abc123_video.mp4",
  "size": 52428800,
  "format": ".mp4"
}

Example with curl:
curl -X POST http://localhost:8000/api/upload \
  -F "file=@video.mp4"
```

### Process Video - Text Detection
```
POST /api/process
Content-Type: application/json

Parameters:
{
  "video_id": "abc123",
  "operation": "text_detection"
}

Response:
{
  "status": "success",
  "operation": "text_detection",
  "detected_texts": [
    {
      "text": "Hello World",
      "confidence": 0.95,
      "bounds": [...]
    }
  ],
  "frame_count": 3
}

Example with curl:
curl -X POST "http://localhost:8000/api/process?video_id=abc123&operation=text_detection"
```

### Process Video - Person Detection
```
POST /api/process
Parameters:
{
  "video_id": "abc123",
  "operation": "person_detection"
}

Response:
{
  "status": "success",
  "operation": "person_detection",
  "persons_detected": 1,
  "positions": [
    {
      "x": 100,
      "y": 50,
      "width": 300,
      "height": 400,
      "confidence": 0.95
    }
  ]
}
```

### Process Video - Add Text
```
POST /api/process
Parameters:
{
  "video_id": "abc123",
  "operation": "add_text",
  "params": {
    "text": "Your text here"
  }
}

Response:
{
  "status": "success",
  "operation": "add_text",
  "output_path": "/outputs/text_abc123.mp4"
}
```

### Export Video
```
POST /api/export
Parameters:
{
  "video_id": "abc123"
}

Response:
{
  "status": "success",
  "download_url": "/outputs/text_abc123.mp4",
  "filename": "text_abc123.mp4"
}

Example with curl:
curl -X POST "http://localhost:8000/api/export?video_id=abc123"
```

### Download Video
```
GET /download/{filename}
Returns: Video file

Example:
http://localhost:8000/download/text_abc123.mp4
```

### Cleanup
```
POST /api/cleanup/{video_id}
Deletes temporary files

Response:
{
  "status": "success",
  "message": "Cleanup complete"
}
```

---

## TESTING WITH POSTMAN

### 1. Test Health Check
- Method: GET
- URL: http://localhost:8000/health
- Send and verify response

### 2. Test Upload
- Method: POST
- URL: http://localhost:8000/api/upload
- Go to Body → form-data
- Add key "file" (type: File)
- Select video file
- Send

### 3. Test Processing
- Copy video_id from upload response
- Method: POST
- URL: http://localhost:8000/api/process?video_id=YOUR_ID&operation=text_detection
- Send

### 4. Test Export
- Method: POST
- URL: http://localhost:8000/api/export?video_id=YOUR_ID
- Send and get download_url

---

## ENVIRONMENT VARIABLES

### Backend (.env)
```
# API Configuration
UPLOAD_DIR=uploads
OUTPUT_DIR=outputs
MAX_FILE_SIZE=536870912

# Google Vision API
GOOGLE_VISION_API_KEY=your_api_key

# remove.bg API
REMOVEBG_API_KEY=your_api_key

# Server
ENVIRONMENT=development
DEBUG=true
```

### Flutter (Not needed, but for future cloud URLs)
```dart
const String API_BASE_URL = 'http://localhost:8000/api';
const String API_TIMEOUT = '30';
```

---

## FILE STRUCTURE QUICK REFERENCE

```
ai-video-editor/
├── backend/
│   ├── app/
│   │   ├── main.py (FastAPI app)
│   │   ├── services/
│   │   │   ├── video_processor.py (FFmpeg wrapper)
│   │   │   └── ai_service.py (AI integrations)
│   │   └── api/ (endpoints)
│   ├── requirements.txt
│   ├── .env
│   └── venv/ (virtual environment)
├── frontend/
│   ├── lib/
│   │   ├── main.dart
│   │   ├── screens/
│   │   ├── services/
│   │   └── models/
│   ├── pubspec.yaml
│   └── android/ (APK build config)
└── shared/
    └── constants & types
```

---

## DEBUGGING TIPS

### Backend Debugging

```python
# Add debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Log important events
logger.info("Processing started")
logger.error("Error occurred", exc_info=True)
logger.debug("Debug information")

# Test FFmpeg directly
import subprocess
result = subprocess.run(["ffmpeg", "-version"], capture_output=True)
print(result.stdout.decode())
```

### Flutter Debugging

```dart
// Print statements
print("Debug message: $variable");
debugPrint("Debug: $value");

// Check widget tree
// Use Flutter Inspector in VS Code / Android Studio

// Check network traffic
// Use Network tab in Chrome DevTools
// Or use Dio interceptor:
_dio.interceptors.add(LoggingInterceptor());
```

### Common Issues & Quick Fixes

| Issue | Quick Fix |
|-------|-----------|
| Port 8000 in use | `lsof -ti:8000 \| xargs kill -9` |
| Virtual env not activating | Check path, use full path to activate |
| FFmpeg command not found | Add to PATH or use full path |
| Flutter hot reload not working | Run `flutter clean` then `flutter run` |
| CORS errors | Check CORSMiddleware in main.py |
| API timeout | Increase timeout or use async jobs |

---

## PERFORMANCE TIPS

### Backend Optimization
- Use `uvicorn` with multiple workers: `uvicorn app.main:app -w 4`
- Enable gzip compression for responses
- Cache FFmpeg operations results
- Use async/await for I/O operations
- Monitor with: `htop` or `top`

### Flutter Optimization
- Use `const` constructors
- Implement proper state management
- Lazy load widgets with `ListView.builder`
- Profile with DevTools: `flutter run --profile`

### Video Processing Optimization
- Use appropriate video codec (h264 vs h265)
- Adjust preset (ultrafast, fast, medium, slow)
- Limit frame extraction to necessary frames
- Use lower resolution for preview, high for export

---

## DEPLOYMENT QUICK REFERENCE

### Docker Deployment
```bash
# Build image
docker build -t ai-video-editor .

# Run container
docker run -p 8000:8000 ai-video-editor

# Check logs
docker logs container_id
```

### Cloud Deployment (Google Cloud Run)
```bash
gcloud run deploy ai-video-editor \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

### VPS Deployment (Ubuntu)
```bash
# Install Python and dependencies
sudo apt install python3-pip ffmpeg

# Clone code, setup venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app

# Setup systemd service (for auto-restart)
# Create /etc/systemd/system/ai-editor.service
```

---

## USEFUL LINKS

- Flutter Documentation: https://flutter.dev/docs
- FastAPI: https://fastapi.tiangolo.com
- FFmpeg Filters: https://ffmpeg.org/ffmpeg-filters.html
- Google Vision API: https://cloud.google.com/vision/docs
- remove.bg API: https://remove.bg/api
- Dart Language: https://dart.dev
- Python: https://python.org

---

## QUICK START (30 MINUTES)

1. **Backend** (10 min):
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python app/main.py
   ```

2. **Test API** (5 min):
   - Visit http://localhost:8000/docs
   - Try uploading a video

3. **Frontend** (15 min):
   ```bash
   cd frontend
   flutter pub get
   flutter run
   ```

Done! You have a working app!

---

## TROUBLESHOOTING CHECKLIST

- [ ] Backend server running? (`http://localhost:8000/health`)
- [ ] Frontend can connect? (Check network tab in DevTools)
- [ ] FFmpeg installed? (`ffmpeg -version`)
- [ ] Python virtual env activated? (`which python`)
- [ ] All dependencies installed? (`pip list`)
- [ ] API keys in .env? (Check file exists)
- [ ] Correct paths in code? (Check absolute/relative paths)
- [ ] Firewall blocking? (Check ports 8000, 8080)

---

## GETTING HELP

1. **Read the error message carefully** - it usually tells you what's wrong
2. **Check the guide** - Section matches your issue?
3. **Google the error** - Most errors have been solved before
4. **Check logs** - Add logging to pinpoint issue
5. **Isolate the problem** - Test components separately
6. **Ask in communities** - Stack Overflow, Reddit r/learnprogramming

---

This is your quick reference. Bookmark it! 🚀

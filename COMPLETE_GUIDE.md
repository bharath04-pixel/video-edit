# Complete Implementation Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Local Development](#local-development)
3. [API Usage](#api-usage)
4. [Advanced Features](#advanced-features)
5. [Deployment](#deployment)
6. [Troubleshooting](#troubleshooting)
7. [Performance Tuning](#performance-tuning)
8. [Security](#security)

---

## Getting Started

### Prerequisites

Before starting, ensure you have:

```bash
# Check versions
python --version      # Python 3.10+
ffmpeg -version       # Latest
flutter --version     # Flutter 3.0+
```

### 5-Minute Quick Start

```bash
# 1. Run automatic setup
python setup_backend.py

# 2. Start backend (opens in browser)
python setup_backend.py --start

# 3. In new terminal, run frontend
cd frontend
flutter run

# 4. In another terminal, test API
cd backend
python test_api.py
```

---

## Local Development

### Backend Development

```bash
# Activate environment
cd backend
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install in development mode
pip install -e .

# Run with auto-reload
python app/main.py

# Or use uvicorn directly
uvicorn app.main:app --reload --port 8000
```

### Frontend Development

```bash
cd frontend

# Hot reload
flutter run -v

# Device list
flutter devices

# Run on specific device
flutter run -d <device-id>

# Profiling
flutter run --profile
```

### Database Operations

```bash
# Initialize database
python database.py

# View logs
tail -f logs/api.log

# Clear cache
redis-cli FLUSHALL  # If using Redis
```

---

## API Usage

### Authentication (Optional)

```python
# Get JWT token
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"pass"}'

# Response
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}

# Use in requests
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/protected
```

### Upload Video

```python
import requests

with open("video.mp4", "rb") as f:
    files = {"file": f}
    response = requests.post(
        "http://localhost:8000/api/upload",
        files=files
    )
    
print(response.json())
# {
#   "status": "success",
#   "id": "abc-123",
#   "filename": "video.mp4",
#   "file_size": 1024000
# }
```

### Process Video

```python
# Text detection
response = requests.post(
    "http://localhost:8000/api/process",
    params={
        "video_id": "abc-123",
        "operation": "text_detection"
    }
)

# Person detection
response = requests.post(
    "http://localhost:8000/api/process",
    params={
        "video_id": "abc-123",
        "operation": "person_detection"
    }
)

# Get metadata
response = requests.post(
    "http://localhost:8000/api/process",
    params={
        "video_id": "abc-123",
        "operation": "extract_metadata"
    }
)
```

### Export and Download

```python
# Export video
export_response = requests.post(
    "http://localhost:8000/api/export",
    params={"video_id": "abc-123"}
)

download_url = export_response.json()["download_url"]

# Download file
download_response = requests.get(
    f"http://localhost:8000{download_url}"
)

with open("processed_video.mp4", "wb") as f:
    f.write(download_response.content)
```

---

## Advanced Features

### Rate Limiting

```python
# Enable in advanced_features.py
from advanced_features import RateLimiter

limiter = RateLimiter(requests_per_minute=100)

@app.middleware("http")
async def rate_limit_middleware(request, call_next):
    client_id = request.client.host
    if not limiter.is_allowed(client_id):
        return JSONResponse({"detail": "Rate limit exceeded"}, status_code=429)
    return await call_next(request)
```

### Caching

```python
from advanced_features import SimpleCache

cache = SimpleCache()

# Cache API responses
@app.get("/stats")
def get_stats():
    cached = cache.get("stats")
    if cached:
        return cached
    
    stats = expensive_operation()
    cache.set("stats", stats, ttl_seconds=3600)
    return stats
```

### Database Integration

```python
from database import User, Video, get_db

# Create user
@app.post("/users")
def create_user(email: str, password: str, db = Depends(get_db)):
    user = User(email=email, hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    return user

# Get user videos
@app.get("/users/{user_id}/videos")
def get_user_videos(user_id: int, db = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    return user.videos
```

---

## Deployment

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Backend: http://localhost:8000
# Docs: http://localhost:8000/docs

# Stop containers
docker-compose down
```

### AWS EC2 Deployment

```bash
# Run deployment script
bash deploy_aws.sh

# Monitor service
sudo systemctl status ai-video-editor

# View logs
journalctl -u ai-video-editor -f
```

### Google Cloud Run

```bash
# Deploy
bash deploy_gcp.sh

# Get service URL
gcloud run services describe ai-video-editor --region us-central1
```

### Heroku

```bash
# Deploy
bash deploy_heroku.sh

# View logs
heroku logs -a your-app-name -t

# Scale dynos
heroku ps:scale web=2
```

---

## Troubleshooting

### Run Diagnostics

```bash
# Comprehensive check
python troubleshoot.py

# Auto-fix issues
python troubleshoot.py --fix
```

### Common Issues

**Backend won't start**
```bash
# Check if port is in use
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>
```

**FFmpeg not found**
```bash
# macOS
brew install ffmpeg

# Windows
choco install ffmpeg

# Linux
sudo apt install ffmpeg
```

**Flutter can't connect **
```dart
// Update API URL in api_service.dart
const String API_BASE_URL = 'http://your-backend:8000/api';

// Check CORS in main.py is enabled
```

**Database error**
```python
# Reset database
rm ai_video_editor.db
python database.py

# Check SQLAlchemy version
pip install --upgrade sqlalchemy
```

---

## Performance Tuning

### Backend Optimization

```python
# Use uvicorn with multiple workers
# In production
gunicorn -w 4 -b 0.0.0.0:8000 \
  -k uvicorn.workers.UvicornWorker \
  app.main:app
```

### Database Optimization

```python
# Add indexes to frequently queried fields
class Video(Base):
    __tablename__ = "videos"
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    created_at = Column(DateTime, index=True)

# Enable query caching
from sqlalchemy.orm import Query
session.query(Video).from_statement(text(...)).caching_ok = True
```

### Video Processing

```python
# Process frames in optimal chunks
BATCH_SIZE = 30  # frames per batch

# Use lower resolution for preview
extract_frames(video, scale=0.5)

# Optimize codec
codec = "libx264"  # fast
preset = "fast"  # faster encoding
```

---

## Security

### Environment Variables

```env
# Never commit sensitive data
GOOGLE_VISION_API_KEY=<secret>
REMOVEBG_API_KEY=<secret>
JWT_SECRET_KEY=<secret>
DATABASE_URL=<secret>
```

### CORS Configuration

```python
# Restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.com",
        "https://app.yourdomain.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### Input Validation

```python
from pydantic import BaseModel, validator

class VideoUpload(BaseModel):
    filename: str
    
    @validator('filename')
    def filename_valid(cls, v):
        if not v.endswith(('.mp4', '.mov', '.avi')):
            raise ValueError('Invalid file type')
        return v
```

### SQL Injection Prevention

```python
# ✅ SAFE: Use ORM
user = db.query(User).filter(User.id == user_id).first()

# ❌ UNSAFE: Raw SQL
user = db.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

---

## Monitoring & Logging

### Application Logs

```bash
# Tail logs
tail -f logs/api.log

# Filter by log level
grep "ERROR" logs/api.log

# Watch in real-time
watch -n 1 "tail -20 logs/api.log"
```

### Health Checks

```bash
# Regular health check
curl http://localhost:8000/health

# Setup monitoring
# In Datadog, New Relic, or similar:
- Monitor /health endpoint every 60 seconds
- Alert if response time > 5 seconds
- Alert if error rate > 5%
```

---

## Next Steps

1. **Add Authentication**: Implement JWT tokens
2. **Database Persistence**: Set up PostgreSQL
3. **Real-time Updates**: Add WebSocket support
4. **Advanced Caching**: Integrate Redis
5. **Background Jobs**: Use Celery for async tasks
6. **Monitoring**: Set up logging to cloud services
7. **CI/CD**: Implement GitHub Actions
8. **Load Balancing**: Add Nginx load balancer

---

## Resources

- FastAPI: https://fastapi.tiangolo.com
- Flutter: https://flutter.dev/docs
- FFmpeg: https://ffmpeg.org
- OpenCV: https://docs.opencv.org
- Docker: https://docs.docker.com
- AWS: https://docs.aws.amazon.com

---

**Status**: ✅ Production Ready
**Last Updated**: 2026-04-05

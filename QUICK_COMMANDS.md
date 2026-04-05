# Quick Command Reference

## 🚀 Quick Start Commands

### One-Command Startup (Recommended)
```bash
python start_all.py
```

### Manual Startup

**Backend**
```bash
cd backend
python setup_backend.py
python setup_backend.py --start
```

**Frontend**
```bash
cd frontend
flutter run
```

**Testing**
```bash
cd backend
python test_api.py
```

---

## 🐳 Docker Commands

```bash
# Build and start
docker-compose up --build

# Stop containers
docker-compose down

# View logs
docker-compose logs -f api

# Rebuild without cache
docker-compose build --no-cache
```

---

## 🔧 Setup & Configuration

```bash
# Automatic setup
python setup_backend.py

# Manual setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file
cp backend/.env.example backend/.env
nano backend/.env  # Edit with API keys
```

---

## 🌐 Deployment

```bash
# AWS EC2
bash deploy_aws.sh

# Google Cloud Run
bash deploy_gcp.sh

# Heroku
bash deploy_heroku.sh
```

---

## 🧪 Testing

```bash
# Run all API tests
python backend/test_api.py

# Run Flutter tests
cd frontend && flutter test

# Run with coverage
pytest backend/tests/ --cov=backend/app
```

---

## 🔍 Troubleshooting

```bash
# Run diagnostics
python troubleshoot.py

# Auto-fix issues
python troubleshoot.py --fix

# Check if port 8000 is available
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows
```

---

## 📚 Viewing Documentation

```bash
# Open API interactive docs (while running)
http://localhost:8000/docs

# View markdown files
cat README.md
cat COMPLETE_GUIDE.md
cat FEATURES_IMPLEMENTATION.md
```

---

## 💻 Flutter Commands

```bash
# Get dependencies
flutter pub get

# Run app
flutter run

# Build APK
flutter build apk --release

# Get device list
flutter devices

# Clean build
flutter clean
```

---

## 📝 File Management

```bash
# Add video to uploads
cp video.mp4 backend/uploads/

# Check uploaded files
ls backend/uploads/

# Clean up temp files
rm -rf backend/uploads/
```

---

## 🔐 Environment Setup

```bash
# View .env file
cat backend/.env

# Edit .env
nano backend/.env  # macOS/Linux
notepad backend/.env  # Windows

# Set environment variable (one-time)
export GOOGLE_VISION_API_KEY="your_key"  # macOS/Linux
set GOOGLE_VISION_API_KEY=your_key  # Windows
```

---

## 📊 Monitoring

```bash
# Check API health
curl http://localhost:8000/health

# Check API info
curl http://localhost:8000/info

# Monitor logs
tail -f backend/logs/api.log

# Watch real-time
watch -n 1 "tail -20 backend/logs/api.log"
```

---

## 🛑 Stopping Services

```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9  # macOS/Linux

# Or find and kill manually
ps aux | grep "main.py"
kill -9 <PID>

# Stop Docker
docker-compose down
```

---

## 📦 Dependency Management

```bash
# Upgrade pip
pip install --upgrade pip

# Install new package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt

# Check for outdated packages
pip list --outdated
```

---

## 🔄 Git Commands

```bash
# Initialize repo
git init

# Add files
git add .

# Commit
git commit -m "Description"

# Push
git push origin main

# Check status
git status

# View logs
git log --oneline
```

---

## 🐛 Debugging

```bash
# Backend debug
export PYTHONUNBUFFERED=1
python -u app/main.py

# Flutter debug
flutter run -v

# Check system resources
top  # macOS/Linux
tasklist  # Windows

# Check open ports
netstat -an | grep LISTEN
```

---

## 🎨 Frontend Development

```bash
# Format code
flutter format lib/

# Analyze code
flutter analyze

# Hot reload (while running)
Press 'r' in terminal

# Hot restart
Press 'R' in terminal

# Full restart
Control+C and flutter run again
```

---

## 📱 APK Building

```bash
cd frontend

# Debug APK
flutter build apk --debug

# Release APK
flutter build apk --release

# Install and run
flutter install

# View APK file
ls build/app/outputs/flutter-app.apk
```

---

## 🌍 API Endpoints Quick Reference

```bash
# Health check
curl http://localhost:8000/health

# API info
curl http://localhost:8000/info

# Upload (with Postman or similar)
POST http://localhost:8000/api/upload

# Process
POST http://localhost:8000/api/process?video_id=ID&operation=text_detection

# Export
POST http://localhost:8000/api/export?video_id=ID

# Download
GET http://localhost:8000/download/filename.mp4

# Cleanup
POST http://localhost:8000/api/cleanup/ID
```

---

## 📥 Installation Commands

```bash
# FFmpeg
brew install ffmpeg  # macOS
choco install ffmpeg  # Windows
sudo apt install ffmpeg  # Linux

# Python packages
pip install -r backend/requirements.txt

# Flutter dependencies
flutter pub get

# System dependencies (Ubuntu)
sudo apt update && sudo apt upgrade
sudo apt install python3.10 ffmpeg git
```

---

## 🔗 Useful Links

```bash
# Open API docs
open http://localhost:8000/docs  # macOS
start http://localhost:8000/docs  # Windows
xdg-open http://localhost:8000/docs  # Linux

# GitHub
git remote add origin https://github.com/username/repo.git

# Docker Hub
docker login
docker push username/ai-video-editor
```

---

## 📊 Performance Commands

```bash
# Profile Flutter
flutter run --profile

# Profile backend
python -m cProfile -s cumulative app/main.py

# Memory usage
ps aux | grep python

# CPU usage
top -p <PID>

# Network statistics
netstat -s
```

---

**Bookmark this file for quick reference!** 📌


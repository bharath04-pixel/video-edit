# 🚀 QUICK START COMMANDS

> Copy-paste these commands to get running in 2 minutes

---

## Windows (PowerShell)

### Start Everything at Once
```powershell
# Run all 3 services with one command
.\start-all-services.bat
```

**Then open in browser:**
- Backend: http://localhost:8000
- React App: http://localhost:3000  
- Website: http://localhost:8001

---

### Or Start Manually

**Terminal 1 - Backend:**
```powershell
cd backend
python app/main.py
# ✅ Backend runs on http://localhost:8000
```

**Terminal 2 - React App:**
```powershell
cd react-app
npm install
npm start
# ✅ React runs on http://localhost:3000
```

**Terminal 3 - Website:**
```powershell
cd website
python -m http.server 8001
# ✅ Website runs on http://localhost:8001
```

---

## Mac/Linux

### Start Everything
```bash
chmod +x start-all-services.sh
./start-all-services.sh
```

### Or Manually
```bash
# Terminal 1
cd backend && python app/main.py

# Terminal 2
cd react-app && npm install && npm start

# Terminal 3
cd website && python -m http.server 8001
```

---

## 🔧 First Time Setup

### Install Node Modules
```bash
cd react-app
npm install
```

### Install FFmpeg (For Full Functionality)
```bash
# Windows
python install_ffmpeg.py

# Mac
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg
```

---

## 📱 Build Android APK

### Windows
```powershell
.\build-apk.bat
```

### Mac/Linux
```bash
chmod +x build-apk.sh
./build-apk.sh
```

**Output:** `mobile-app/android/app/build/outputs/apk/debug/app-debug.apk`

---

## 🌐 Test APIs

### Health Check
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "ok",
  "message": "API is running",
  "version": "1.0.0",
  "max_file_size_mb": 512
}
```

### API Info
```bash
curl http://localhost:8000/
```

### API Docs
Open: **http://localhost:8000/docs**

---

## 🚀 Deploy to Cloud

### AWS
```bash
bash deploy_aws.sh
```

### Google Cloud
```bash
bash deploy_gcp.sh
```

### Heroku
```bash
bash deploy_heroku.sh
```

---

## 🧹 Cleanup & Reset

### Clear Uploaded Files
```bash
rm -rf backend/uploads/*
rm -rf backend/outputs/*
```

### Reset React App
```bash
cd react-app
rm -rf node_modules
npm install
npm start
```

### Stop All Services (Mac/Linux)
```bash
pkill -f "python app/main.py"
pkill -f "npm start"
pkill -f "http.server"
```

---

## ❌ Troubleshooting

### Port 8000 Already in Use
```powershell
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -Ti:8000
kill -9 <PID>
```

### FFmpeg Not Found
```bash
# Install FFmpeg
python install_ffmpeg.py

# Verify
ffmpeg -version
```

### React App Won't Start
```bash
cd react-app
rm -rf node_modules package-lock.json
npm install  
npm start
```

### APK Build Fails
```bash
# Check Java version (need 11+)
java -version

# Clean rebuild
cd mobile-app/android
gradlew clean
gradlew assembleDebug
```

---

## 📊 Architecture at a Glance

```
┌─────────────────────────────────────────────┐
│   React Web App (localhost:3000)            │
│   - Upload Videos                           │
│   - Edit with AI                            │
│   - Download Results                        │
└──────────────────┬──────────────────────────┘
                   │
                   │ HTTP/REST
                   │
┌──────────────────▼──────────────────────────┐
│   FastAPI Backend (localhost:8000)          │
│   - Video Upload Handler                    │
│   - AI Processing Engine                    │
│   - File Management                         │
│   - FFmpeg Integration                      │
└──────────────────┬──────────────────────────┘
                   │
         ┌─────────┴──────────┐
         │                    │
      ┌──▼──┐         ┌──────▼───┐
      │Upload│         │Processing│
      │Files │         │Outputs   │
      └──────┘         └──────────┘

┌─────────────────────────────────────────────┐
│   Website (localhost:8001)                  │
│   - Landing Page                            │
│   - Features Showcase                       │
│   - Pricing Info                            │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│   Mobile App (Android APK)                  │
│   - React Native                            │
│   - Same API Backend                        │
│   - Native Controls                         │
└─────────────────────────────────────────────┘
```

---

## 📈 Performance Tips

1. **Enable Caching**
   - API responses cache for 5 minutes
   - Browser cache for static files (1 hour)

2. **Optimize Video Upload**
   - Convert to H.264 beforehand
   - Use 1080p resolution max
   - Compress audio to 128kbps

3. **Scale Backend**
   - Use load balancer (Nginx)
   - Deploy multiple instances
   - Use CDN for downloads

4. **Monitor Performance**
   - Check `logs/api.log`
   - Monitor CPU/Memory usage
   - Track API response times

---

## 📚 Full Documentation

- [COMPLETE_SETUP_GUIDE.md](COMPLETE_SETUP_GUIDE.md) → Detailed setup
- [README_COMPLETE.md](README_COMPLETE.md) → Full overview
- [ARCHITECTURE_GUIDE.md](ARCHITECTURE_GUIDE.md) → System design
- [GETTING_STARTED.md](GETTING_STARTED.md) → Beginner guide

---

## 🎯 Checklist

After setup, verify:
- [ ] Backend running on 8000
- [ ] React App running on 3000
- [ ] Website running on 8001
- [ ] Can upload video in React App
- [ ] API docs accessible at /docs
- [ ] Video processing works (if FFmpeg installed)

---

## 💾 Environment Variables

`.env` file for backend:
```env
UPLOAD_DIR=uploads
OUTPUT_DIR=outputs
MAX_FILE_SIZE=536870912
DEBUG=True
API_PORT=8000
```

---

**Ready to go? Run:** `start-all-services.bat` (Windows) or `./start-all-services.sh` (Mac/Linux)

✅ Everything is now configured and ready to use!

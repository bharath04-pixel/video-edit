# 📦 Complete Setup & Deployment Guide

**AI Video Editor - React App, Website, Website & APK**

>  **Last Updated:** April 5, 2026
>  **Status:** ✅ PRODUCTION READY

---

## 🚀 Quick Start (5 minutes)

### Prerequisites
- Node.js 16+
- Python 3.8+
- NPM or Yarn

### 1️⃣ Start Backend API
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
python app/main_updated.py
```
✅ Backend runs on `http://localhost:8000`

### 2️⃣ Start React App
```bash
cd react-app
npm install
npm start
```
✅ React app runs on `http://localhost:3000`

### 3️⃣ Start Website
```bash
# Option 1: Live Server (VS Code)
# Right-click website\index.html → Open with Live Server

# Option 2: Python Server
cd website
python -m http.server 8001
```
✅ Website runs on `http://localhost:8001`

---

## 📦 Component Breakdown

### Backend API (`port 8000`)
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | API root info |
| `/api` | GET | API documentation |
| `/health` | GET | System health check |
| `/info` | GET | API statistics |
| `/api/upload` | POST | Upload video |
| `/api/process` | POST | Process video with AI |
| `/api/export` | POST | Export video |
| `/download/{file}` | GET | Download processed video |
| `/api/cleanup/{id}` | POST | Clean up files |

**Features:**
- FastAPI framework
- CORS enabled
- File upload handling (500MB max)
- Video processing with FFmpeg
- AI detection (text, faces, objects)
- Comprehensive logging

**Documentation:** `http://localhost:8000/docs` (Swagger UI)

---

### React Web App (`port 3000`)
**Pages:**
- 🏠 **Home** - Landing page with features
- 📤 **Upload** - Drag-and-drop file upload
- ✏️ **Editor** - Video editing interface
- ✅ **Results** - Processing results & export

**Features:**
- Material-UI components
- Video preview
- AI feature toggles
- Brightness/contrast/saturation adjustment
- Progress tracking
- Download support

**Start:**
```bash
cd react-app
npm install
npm start
```

---

### Website (`port 8001`)
**Pages:**
- 🎬 Hero section with CTA
- ✨ Features showcase
- 🚀 How it works
- 💰 Pricing
- 🏗️ Tech stack
- 📞 Contact/Footer

**Features:**
- Responsive design
- No dependencies (pure HTML/CSS)
- Performance optimized
- SEO friendly

**Start:**
```bash
cd website
python -m http.server 8001
# or use Live Server in VS Code
```

---

### Mobile App (APK)
**Technology:** React Native
**Target:** Android 5.0+ (API 21+)
**Build:** Gradle

**Files:**
- `mobile-app/app.json` - App configuration
- `mobile-app/android/` - Android project
- `build-apk.sh` - Linux/Mac build script
- `build-apk.bat` - Windows build script

---

## 🛠️ Installation Guides

### Install FFmpeg (Required for Video Processing)

**Windows:**
```bash
python install_ffmpeg.py
# or manual: https://ffmpeg.org/download.html
```

**Mac:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

---

### Build Android APK

**Prerequisites:**
```bash
# Install Java Development Kit (JDK 11+)
# Install Android Studio
# Set ANDROID_HOME environment variable
```

**Build:**
```bash
# Windows
build-apk.bat

# Mac/Linux
chmod +x build-apk.sh
./build-apk.sh
```

**Output:**
- Debug APK: `mobile-app/android/app/build/outputs/apk/debug/app-debug.apk`
- Release APK: `mobile-app/android/app/build/outputs/apk/release/app-release.apk`
- App Bundle: `mobile-app/android/app/build/outputs/bundle/release/app-release.aab`

**Install APK:**
```bash
adb install mobile-app/android/app/build/outputs/apk/debug/app-debug.apk
```

---

## 🌐 Deployment

### Deploy Backend (AWS)
```bash
bash deploy_aws.sh
```
- Creates EC2 instance
- Configures Nginx
- Sets up SSL
- Deploys with systemd

### Deploy Backend (Google Cloud)
```bash
bash deploy_gcp.sh
```
- Creates Cloud Run service
- Auto-scales based on demand
- Integrates with Cloud Storage

### Deploy Backend (Heroku)
```bash
bash deploy_heroku.sh
```
- Creates Heroku app
- Configures Procfile
- Sets environment variables

### Deploy Website (Netlify)
```bash
# Connect GitHub repo to Netlify
# Deploy from: website/ directory
```

### Deploy Website (GitHub Pages)
```bash
cd website
git add index.html
git commit -m "Deploy website"
git push origin main
```

---

## 📱 API Usage Examples

### Upload Video
```bash
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@video.mp4"
```

### Process Video
```bash
curl -X POST "http://localhost:8000/api/process?video_id=12345"
```

### Download Result
```bash
curl "http://localhost:8000/download/processed_12345.mp4" \
  --output result.mp4
```

---

## 🧪 Testing

### Unit Tests
```bash
cd backend
python -m pytest tests/
```

### API Tests
```bash
python backend/test_api.py
```

### React Tests
```bash
cd react-app
npm test
```

---

## 📊 File Structure

```
VideoEdit/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── main.py            # Main API
│   │   ├── main_updated.py    # Updated with root path
│   │   ├── services/
│   │   │   ├── video_processor.py
│   │   │   └── ai_service.py
│   │   ├── database.py
│   │   └── config.py
│   ├── requirements.txt
│   └── test_api.py
│
├── react-app/                  # React web application
│   ├── src/
│   │   ├── App.js             # Main component
│   │   ├── pages/
│   │   │   ├── Home.js
│   │   │   ├── Upload.js
│   │   │   ├── Editor.js
│   │   │   └── Results.js
│   │   └── index.css
│   ├── public/
│   │   └── index.html
│   └── package.json
│
├── website/                     # Static website
│   └── index.html              # Landing page
│
├── mobile-app/                  # React Native app
│   ├── android/
│   │   └── app/
│   │       └── build.gradle
│   └── app.json
│
├── build-apk.sh               # APK builder (Linux/Mac)
├── build-apk.bat              # APK builder (Windows)
├── install_ffmpeg.py          # FFmpeg installer
├── install_dependencies.ps1   # Python setup
│
├── deploy_aws.sh              # AWS deployment
├── deploy_gcp.sh              # GCP deployment
├── deploy_heroku.sh           # Heroku deployment
│
└── Documentation/
    ├── README.md
    ├── ARCHITECTURE_GUIDE.md
    ├── GETTING_STARTED.md
    ├── QUICK_REFERENCE.md
    └── COMPLETE_CODE_SAMPLES.md
```

---

## 🔧 Configuration

### Backend Environment (`.env`)
```env
UPLOAD_DIR=uploads
OUTPUT_DIR=outputs
MAX_FILE_SIZE=536870912
API_PORT=8000
DEBUG=True
CORS_ORIGINS=["*"]
```

### React Configuration (`.env`)
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_TIMEOUT=30000
```

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -Ti:8000
kill -9 <PID>
```

### FFmpeg Not Found
```bash
# Download from official site if install script fails
# https://ffmpeg.org/download.html

# Verify installation
ffmpeg -version
```

### React App Won't Start
```bash
# Clear cache and node_modules
cd react-app
rm -rf node_modules package-lock.json
npm install
npm start
```

### APK Build Fails
```bash
# Check Java version (should be 11+)
java -version

# Check Android SDK
echo $ANDROID_HOME

# Clean and rebuild
cd mobile-app/android
./gradlew clean
./gradlew assembleDebug
```

---

## 📈 Performance Tips

1. **Enable Caching:**
   - Redis for API responses
   - Browser caching for static files

2. **Optimize Videos:**
   - Pre-process to H.264 codec
   - Use streaming delivery
   - Enable video compression

3. **Scale Backend:**
   - Use load balancer (Nginx)
   - Horizontal scaling with Docker
   - CDN for static content

4. **Monitor Performance:**
   - Use Application Insights (Azure)
   - CloudWatch (AWS)
   - Stackdriver (GCP)

---

## 🔐 Security Considerations

1. **API Authentication:**
   - Implement JWT tokens
   - Rate limiting enabled
   - Input validation

2. **File Upload:**
   - Validate file types
   - Scan for malware
   - Check file size limits

3. **Data Privacy:**
   - Encrypt sensitive data
   - Implement HTTPS
   - Auto-delete old files

4. **Access Control:**
   - Role-based permissions
   - API key management
   - Audit logging

---

## 📚 Documentation Links

- **FastAPI Docs:** http://localhost:8000/docs
- **React Docs:** https://react.dev
- **Material-UI:** https://mui.com
- **FFmpeg Guide:** https://ffmpeg.org/documentation.html
- **React Native:** https://reactnative.dev
- **Gradle Guide:** https://gradle.org/

---

## 🎯 Next Steps

1. ✅ Start backend API
2. ✅ Start React app
3. ✅ Start website
4. ✅ Build and deploy APK
5. ✅ Deploy to cloud
6. ✅ Monitor performance
7. ✅ Gather user feedback

---

## 📞 Support

- 📖 Check documentation files
- 🐛 Review error logs in `backend/logs/`
- 💬 Open GitHub issues
- 📧 Contact: support@aivideoeditor.com

---

**Happy Coding! 🚀**

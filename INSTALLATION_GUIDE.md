# 📥 INSTALLATION GUIDE - Complete Setup Instructions

## 🎬 Part 1: Install FFmpeg (Required for Video Processing)

### Option A: Automated Installation (Recommended) 🤖

The easiest way - run this command:

```powershell
cd c:\Users\gokul\Downloads\VideoEdit
python install_ffmpeg.py
```

**What it does:**
1. Downloads FFmpeg from official source
2. Extracts to `C:\ffmpeg`
3. Adds to Windows PATH automatically
4. Verifies installation
5. ✅ Done! Restart PowerShell

### Option B: Manual Installation 📖

**Step 1: Download**
- Go to: https://ffmpeg.org/download.html
- Click "Windows" → "Build" section
- Download **"ffmpeg-release-essentials.zip"** (builds by BtbN)
  - URL: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip

**Step 2: Extract**
- Extract the ZIP file to: `C:\ffmpeg`
- You should see: `C:\ffmpeg\bin\ffmpeg.exe`

**Step 3: Add to PATH**

**Method 1: GUI (Easy)**
1. Press `Win + X` → "System" 
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "User variables" → Click "New"
5. Variable name: `Path` (or edit existing)
6. Variable value: `C:\ffmpeg\bin`
7. Click OK → OK → OK
8. **Restart your terminal**

**Method 2: PowerShell (Quick)**
```powershell
# Run as Administrator
$ffmpegPath = "C:\ffmpeg\bin"
[Environment]::SetEnvironmentVariable("Path", "$env:Path;$ffmpegPath", "Machine")
```
Then restart PowerShell.

**Step 4: Verify**
```powershell
ffmpeg -version
```
You should see the FFmpeg version information.

---

## 🎸 Part 2: Install Flutter (Optional - for Mobile UI)

### Option A: Windows GUI Installation 🖱️

**Step 1: Download Flutter**
- Go to: https://flutter.dev/docs/get-started/install
- Click "Windows"
- Download Flutter SDK ZIP file
- Extract to: `C:\flutter`

**Step 2: Add Flutter to PATH**
- Press `Win + X` → "System"
- Advanced system settings → Environment Variables
- Edit `Path` variable
- Add: `C:\flutter\bin`
- Restart terminal

**Step 3: Initial Setup**
```powershell
flutter config --enable-windows-desktop
flutter doctor
```

### Option B: Chocolatey Installation 🍫

If you have admin access:
```powershell
choco install flutter -y
flutter config --enable-windows-desktop
flutter doctor
```

### Step 4: Test Flutter

```powershell
cd c:\Users\gokul\Downloads\VideoEdit\frontend
flutter run
```

The app should open on your emulator/device display.

---

## 🐳 Part 3: Install Docker (Optional - for Containerization)

### Windows Installation

**Step 1: Download Docker Desktop**
- Go to: https://docker.com/products/docker-desktop
- Click "Download for Windows"
- Run the installer

**Step 2: Install**
- Follow the installation wizard
- Use WSL 2 backend (recommended)
- Restart computer when promped

**Step 3: Verify Installation**
```powershell
docker --version
docker-compose --version
```

**Step 4: Test the Application**
```powershell
cd c:\Users\gokul\Downloads\VideoEdit
docker-compose up --build
```

Your app will be available at `http://localhost:8000`

---

## ✅ Verification Checklist

### After Installing FFmpeg
- [ ] Run: `ffmpeg -version`
- [ ] Should show version information
- [ ] Restart backend server
- [ ] Run: `python backend/test_api.py`
- [ ] Should pass all 7 tests

### After Installing Flutter
- [ ] Run: `flutter --version`
- [ ] Should show Flutter version
- [ ] Run: `flutter doctor` (check requirements)
- [ ] Run: `cd frontend && flutter run`
- [ ] App should launch

### After Installing Docker
- [ ] Run: `docker --version`
- [ ] Run: `docker-compose --version`
- [ ] Run: `docker-compose up --build`
- [ ] Visit: `http://localhost:8000`

---

## 🚀 Quick Start After Installation

### With FFmpeg Only (Video Processing Enabled)
```powershell
# Restart the backend
cd c:\Users\gokul\Downloads\VideoEdit\backend
venv\Scripts\python.exe app/main.py

# In new terminal, run tests
cd c:\Users\gokul\Downloads\VideoEdit\backend
venv\Scripts\python.exe test_api.py
```

### With Flutter (Mobile UI Testing)
```powershell
# Terminal 1: Backend
cd backend && venv\Scripts\python.exe app/main.py

# Terminal 2: Frontend
cd frontend && flutter run

# Terminal 3: Tests
cd backend && venv\Scripts\python.exe test_api.py
```

### With Docker (Containerized Setup)
```powershell
# Build and run all services
docker-compose up --build

# Access at http://localhost:8000
```

---

## 🐛 Troubleshooting

### FFmpeg Not Found After Installation
**Solution:**
```powershell
# Close ALL PowerShell windows
# Reopen PowerShell
# Try again: ffmpeg -version
```

### Flutter Build Fails
**Solution:**
```powershell
cd frontend
flutter clean
flutter pub get
flutter run -v
```

### Docker Permission Denied
**Solution:**
- Make sure Docker Desktop is running
- Run PowerShell as Administrator
- Or restart your computer and try again

### Port 8000 Already in Use
**Solution:**
```powershell
# Find and kill process on port 8000
Get-Process | Where-Object {$_.Name -like "*python*"} | Stop-Process -Force

# Or use different port
cd backend
venv\Scripts\python.exe app/main.py --port 8001
```

---

## 📊 System Requirements Summary

| Component | Required? | How to Install | Verification |
|-----------|-----------|---|---|
| **Python 3.10+** | ✅ YES | Already installed | `python --version` |
| **FFmpeg** | ✅ YES | `python install_ffmpeg.py` | `ffmpeg -version` |
| **Flutter** | ⚠️ Optional | https://flutter.dev | `flutter --version` |
| **Docker** | ⚠️ Optional | https://docker.com | `docker --version` |

---

## 🎯 Recommended Installation Order

1. **First**: Verify Python is installed
   ```powershell
   python --version
   ```

2. **Second**: Install FFmpeg (video processing)
   ```powershell
   python install_ffmpeg.py
   # Then restart PowerShell
   ```

3. **Third** (Optional): Install Flutter (mobile UI)
   - For desktop development: https://flutter.dev/docs/get-started/install

4. **Fourth** (Optional): Install Docker (containerization)
   - For production: https://docker.com/products/docker-desktop

---

## 💡 Tips

- **Always restart PowerShell** after modifying PATH environment variables
- **Keep terminal running** where backend server is started
- **Use separate terminals** for backend, frontend, and tests
- **Check documentation** in [MASTER_INDEX.md](MASTER_INDEX.md) for more guides

---

## 📞 Getting Help

If installation fails:

1. **Run diagnostics**
   ```powershell
   python troubleshoot.py
   ```

2. **Check system status**
   ```
   Read: SYSTEM_STATUS.md
   ```

3. **Review logs**
   - Backend logs in terminal where server is running
   - Error messages provide specific guidance

---

## 🎉 Next Steps After Installation

1. ✅ Install FFmpeg
2. ✅ Restart backend server
3. ✅ Run API tests
4. ✅ (Optional) Install Flutter
5. ✅ (Optional) Install Docker
6. ✅ Read [START_HERE.md](START_HERE.md)
7. ✅ Begin development!

---

**Installation Status**: Ready to Begin  
**Recommended Time**: 5-30 minutes (depends on components)

# Install dependencies for AI Video Editor on Windows

Write-Host "🚀 AI Video Editor - Dependency Installation" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

# Check Python
Write-Host "`n1️⃣ Checking Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Python not found. Download from https://python.org" -ForegroundColor Red
    exit 1
}

# Check FFmpeg
Write-Host "`n2️⃣ Checking FFmpeg..." -ForegroundColor Yellow
$ffmpegVersion = ffmpeg -version 2>&1 | Select-Object -First 1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ FFmpeg found" -ForegroundColor Green
} else {
    Write-Host "❌ FFmpeg not found" -ForegroundColor Red
    Write-Host "   Download from: https://ffmpeg.org/download.html" -ForegroundColor Yellow
    Write-Host "   Extract to C:\ffmpeg and add to PATH" -ForegroundColor Yellow
    Write-Host "   Then restart terminal" -ForegroundColor Yellow
}

# Check Flutter
Write-Host "`n3️⃣ Checking Flutter..." -ForegroundColor Yellow
$flutterVersion = flutter --version 2>&1 | Select-Object -First 1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Flutter found" -ForegroundColor Green
} else {
    Write-Host "❌ Flutter not found" -ForegroundColor Red
    Write-Host "   Download from: https://flutter.dev/docs/get-started/install" -ForegroundColor Yellow
    Write-Host "   Then add to PATH and run: flutter config --enable-windows-desktop" -ForegroundColor Yellow
}

# Setup Python environment
Write-Host "`n4️⃣ Setting up Python virtual environment..." -ForegroundColor Yellow
cd backend
if (-not (Test-Path "venv")) {
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✅ Virtual environment already exists" -ForegroundColor Green
}

# Activate venv
Write-Host "`n5️⃣ Installing Python packages..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
pip install -q -r requirements.txt
Write-Host "✅ Python packages installed" -ForegroundColor Green

# Setup Flutter
Write-Host "`n6️⃣ Setting up Flutter..." -ForegroundColor Yellow
cd ..\frontend
flutter pub get
Write-Host "✅ Flutter packages installed" -ForegroundColor Green

Write-Host "`n✅ Setup Complete!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Make sure FFmpeg is installed and in PATH"
Write-Host "2. Make sure Flutter is installed and in PATH"
Write-Host "3. Run: python start_all.py"
Write-Host "`nDocumentation:" -ForegroundColor Cyan
Write-Host "- START_HERE.md" -ForegroundColor Yellow
Write-Host "- README.md" -ForegroundColor Yellow
Write-Host "- SETUP_INSTRUCTIONS.md" -ForegroundColor Yellow

@echo off
REM ================================================
REM AI Video Editor - Complete Startup Script
REM ================================================
REM Launches Backend API, React App, and Website

setlocal enabledelayedexpansion

cls
echo.
echo ================================================
echo  AI Video Editor - All Services Launcher
echo ================================================
echo.

REM Change to project directory
cd /d "%~dp0"

REM Function to start service
:start_service
set service_name=%~1
set service_path=%~2
set port=%~3
set command=%~4

echo.
echo ===== Starting %service_name% on port %port% =====
echo Path: %service_path%
echo.

cd /d "%service_path%"

if "%service_name%"=="Backend API" (
    start "Backend API" cmd /k "python app/main_updated.py"
) else if "%service_name%"=="React App" (
    timeout /t 3 /nobreak
    start "React App" cmd /k "npm start"
) else if "%service_name%"=="Website" (
    timeout /t 3 /nobreak
    start "Website" cmd /k "python -m http.server 8001"
)

cd /d "%~dp0"

:start_services

echo [1/3] Starting Backend API...
call :start_service "Backend API" "%cd%\backend" "8000" "python"
echo.

echo [2/3] Starting React App...
call :start_service "React App" "%cd%\react-app" "3000" "npm"
echo.

echo [3/3] Starting Website...
call :start_service "Website" "%cd%\website" "8001" "python"
echo.

cls
echo.
echo ================================================
echo  ✓ All Services Started Successfully!
echo ================================================
echo.
echo Services are now running:
echo.
echo  🔷 Backend API
echo     URL: http://localhost:8000
echo     API Docs: http://localhost:8000/docs
echo     Status: Go to /health endpoint
echo.
echo  👁 React Web App
echo     URL: http://localhost:3000
echo     Upload videos and edit
echo.
echo  🌐 Website
echo     URL: http://localhost:8001
echo     Landing page and info
echo.
echo ================================================
echo.
echo IMPORTANT:
echo - FFmpeg must be installed for full functionality
echo - All windows will stay open in background
echo - Close any window to stop that service
echo - To stop all: Ctrl+C in each window
echo.
echo Install FFmpeg:
echo   python install_ffmpeg.py
echo.
echo ================================================
echo.

timeout /t 10

:end

@echo off
setlocal enabledelayedexpansion

echo ================================================
echo AI Video Editor - APK Builder (Windows)
echo ================================================
echo.

REM Check if React Native is installed
where react-native >nul 2>&1
if errorlevel 1 (
    echo X React Native CLI not found
    echo Install with: npm install -g react-native-cli
    exit /b 1
)

echo. + React Native CLI found

REM Check if Android SDK is installed
if not defined ANDROID_HOME (
    echo X Android SDK not found
    echo Please set ANDROID_HOME environment variable
    exit /b 1
)

echo. + Android SDK found at: !ANDROID_HOME!
echo.

REM Navigate to mobile-app directory
cd /d "%~dp0mobile-app"

echo Mobile app directory: !CD!
echo.

REM Install dependencies
echo. Installing dependencies...
call npm install

if errorlevel 1 (
    echo X Failed to install dependencies
    exit /b 1
)

echo. + Dependencies installed
echo.

REM Build APK Debug
echo. Building APK ^(Debug^)...
cd android
call gradlew.bat assembleDebug

if errorlevel 1 (
    echo X Debug APK build failed
    exit /b 1
)

echo. + Debug APK built successfully!
echo. Location: app\build\outputs\apk\debug\app-debug.apk
echo.

REM Build APK Release
echo. Building APK ^(Release^)...
call gradlew.bat assembleRelease

if errorlevel 1 (
    echo X Release APK build failed
    echo Note: Debug APK is still available
    exit /b 1
)

echo. + Release APK built successfully!
echo. Location: app\build\outputs\apk\release\app-release.apk
echo.

REM Show file info
if exist "app\build\outputs\apk\release\app-release.apk" (
    for /F "usebackq" %%A in ('app\build\outputs\apk\release\app-release.apk') do (
        set size=%%~zA
        echo File size: !size! bytes
    )
)

echo.

REM Build App Bundle for Play Store
echo. Building App Bundle for Google Play Store...
call gradlew.bat bundleRelease

if errorlevel 1 (
    echo X App Bundle build failed
) else (
    echo. + App Bundle created successfully!
    echo. Location: app\build\outputs\bundle\release\app-release.aab
)

echo.
echo ================================================
echo All build tasks completed!
echo ================================================
echo.
echo Next steps:
echo 1. Transfer APK to Android device
echo 2. Enable installation from unknown sources
echo 3. Install APK and launch app
echo.

pause

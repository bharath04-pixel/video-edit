#!bin/bash

# AI Video Editor - APK Build Script
# Builds Android APK from React Native source

echo "================================================"
echo "AI Video Editor - APK Builder"
echo "================================================"
echo ""

# Check if React Native is installed
if ! command -v react-native &> /dev/null; then
    echo "❌ React Native CLI not found"
    echo "Install with: npm install -g react-native-cli"
    exit 1
fi

# Check if Android SDK is installed
if [ ! -d "$ANDROID_HOME" ]; then
    echo "❌ Android SDK not found"
    echo "Please set ANDROID_HOME environment variable"
    exit 1
fi

echo "✅ React Native CLI found"
echo "✅ Android SDK found at: $ANDROID_HOME"
echo ""

# Navigate to mobile-app directory
cd "$(dirname "$0")"/../mobile-app

echo "📁 Current directory: $(pwd)"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"
echo ""

# Build APK
echo "🔨 Building APK (Debug)..."
cd android
./gradlew assembleDebug

if [ $? -eq 0 ]; then
    echo "✅ Debug APK built successfully!"
    echo "📁 Location: app/build/outputs/apk/debug/app-debug.apk"
else
    echo "❌ APK build failed"
    exit 1
fi

echo ""
echo "🔨 Building APK (Release)..."
./gradlew assembleRelease

if [ $? -eq 0 ]; then
    echo "✅ Release APK built successfully!"
    echo "📁 Location: app/build/outputs/apk/release/app-release.apk"
    echo ""
    echo "📊 File sizes:"
    ls -lh app/build/outputs/apk/release/app-release.apk
else
    echo "❌ Release APK build failed"
    echo "⚠️  Debug APK is still available at app/build/outputs/apk/debug/app-debug.apk"
    exit 1
fi

echo ""
echo "🎉 APK build completed successfully!"
echo ""
echo "Next steps:"
echo "1. Transfer APK to Android device"
echo "2. Enable installation from unknown sources"
echo "3. Install APK and launch app"
echo ""

# Create App Bundle for Play Store
echo "📦 Building App Bundle for Google Play Store..."
./gradlew bundleRelease

if [ $? -eq 0 ]; then
    echo "✅ App Bundle created successfully!"
    echo "📁 Location: app/build/outputs/bundle/release/app-release.aab"
fi

echo ""
echo "================================================"
echo "All build tasks completed!"
echo "================================================"

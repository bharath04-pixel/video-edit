#!/bin/bash
# AI VIDEO EDITOR - QUICK SETUP SCRIPT
# Run this to set up your entire development environment

echo "🚀 AI Video Editor - Setup Script"
echo "===================================="
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     OS="Linux";;
    Darwin*)    OS="macOS";;
    CYGWIN*)    OS="Cygwin";;
    MINGW*)     OS="MinGw";;
    *)          OS="UNKNOWN";;
esac

echo -e "${BLUE}Detected OS: $OS${NC}"
echo ""

# Step 1: Create project structure
echo -e "${BLUE}Step 1: Creating project structure...${NC}"
mkdir -p ai-video-editor/{frontend,backend,shared,docs}
cd ai-video-editor

# Initialize git
git init
git config user.name "Your Name"
git config user.email "your@email.com"

# Create .gitignore
cat > .gitignore << 'EOF'
# Flutter
build/
ios/
android/
.dart_tool/
.flutter-plugins

# Python
backend/venv/
backend/__pycache__/
backend/*.pyc
backend/.env

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
EOF

echo -e "${GREEN}✓ Project structure created${NC}"
echo ""

# Step 2: Install system dependencies
echo -e "${BLUE}Step 2: Installing system dependencies...${NC}"

if [ "$OS" = "macOS" ]; then
    echo "Installing for macOS with Homebrew..."
    brew install git python@3.10 node ffmpeg
elif [ "$OS" = "Linux" ]; then
    echo "Installing for Linux..."
    sudo apt update
    sudo apt install -y git python3.10 python3-pip nodejs ffmpeg
fi

echo -e "${GREEN}✓ System dependencies installed${NC}"
echo ""

# Step 3: Setup Flutter
echo -e "${BLUE}Step 3: Setting up Flutter...${NC}"
if ! command -v flutter &> /dev/null; then
    echo "Flutter not found. Download from https://flutter.dev/docs/get-started"
    echo "Then add to PATH and run: flutter doctor"
else
    echo -e "${GREEN}✓ Flutter found: $(flutter --version)${NC}"
fi

echo ""

# Step 4: Create backend environment
echo -e "${BLUE}Step 4: Setting up Python backend...${NC}"
cd backend

if [ "$OS" = "macOS" ] || [ "$OS" = "Linux" ]; then
    python3 -m venv venv
    source venv/bin/activate
else
    python -m venv venv
    venv\Scripts\activate
fi

# Create requirements.txt
cat > requirements.txt << 'EOF'
fastapi==0.104.0
uvicorn==0.24.0
python-multipart==0.0.6
python-dotenv==1.0.0
aiofiles==23.2.1
pillow==10.1.0
numpy==1.26.2
opencv-python==4.8.1.78
requests==2.31.0
pydantic==2.5.0
gunicorn==21.2.0
EOF

pip install -r requirements.txt

# Create .env
cat > .env << 'EOF'
# API Configuration
UPLOAD_DIR=uploads
OUTPUT_DIR=outputs
MAX_FILE_SIZE=536870912

# Google Vision API
GOOGLE_VISION_API_KEY=your_api_key_here

# remove.bg API
REMOVEBG_API_KEY=your_api_key_here
EOF

# Create app directory structure
mkdir -p app/api
mkdir -p app/services

# Create __init__.py files
touch app/__init__.py
touch app/api/__init__.py
touch app/services/__init__.py

echo -e "${GREEN}✓ Backend environment created${NC}"
echo ""

# Step 5: Create Flutter project
echo -e "${BLUE}Step 5: Creating Flutter project...${NC}"
cd ../frontend
if command -v flutter &> /dev/null; then
    flutter create .
    flutter pub get
    echo -e "${GREEN}✓ Flutter project created${NC}"
else
    echo -e "${YELLOW}⚠ Flutter not in PATH. Install from https://flutter.dev${NC}"
fi

echo ""
echo -e "${GREEN}==================================${NC}"
echo -e "${GREEN}✓ Setup complete!${NC}"
echo -e "${GREEN}==================================${NC}"
echo ""
echo "Next steps:"
echo "1. Add API keys to backend/.env"
echo "2. Start backend: cd backend && python app/main.py"
echo "3. Start Flutter: cd frontend && flutter run"
echo "4. Visit http://localhost:8000/docs for API docs"
echo ""

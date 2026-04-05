#!/bin/bash

# AI VIDEO EDITOR - PROJECT DIAGNOSTIC SCRIPT
# Run this to get a complete status of your project

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   AI VIDEO EDITOR - PROJECT DIAGNOSTIC SCRIPT                 ║"
echo "║   This will assess your current implementation state           ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== 1. GIT INFORMATION ===${NC}"
echo ""
echo "📊 Git Log (Last 5 commits):"
git log --oneline | head -5 || echo "❌ Git not initialized"
echo ""

echo "📌 Current Branch:"
git branch || echo "❌ No git repo"
echo ""

echo "📝 Git Status:"
git status || echo "❌ Not a git repo"
echo ""

echo -e "${BLUE}=== 2. PROJECT STRUCTURE ===${NC}"
echo ""
echo "📁 Root Directory Contents:"
ls -la | grep -E "^d" | awk '{print $9}' | grep -v "^$"
echo ""

echo -e "${BLUE}=== 3. FRONTEND STATUS ===${NC}"
echo ""
if [ -d "frontend" ]; then
    echo -e "${GREEN}✓ frontend/ folder exists${NC}"
    echo ""
    echo "📂 Frontend Structure:"
    ls -la frontend/ | head -15
    echo ""
    
    if [ -f "frontend/pubspec.yaml" ]; then
        echo -e "${GREEN}✓ pubspec.yaml found${NC}"
        echo ""
        echo "Dependencies:"
        grep -A 20 "dependencies:" frontend/pubspec.yaml | head -15
    else
        echo -e "${RED}✗ pubspec.yaml NOT found${NC}"
    fi
    echo ""
    
    if [ -d "frontend/lib" ]; then
        echo -e "${GREEN}✓ lib/ folder exists${NC}"
        echo ""
        echo "Dart Files:"
        find frontend/lib -name "*.dart" | head -20
    else
        echo -e "${RED}✗ lib/ folder NOT found${NC}"
    fi
else
    echo -e "${RED}✗ frontend/ folder NOT found${NC}"
    echo "  Status: Phase 2 not started"
fi
echo ""

echo -e "${BLUE}=== 4. BACKEND STATUS ===${NC}"
echo ""
if [ -d "backend" ]; then
    echo -e "${GREEN}✓ backend/ folder exists${NC}"
    echo ""
    echo "📂 Backend Structure:"
    ls -la backend/ | head -15
    echo ""
    
    if [ -f "backend/requirements.txt" ]; then
        echo -e "${GREEN}✓ requirements.txt found${NC}"
        echo ""
        echo "Dependencies:"
        cat backend/requirements.txt
    else
        echo -e "${RED}✗ requirements.txt NOT found${NC}"
    fi
    echo ""
    
    if [ -d "backend/app" ]; then
        echo -e "${GREEN}✓ app/ folder exists${NC}"
        echo ""
        echo "Python Files:"
        find backend/app -name "*.py" | head -20
    else
        echo -e "${RED}✗ app/ folder NOT found${NC}"
    fi
    echo ""
    
    if [ -f "backend/.env" ]; then
        echo -e "${GREEN}✓ .env file found${NC}"
        echo "  (Not displaying for security)"
    else
        echo -e "${RED}✗ .env file NOT found${NC}"
    fi
else
    echo -e "${RED}✗ backend/ folder NOT found${NC}"
    echo "  Status: Phase 3 not started"
fi
echo ""

echo -e "${BLUE}=== 5. TOOL VERSIONS ===${NC}"
echo ""

echo "Python:"
python3 --version || echo "❌ Python not found"
echo ""

echo "Flutter:"
flutter --version || echo "❌ Flutter not found"
echo ""

echo "FFmpeg:"
ffmpeg -version 2>&1 | head -1 || echo "❌ FFmpeg not found"
echo ""

echo "Node.js:"
node --version || echo "❌ Node.js not found"
echo ""

echo "Git:"
git --version || echo "❌ Git not found"
echo ""

echo -e "${BLUE}=== 6. BACKEND API TEST ===${NC}"
echo ""
echo "Testing if backend is running on port 8000..."
curl -s http://localhost:8000/health && echo "" && echo -e "${GREEN}✓ Backend API is responding${NC}" || echo -e "${RED}✗ Backend API NOT responding${NC}"
echo ""

echo -e "${BLUE}=== 7. PYTHON ENVIRONMENT ===${NC}"
echo ""
if [ -d "backend/venv" ]; then
    echo -e "${GREEN}✓ Virtual environment exists${NC}"
    echo ""
    echo "Installed packages:"
    source backend/venv/bin/activate 2>/dev/null && pip list 2>/dev/null | head -15 || echo "Could not activate venv"
else
    echo -e "${RED}✗ Virtual environment NOT found${NC}"
    echo "  Run: cd backend && python3 -m venv venv"
fi
echo ""

echo -e "${BLUE}=== 8. FILE STORAGE ===${NC}"
echo ""
if [ -d "backend/uploads" ]; then
    echo -e "${GREEN}✓ uploads/ folder exists${NC}"
    echo "  Size: $(du -sh backend/uploads 2>/dev/null | cut -f1)"
else
    echo -e "${RED}✗ uploads/ folder NOT found${NC}"
fi

if [ -d "backend/outputs" ]; then
    echo -e "${GREEN}✓ outputs/ folder exists${NC}"
    echo "  Size: $(du -sh backend/outputs 2>/dev/null | cut -f1)"
else
    echo -e "${RED}✗ outputs/ folder NOT found${NC}"
fi
echo ""

echo -e "${BLUE}=== 9. PHASE ASSESSMENT ===${NC}"
echo ""

PHASE=0

# Phase 1 checks
if [ -f ".gitignore" ] && [ -f "README.md" ]; then
    PHASE=1
fi

# Phase 2 checks
if [ -d "frontend/lib" ] && [ -f "frontend/pubspec.yaml" ]; then
    PHASE=2
fi

# Phase 3 checks
if [ -d "backend/app" ] && [ -f "backend/requirements.txt" ]; then
    PHASE=3
fi

# Phase 4 checks
if [ -f "backend/app/services/video_processor.py" ]; then
    PHASE=4
fi

# Phase 5 checks
if [ -f "backend/app/services/ai_service.py" ]; then
    PHASE=5
fi

# Phase 6 checks
if [ -f "frontend/lib/services/api_service.dart" ]; then
    PHASE=6
fi

echo -e "${BLUE}Your Project is at: PHASE $PHASE${NC}"
echo ""

case $PHASE in
    0)
        echo "🔴 Status: Project not started"
        echo "Next: Initialize project structure"
        echo "Command: mkdir -p frontend backend && git init"
        ;;
    1)
        echo "🟡 Status: Basic setup complete"
        echo "Next: Create Flutter project"
        echo "Command: cd frontend && flutter create ."
        ;;
    2)
        echo "🟡 Status: Flutter project created"
        echo "Next: Create backend API"
        echo "Command: cd backend && python3 -m venv venv"
        ;;
    3)
        echo "🟡 Status: Backend API created"
        echo "Next: Implement video processing (FFmpeg)"
        echo "Command: Add VideoProcessor service to backend"
        ;;
    4)
        echo "🟡 Status: Video processing added"
        echo "Next: Add AI integration (Google Vision, OpenCV)"
        echo "Command: Add AIService to backend"
        ;;
    5)
        echo "🟡 Status: AI integration complete"
        echo "Next: Connect Flutter to backend API"
        echo "Command: Add APIService to Flutter"
        ;;
    6)
        echo "🟢 Status: Full integration in progress"
        echo "Next: Complete Phase 6 (Frontend-Backend Connection)"
        echo "       and then Phase 7 (Testing & Deployment)"
        ;;
    *)
        echo "🟢 Status: Advanced phase"
        echo "Next: Follow Phase 7 (Testing & Deployment)"
        ;;
esac

echo ""
echo -e "${BLUE}=== 10. NEXT IMMEDIATE STEPS ===${NC}"
echo ""

if [ $PHASE -lt 3 ]; then
    echo "1. Complete backend setup:"
    echo "   cd backend"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    echo "   python app/main.py"
fi

if [ $PHASE -lt 2 ]; then
    echo ""
    echo "2. Complete Flutter setup:"
    echo "   cd frontend"
    echo "   flutter pub get"
    echo "   flutter run"
fi

if [ $PHASE -ge 3 ] && [ $PHASE -lt 6 ]; then
    echo ""
    echo "Current Phase: $PHASE"
    echo "Continue with the implementation guide for Phase $((PHASE + 1))"
fi

echo ""
echo -e "${BLUE}=== 11. RESOURCE FILES ===${NC}"
echo ""
echo "Use these guides:"
echo "  • CONTINUATION_GUIDE.md - Understand where you are"
echo "  • AI_VIDEO_EDITOR_COMPLETE_GUIDE.md - Full implementation"
echo "  • QUICK_REFERENCE.md - Commands & APIs"
echo "  • COMPLETE_CODE_SAMPLES.md - Copy-paste code"
echo ""

echo -e "${BLUE}=== DIAGNOSIS COMPLETE ===${NC}"
echo ""
echo "🎯 Summary:"
echo "  Current Phase: $PHASE/8"
echo "  Backend Ready: $([ -d 'backend/app' ] && echo 'YES' || echo 'NO')"
echo "  Frontend Ready: $([ -d 'frontend/lib' ] && echo 'YES' || echo 'NO')"
echo "  API Running: $(curl -s http://localhost:8000/health > /dev/null && echo 'YES' || echo 'NO')"
echo ""


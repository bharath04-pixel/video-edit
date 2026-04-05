#!/bin/bash

# ================================================
# AI Video Editor - Complete Startup Script
# ================================================
# Launches Backend API, React App, and Website

clear

echo ""
echo "================================================"
echo "  AI Video Editor - All Services Launcher"
echo "================================================"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if required commands exist
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}✗ $1 not found${NC}"
        return 1
    fi
    echo -e "${GREEN}✓ $1 found${NC}"
    return 0
}

# Check prerequisites
echo "Checking prerequisites..."
echo ""

check_command "python"
check_command "node"
check_command "npm"

echo ""

# Function to start service
start_service() {
    local service_name=$1
    local service_path=$2
    local port=$3
    local command=$4

    echo ""
    echo "===== Starting $service_name on port $port ====="
    echo "Path: $service_path"
    echo ""

    cd "$service_path"

    if [ "$service_name" = "Backend API" ]; then
        python app/main_updated.py &
        BACKEND_PID=$!
        echo -e "${GREEN}✓ Backend API started (PID: $BACKEND_PID)${NC}"
    elif [ "$service_name" = "React App" ]; then
        sleep 2
        npm start &
        REACT_PID=$!
        echo -e "${GREEN}✓ React App started (PID: $REACT_PID)${NC}"
    elif [ "$service_name" = "Website" ]; then
        sleep 2
        python -m http.server 8001 &
        WEBSITE_PID=$!
        echo -e "${GREEN}✓ Website started (PID: $WEBSITE_PID)${NC}"
    fi
}

# Start all services
echo ""
echo "Starting all services..."
echo ""

# Backend API
start_service "Backend API" "$SCRIPT_DIR/backend" "8000" "python"

# React App  
start_service "React App" "$SCRIPT_DIR/react-app" "3000" "npm"

# Website
start_service "Website" "$SCRIPT_DIR/website" "8001" "python"

# Wait a bit for services to start
sleep 3

clear

echo ""
echo "================================================"
echo -e "  ${GREEN}✓ All Services Started Successfully!${NC}"
echo "================================================"
echo ""
echo -e "${BLUE}Services are now running:${NC}"
echo ""
echo -e "  ${BLUE}🔷 Backend API${NC}"
echo "     URL: http://localhost:8000"
echo "     API Docs: http://localhost:8000/docs"
echo "     Status: Go to /health endpoint"
echo ""
echo -e "  ${BLUE}👁 React Web App${NC}"
echo "     URL: http://localhost:3000"
echo "     Upload videos and edit"
echo ""
echo -e "  ${BLUE}🌐 Website${NC}"
echo "     URL: http://localhost:8001"
echo "     Landing page and info"
echo ""
echo "================================================"
echo ""
echo -e "${YELLOW}IMPORTANT:${NC}"
echo "- FFmpeg must be installed for full functionality"
echo "- All processes run in background"
echo "- To stop all: Run stop-all-services.sh"
echo "- Or manually kill PIDs: $BACKEND_PID, $REACT_PID, $WEBSITE_PID"
echo ""
echo "Install FFmpeg:"
echo "  sudo apt-get install ffmpeg     # Ubuntu/Debian"
echo "  brew install ffmpeg             # Mac"
echo ""
echo "================================================"
echo ""
echo "Opening services in browser..."
sleep 2

# Try to open in browser
if command -v open &> /dev/null; then
    # Mac
    open http://localhost:8000
    open http://localhost:3000
    open http://localhost:8001
elif command -v xdg-open &> /dev/null; then
    # Linux
    xdg-open http://localhost:8000
    xdg-open http://localhost:3000
    xdg-open http://localhost:8001
fi

echo ""
echo "Press Ctrl+C to stop services (multiple times may be needed)"
echo ""

# Keep script running
wait

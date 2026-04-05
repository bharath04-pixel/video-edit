#!/usr/bin/env python3
"""
Start Everything Automation Script
Initializes and starts both backend and frontend
"""

import subprocess
import sys
import time
import os
from pathlib import Path

class AppStarter:
    def __init__(self):
        self.backend_process = None
        self.flutter_process = None
        self.os_name = sys.platform
    
    def print_header(self, text):
        print(f"\n{'='*60}")
        print(f"🚀 {text}")
        print(f"{'='*60}\n")
    
    def print_success(self, text):
        print(f"✅ {text}")
    
    def print_error(self, text):
        print(f"❌ {text}")
    
    def print_info(self, text):
        print(f"ℹ️  {text}")
    
    def start_backend(self):
        """Start FastAPI backend"""
        self.print_header("Starting Backend (FastAPI)")
        
        backend_path = Path("backend")
        if not backend_path.exists():
            self.print_error("Backend directory not found!")
            return False
        
        # Activate venv and start
        if self.os_name == "win32":
            activate_cmd = "venv\\Scripts\\activate && python app/main.py"
            self.backend_process = subprocess.Popen(
                activate_cmd,
                shell=True,
                cwd="backend",
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            cmd = "source venv/bin/activate && python app/main.py"
            self.backend_process = subprocess.Popen(
                cmd,
                shell=True,
                executable="/bin/bash",
                cwd="backend"
            )
        
        print("Waiting for backend to start...")
        time.sleep(3)
        
        # Check if running
        import requests
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                self.print_success("Backend running at http://localhost:8000")
                self.print_info("API Docs: http://localhost:8000/docs")
                return True
        except:
            pass
        
        self.print_error("Backend failed to start")
        return False
    
    def start_frontend(self):
        """Start Flutter app"""
        self.print_header("Starting Frontend (Flutter)")
        
        frontend_path = Path("frontend")
        if not frontend_path.exists():
            self.print_error("Frontend directory not found!")
            return False
        
        try:
            self.flutter_process = subprocess.Popen(
                ["flutter", "run"],
                cwd="frontend"
            )
            self.print_success("Flutter started!")
            return True
        except Exception as e:
            self.print_error(f"Failed to start Flutter: {str(e)}")
            return False
    
    def test_api(self):
        """Run API tests"""
        self.print_header("Testing API")
        
        time.sleep(2)  # Wait for backend to fully start
        
        test_path = Path("backend/test_api.py")
        if not test_path.exists():
            self.print_error("Test script not found!")
            return False
        
        try:
            result = subprocess.run(
                [sys.executable, "test_api.py"],
                cwd="backend",
                capture_output=True,
                text=True,
                timeout=60
            )
            print(result.stdout)
            return result.returncode == 0
        except Exception as e:
            self.print_error(f"Tests failed: {str(e)}")
            return False
    
    def run_all(self):
        """Start everything"""
        print("\n")
        print("╔" + "="*58 + "╗")
        print("║" + " "*15 + "AI VIDEO EDITOR - STARTUP" + " "*19 + "║")
        print("╚" + "="*58 + "╝")
        
        # Check prerequisites
        print("\n📋 Checking prerequisites...")
        if not self.check_requirements():
            self.print_error("Prerequisites not met!")
            return False
        
        # Start backend
        if not self.start_backend():
            return False
        
        # Run tests
        print("\n🧪 Running tests...")
        self.test_api()
        
        # Start frontend
        print("\nWould you like to start Flutter? (y/n): ", end="")
        if input().lower() == 'y':
            self.start_frontend()
        
        # Summary
        self.print_header("✅ STARTUP COMPLETE")
        print("🌐 Backend: http://localhost:8000")
        print("📱 Frontend: Check Flutter window")
        print("📖 API Docs: http://localhost:8000/docs")
        print("🧪 Tests: Run 'python backend/test_api.py'")
        print("\nPress Ctrl+C to stop all services")
        
        # Keep running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n🛑 Shutting down...")
            self.cleanup()
    
    def check_requirements(self):
        """Check if all requirements are met"""
        requirements = []
        
        # Check Python
        try:
            subprocess.run([sys.executable, "--version"], capture_output=True, check=True)
            requirements.append(("Python", True))
        except:
            requirements.append(("Python", False))
        
        # Check FFmpeg
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            requirements.append(("FFmpeg", True))
        except:
            requirements.append(("FFmpeg", False))
        
        # Check Flutter
        try:
            subprocess.run(["flutter", "--version"], capture_output=True, check=True)
            requirements.append(("Flutter", True))
        except:
            requirements.append(("Flutter", False))
        
        # Check directories
        requirements.append(("Backend dir", Path("backend").exists()))
        requirements.append(("Frontend dir", Path("frontend").exists()))
        
        # Print results
        all_met = True
        for req, available in requirements:
            status = "✅" if available else "❌"
            print(f"  {status} {req}")
            if not available:
                all_met = False
        
        return all_met
    
    def cleanup(self):
        """Clean up processes"""
        if self.backend_process:
            self.backend_process.terminate()
        if self.flutter_process:
            self.flutter_process.terminate()

if __name__ == "__main__":
    starter = AppStarter()
    starter.run_all()

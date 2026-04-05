#!/usr/bin/env python3
"""
Comprehensive Troubleshooting Guide
Diagnostic tools and fixes for common issues
"""

import subprocess
import sys
import os
from pathlib import Path

class Troubleshooter:
    def __init__(self):
        self.issues_found = []
        self.fixes_applied = []
    
    def print_header(self, title):
        print(f"\n{'='*60}")
        print(f"🔍 {title}")
        print(f"{'='*60}")
    
    def print_success(self, message):
        print(f"✅ {message}")
    
    def print_warning(self, message):
        print(f"⚠️  {message}")
    
    def print_error(self, message):
        print(f"❌ {message}")
    
    # ====================================================================
    # DIAGNOSTIC TOOLS
    # ====================================================================
    
    def check_python(self):
        """Check Python installation"""
        self.print_header("Python Environment")
        try:
            version = subprocess.check_output([sys.executable, "--version"]).decode().strip()
            self.print_success(f"Python: {version}")
            
            # Check if 3.10+
            parts = version.split()[-1].split('.')
            if int(parts[0]) >= 3 and int(parts[1]) >= 10:
                self.print_success("Python version is compatible (3.10+)")
                return True
            else:
                self.print_error("Python version should be 3.10 or higher")
                self.issues_found.append("Python version too old")
                return False
        except Exception as e:
            self.print_error(f"Python check failed: {str(e)}")
            return False
    
    def check_ffmpeg(self):
        """Check FFmpeg installation"""
        self.print_header("FFmpeg Installation")
        try:
            result = subprocess.check_output(["ffmpeg", "-version"], stderr=subprocess.STDOUT).decode()
            version_line = result.split('\n')[0]
            self.print_success(f"FFmpeg: {version_line}")
            return True
        except FileNotFoundError:
            self.print_error("FFmpeg not found in PATH")
            self.issues_found.append("FFmpeg not installed")
            print("\nFix:")
            print("  macOS: brew install ffmpeg")
            print("  Windows: choco install ffmpeg")
            print("  Linux: sudo apt install ffmpeg")
            return False
        except Exception as e:
            self.print_error(f"FFmpeg check failed: {str(e)}")
            return False
    
    def check_virtual_env(self):
        """Check virtual environment"""
        self.print_header("Virtual Environment")
        venv_path = Path("backend/venv")
        
        if venv_path.exists():
            self.print_success(f"Virtual environment exists: {venv_path}")
            return True
        else:
            self.print_error(f"Virtual environment not found: {venv_path}")
            self.issues_found.append("Virtual environment not created")
            return False
    
    def check_dependencies(self):
        """Check Python dependencies"""
        self.print_header("Python Dependencies")
        try:
            result = subprocess.check_output([sys.executable, "-m", "pip", "list"]).decode()
            
            required = ["fastapi", "uvicorn", "opencv-python", "numpy"]
            missing = []
            
            for package in required:
                if package.lower() in result.lower():
                    self.print_success(f"{package}: installed")
                else:
                    self.print_warning(f"{package}: NOT installed")
                    missing.append(package)
            
            if missing:
                self.issues_found.append(f"Missing packages: {', '.join(missing)}")
                return False
            return True
        except Exception as e:
            self.print_error(f"Dependency check failed: {str(e)}")
            return False
    
    def check_port(self, port=8000):
        """Check if port is available"""
        self.print_header(f"Port {port} Availability")
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result != 0:
                self.print_success(f"Port {port} is available")
                return True
            else:
                self.print_error(f"Port {port} is already in use")
                self.issues_found.append(f"Port {port} in use")
                print(f"\nFix (macOS/Linux):")
                print(f"  lsof -i :{port} | grep LISTEN")
                print(f"  kill -9 <PID>")
                print(f"\nFix (Windows):")
                print(f"  netstat -ano | findstr :{port}")
                print(f"  taskkill /PID <PID> /F")
                return False
        except Exception as e:
            self.print_error(f"Port check failed: {str(e)}")
            return False
    
    def check_files(self):
        """Check required files"""
        self.print_header("Required Files")
        required_files = [
            "backend/app/main.py",
            "backend/requirements.txt",
            "backend/.env",
            "frontend/lib/main.dart",
            "frontend/pubspec.yaml"
        ]
        
        missing = []
        for file_path in required_files:
            if Path(file_path).exists():
                self.print_success(f"Found: {file_path}")
            else:
                self.print_warning(f"Missing: {file_path}")
                missing.append(file_path)
        
        if missing:
            self.issues_found.append(f"Missing files: {', '.join(missing)}")
            return False
        return True
    
    def check_api_endpoint(self, url="http://localhost:8000/health"):
        """Check if API endpoint is responding"""
        self.print_header("API Endpoint Check")
        try:
            import requests
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                self.print_success(f"API is responding: {url}")
                return True
            else:
                self.print_error(f"API returned {response.status_code}")
                self.issues_found.append("API endpoint not responding")
                return False
        except requests.exceptions.ConnectionError:
            self.print_error("Cannot connect to API (is it running?)")
            self.issues_found.append("API connection failed")
            return False
        except Exception as e:
            self.print_error(f"API check failed: {str(e)}")
            return False
    
    # ====================================================================
    # AUTO-FIXES
    # ====================================================================
    
    def fix_virtual_env(self):
        """Create virtual environment"""
        self.print_header("Fixing: Virtual Environment")
        try:
            subprocess.run([sys.executable, "-m", "venv", "backend/venv"], check=True)
            self.print_success("Virtual environment created")
            self.fixes_applied.append("Virtual environment created")
            return True
        except Exception as e:
            self.print_error(f"Failed to create virtual environment: {str(e)}")
            return False
    
    def fix_dependencies(self):
        """Install missing dependencies"""
        self.print_header("Fixing: Python Dependencies")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"],
                check=True
            )
            self.print_success("Dependencies installed")
            self.fixes_applied.append("Dependencies installed")
            return True
        except Exception as e:
            self.print_error(f"Failed to install dependencies: {str(e)}")
            return False
    
    def fix_env_file(self):
        """Create .env file"""
        self.print_header("Fixing: Environment File")
        env_path = Path("backend/.env")
        
        if env_path.exists():
            self.print_warning(".env already exists")
            return True
        
        try:
            content = """ENVIRONMENT=development
DEBUG=true
UPLOAD_DIR=uploads
OUTPUT_DIR=outputs
MAX_FILE_SIZE=536870912
GOOGLE_VISION_API_KEY=your_api_key
REMOVEBG_API_KEY=your_api_key
HOST=0.0.0.0
PORT=8000
WORKERS=4
"""
            env_path.write_text(content)
            self.print_success(".env file created")
            self.fixes_applied.append(".env file created")
            return True
        except Exception as e:
            self.print_error(f"Failed to create .env file: {str(e)}")
            return False
    
    # ====================================================================
    # RUN COMPREHENSIVE CHECK
    # ====================================================================
    
    def run_all_checks(self, auto_fix=False):
        """Run all diagnostic checks"""
        print("\n🔍 AI Video Editor - Comprehensive Diagnostics")
        print("=" * 60)
        
        checks = [
            ("Python", self.check_python),
            ("FFmpeg", self.check_ffmpeg),
            ("Virtual Environment", self.check_virtual_env),
            ("Dependencies", self.check_dependencies),
            ("Port 8000", lambda: self.check_port(8000)),
            ("Required Files", self.check_files),
        ]
        
        results = {}
        for check_name, check_func in checks:
            results[check_name] = check_func()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 DIAGNOSTIC SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for v in results.values() if v)
        total = len(results)
        
        print(f"\nChecks Passed: {passed}/{total}")
        
        if self.issues_found:
            print("\n⚠️  Issues Found:")
            for issue in self.issues_found:
                print(f"  • {issue}")
        
        if auto_fix and self.issues_found:
            print("\n🔧 Attempting Auto-Fixes...")
            self.fix_virtual_env()
            self.fix_env_file()
            self.fix_dependencies()
        
        if self.fixes_applied:
            print("\n✅ Fixes Applied:")
            for fix in self.fixes_applied:
                print(f"  • {fix}")
        
        print("\n" + "=" * 60)
        print("Next Steps:")
        print("1. Review any remaining issues above")
        print("2. Follow the suggested fixes")
        print("3. Run this script again: python troubleshoot.py")
        print("=" * 60)
        
        return len(self.issues_found) == 0

if __name__ == "__main__":
    troubleshooter = Troubleshooter()
    
    auto_fix = "--fix" in sys.argv
    success = troubleshooter.run_all_checks(auto_fix=auto_fix)
    
    sys.exit(0 if success else 1)

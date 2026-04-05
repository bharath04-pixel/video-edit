#!/usr/bin/env python3
"""
Automated Backend Setup Script
Initializes database, installs dependencies, and starts the server
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

class BackendSetup:
    def __init__(self):
        self.os_type = platform.system()
        self.python_cmd = sys.executable
        self.venv_dir = Path("venv")
        self.backend_dir = Path("backend")
        
    def print_step(self, message):
        print(f"\n{'='*60}")
        print(f"📌 {message}")
        print(f"{'='*60}")
    
    def print_success(self, message):
        print(f"✅ {message}")
    
    def print_error(self, message):
        print(f"❌ {message}")
    
    def run_command(self, cmd, shell=False):
        """Run a shell command"""
        try:
            result = subprocess.run(cmd, shell=shell, check=True, capture_output=False)
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            self.print_error(f"Command failed: {' '.join(cmd)}")
            return False
    
    def install_system_dependencies(self):
        """Install system-level dependencies"""
        self.print_step("Installing System Dependencies")
        
        if self.os_type == "Darwin":  # macOS
            commands = [
                ["brew", "install", "ffmpeg"],
                ["brew", "install", "python@3.10"]
            ]
        elif self.os_type == "Linux":  # Ubuntu/Debian
            commands = [
                ["sudo", "apt", "update"],
                ["sudo", "apt", "install", "-y", "ffmpeg", "python3.10", "python3-pip"]
            ]
        elif self.os_type == "Windows":
            self.print_step("Note: For Windows, use Chocolatey or WSL")
            print("Install FFmpeg: choco install ffmpeg")
            return True
        
        for cmd in commands:
            self.run_command(cmd)
        
        self.print_success("System dependencies installed")
        return True
    
    def create_virtual_environment(self):
        """Create Python virtual environment"""
        self.print_step("Creating Virtual Environment")
        
        if not self.venv_dir.exists():
            self.run_command([self.python_cmd, "-m", "venv", str(self.venv_dir)])
            self.print_success("Virtual environment created")
        else:
            self.print_success("Virtual environment already exists")
        
        return True
    
    def install_dependencies(self):
        """Install Python dependencies"""
        self.print_step("Installing Python Dependencies")
        
        if self.os_type == "Windows":
            pip_cmd = self.venv_dir / "Scripts" / "pip"
        else:
            pip_cmd = self.venv_dir / "bin" / "pip"
        
        self.run_command([str(pip_cmd), "install", "--upgrade", "pip"])
        self.run_command([str(pip_cmd), "install", "-r", str(self.backend_dir / "requirements.txt")])
        
        self.print_success("Python dependencies installed")
        return True
    
    def setup_environment_files(self):
        """Setup environment configuration"""
        self.print_step("Setting Up Environment Files")
        
        env_file = self.backend_dir / ".env"
        env_example = self.backend_dir / ".env.example"
        
        if not env_file.exists() and not env_example.exists():
            env_content = """# Backend Configuration
ENVIRONMENT=development
DEBUG=true

# Upload Configuration
UPLOAD_DIR=uploads
OUTPUT_DIR=outputs
MAX_FILE_SIZE=536870912

# API Keys
GOOGLE_VISION_API_KEY=your_api_key_here
REMOVEBG_API_KEY=your_api_key_here

# Server
HOST=0.0.0.0
PORT=8000
WORKERS=4
"""
            env_file.write_text(env_content)
            self.print_success(".env file created")
        else:
            self.print_success(".env file already exists")
        
        return True
    
    def verify_installation(self):
        """Verify all installations"""
        self.print_step("Verifying Installation")
        
        checks = {
            "Python": ["python", "--version"],
            "FFmpeg": ["ffmpeg", "-version"],
            "Pip": ["pip", "--version"]
        }
        
        all_good = True
        for name, cmd in checks.items():
            try:
                subprocess.run(cmd, capture_output=True, timeout=5, check=True)
                self.print_success(f"{name} is installed")
            except:
                self.print_error(f"{name} not found")
                all_good = False
        
        return all_good
    
    def start_server(self):
        """Start the FastAPI server"""
        self.print_step("Starting Backend Server")
        
        if self.os_type == "Windows":
            python_cmd = self.venv_dir / "Scripts" / "python"
        else:
            python_cmd = self.venv_dir / "bin" / "python"
        
        main_file = self.backend_dir / "app" / "main.py"
        
        print(f"\n🚀 Starting server from {main_file}...")
        print(f"📍 Server will be available at: http://localhost:8000")
        print(f"📖 API docs at: http://localhost:8000/docs\n")
        
        self.run_command([str(python_cmd), str(main_file)])
    
    def run_full_setup(self):
        """Execute complete setup"""
        print("\n🎬 AI Video Editor - Backend Setup")
        print("=" * 60)
        
        steps = [
            ("System Dependencies", self.install_system_dependencies),
            ("Virtual Environment", self.create_virtual_environment),
            ("Python Dependencies", self.install_dependencies),
            ("Environment Files", self.setup_environment_files),
            ("Installation Verification", self.verify_installation),
        ]
        
        for step_name, step_func in steps:
            if not step_func():
                self.print_error(f"Failed at: {step_name}")
                return False
        
        self.print_step("Setup Complete! ✅")
        print("\n🎯 Next Steps:")
        print("1. Configure .env file with your API keys")
        print("2. Run: python setup_backend.py --start")
        print("3. Visit http://localhost:8000/docs for API documentation")
        
        return True

if __name__ == "__main__":
    setup = BackendSetup()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--start":
        print("Starting server...")
        setup.start_server()
    else:
        if setup.run_full_setup():
            print("\n💡 Tip: Run 'python setup_backend.py --start' to start the server")
            sys.exit(0)
        else:
            sys.exit(1)

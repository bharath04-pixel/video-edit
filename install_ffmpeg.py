#!/usr/bin/env python3
"""
Automated FFmpeg Installation & Configuration Script for Windows
This script downloads and installs FFmpeg, then adds it to Windows PATH
"""

import os
import sys
import subprocess
import json
from pathlib import Path
import urllib.request
import zipfile
import shutil

class FFmpegInstaller:
    def __init__(self):
        self.ffmpeg_dir = Path("C:\\ffmpeg")
        self.bin_dir = self.ffmpeg_dir / "bin"
        self.download_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        
    def print_header(self, text):
        print(f"\n{'='*60}")
        print(f"🎬 {text}")
        print(f"{'='*60}\n")
    
    def print_step(self, step, text):
        print(f"\n{step}. {text}")
    
    def print_success(self, text):
        print(f"  ✅ {text}")
    
    def print_error(self, text):
        print(f"  ❌ {text}")
        
    def print_info(self, text):
        print(f"  ℹ️  {text}")
    
    def check_ffmpeg_exists(self):
        """Check if FFmpeg is already in PATH"""
        try:
            result = subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                self.print_success(f"FFmpeg already installed: {version_line}")
                return True
        except FileNotFoundError:
            pass
        return False
    
    def create_directories(self):
        """Create necessary directories"""
        self.print_step(1, "Creating directories")
        try:
            self.ffmpeg_dir.mkdir(parents=True, exist_ok=True)
            self.print_success(f"Created: {self.ffmpeg_dir}")
            return True
        except Exception as e:
            self.print_error(f"Failed to create directory: {e}")
            return False
    
    def download_ffmpeg(self):
        """Download FFmpeg"""
        self.print_step(2, "Downloading FFmpeg")
        try:
            zip_file = self.ffmpeg_dir / "ffmpeg.zip"
            self.print_info(f"This may take a few minutes...")
            urllib.request.urlretrieve(self.download_url, zip_file)
            self.print_success(f"Downloaded: {zip_file}")
            return True
        except Exception as e:
            self.print_error(f"Download failed: {e}")
            return False
    
    def extract_ffmpeg(self):
        """Extract FFmpeg ZIP file"""
        self.print_step(3, "Extracting FFmpeg")
        try:
            zip_file = self.ffmpeg_dir / "ffmpeg.zip"
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(self.ffmpeg_dir)
            
            # Find the extracted directory and move its contents
            extracted_dirs = [d for d in self.ffmpeg_dir.iterdir() 
                            if d.is_dir() and d.name.startswith("ffmpeg-")]
            
            if extracted_dirs:
                extracted_dir = extracted_dirs[0]
                # Move bin directory
                src_bin = extracted_dir / "bin"
                if src_bin.exists():
                    for file in src_bin.iterdir():
                        shutil.copy2(file, self.bin_dir)
                    self.print_success(f"Extracted to: {self.bin_dir}")
            
            # Clean up
            zip_file.unlink()
            for d in extracted_dirs:
                shutil.rmtree(d)
            
            return True
        except Exception as e:
            self.print_error(f"Extraction failed: {e}")
            return False
    
    def add_to_path(self):
        """Add FFmpeg to Windows PATH"""
        self.print_step(4, "Adding to Windows PATH")
        bin_path = str(self.bin_dir)
        
        try:
            # Add to user PATH via registry
            import winreg
            
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Environment",
                0,
                winreg.KEY_ALL_ACCESS
            )
            
            current_path = winreg.QueryValueEx(key, "Path")[0]
            
            if bin_path not in current_path:
                new_path = f"{current_path};{bin_path}"
                winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
                winreg.CloseKey(key)
                
                self.print_success(f"Added to PATH: {bin_path}")
                self.print_info("Restart PowerShell for changes to take effect")
            else:
                self.print_success("Already in PATH")
            
            return True
        except Exception as e:
            self.print_error(f"Failed to update PATH: {e}")
            self.print_info("You can manually add the following to PATH:")
            self.print_info(bin_path)
            return False
    
    def verify_installation(self):
        """Verify FFmpeg installation"""
        self.print_step(5, "Verifying installation")
        try:
            result = subprocess.run(
                [str(self.bin_dir / "ffmpeg.exe"), "-version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                self.print_success(f"Verification passed: {version_line}")
                return True
            else:
                self.print_error(f"Verification failed: {result.stderr}")
                return False
        except Exception as e:
            self.print_error(f"Verification error: {e}")
            return False
    
    def run_installation(self):
        """Run complete installation"""
        self.print_header("FFmpeg Installation for Windows")
        
        # Check if already installed
        if self.check_ffmpeg_exists():
            return True
        
        # Create directories
        if not self.create_directories():
            return False
        
        # Download
        if not self.download_ffmpeg():
            return False
        
        # Extract
        if not self.extract_ffmpeg():
            return False
        
        # Add to PATH
        self.add_to_path()
        
        # Verify
        if not self.verify_installation():
            self.print_info("Manual verification: open new PowerShell and run: ffmpeg -version")
            return False
        
        return True
    
    def print_summary(self):
        """Print installation summary"""
        self.print_header("✅ Installation Complete!")
        print("Next steps:")
        print("1. 🔄 Close and reopen PowerShell")
        print("2. ✅ Verify: ffmpeg -version")
        print("3. ⏮️  Restart backend: cd backend && venv\\Scripts\\python.exe app/main.py")
        print("4. 🧪 Run tests: python test_api.py")
        print("\nDocumentation:")
        print("- START_HERE.md")
        print("- SYSTEM_STATUS.md")
        print("- QUICK_COMMANDS.md")

def main():
    try:
        installer = FFmpegInstaller()
        success = installer.run_installation()
        installer.print_summary()
        return 0 if success else 1
    except Exception as e:
        print(f"❌ Installation failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

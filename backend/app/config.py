"""
Configuration module for AI Video Editor Backend
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    
    # Environment
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"
    
    # File handling
    UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "uploads"))
    OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "outputs"))
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 536870912))  # 500MB
    
    # API
    API_TITLE = "AI Video Editor API"
    API_VERSION = "1.0.0"
    
    # Video processing
    ALLOWED_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}
    SAMPLE_RATE = 30  # Process every Nth frame
    
    # CORS
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:8000",
        "*"  # Allow all in development
    ]
    
    # APIs
    GOOGLE_VISION_API_KEY = os.getenv("GOOGLE_VISION_API_KEY", "")
    REMOVEBG_API_KEY = os.getenv("REMOVEBG_API_KEY", "")
    
    @staticmethod
    def setup():
        """Setup directories"""
        Path(Config.UPLOAD_DIR).mkdir(exist_ok=True)
        Path(Config.OUTPUT_DIR).mkdir(exist_ok=True)

class DevelopmentConfig(Config):
    """Development configuration"""
    ENVIRONMENT = "development"
    DEBUG = True
    RELOAD = True

class ProductionConfig(Config):
    """Production configuration"""
    ENVIRONMENT = "production"
    DEBUG = False
    RELOAD = False
    CORS_ORIGINS = [
        "https://yourdomain.com",
        "https://app.yourdomain.com"
    ]

# Select configuration
ENV = os.getenv("ENVIRONMENT", "development")
if ENV == "production":
    config = ProductionConfig()
else:
    config = DevelopmentConfig()

config.setup()

"""
Database Models using SQLAlchemy
For user management, video history, processing logs
"""

from sqlalchemy import create_engine, Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ai_video_editor.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ============================================================================
# USER MODEL
# ============================================================================

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    videos = relationship("Video", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.username}>"


# ============================================================================
# VIDEO MODEL
# ============================================================================

class Video(Base):
    __tablename__ = "videos"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String, index=True)
    filepath = Column(String)
    file_size = Column(Integer)
    duration = Column(Integer)  # seconds
    width = Column(Integer)
    height = Column(Integer)
    codec = Column(String)
    fps = Column(Integer)
    is_processing = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    output_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="videos")
    operations = relationship("ProcessingOperation", back_populates="video")
    
    def __repr__(self):
        return f"<Video {self.filename}>"


# ============================================================================
# PROCESSING OPERATION MODEL
# ============================================================================

class ProcessingOperation(Base):
    __tablename__ = "processing_operations"
    
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(String, ForeignKey("videos.id"))
    operation_type = Column(String)  # text_detection, person_detection, etc.
    status = Column(String, default="pending")  # pending, processing, completed, failed
    result = Column(String, nullable=True)  # JSON string of results
    error_message = Column(String, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    video = relationship("Video", back_populates="operations")
    
    def __repr__(self):
        return f"<ProcessingOperation {self.operation_type} on {self.video_id}>"


# ============================================================================
# API LOG MODEL
# ============================================================================

class APILog(Base):
    __tablename__ = "api_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    method = Column(String)  # GET, POST, etc.
    endpoint = Column(String)
    status_code = Column(Integer)
    response_time = Column(Integer)  # milliseconds
    ip_address = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<APILog {self.method} {self.endpoint} {self.status_code}>"


# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    init_db()
    print("✅ Database initialized successfully!")

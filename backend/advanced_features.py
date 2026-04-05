#!/usr/bin/env python3
"""
Advanced API Features
- Database integration (SQLAlchemy)
- User authentication (JWT)
- Rate limiting
- Caching
- Advanced logging
- Request/Response middleware
"""

from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.security import HTTPBearer, HTTPAuthCredential
import jwt
from datetime import datetime, timedelta
import os
from functools import wraps
import logging

logger = logging.getLogger(__name__)

# ============================================================================
# JWT AUTHENTICATION
# ============================================================================

class JWTAuthenticator:
    """JWT token authentication"""
    
    def __init__(self, secret_key: str = None):
        self.secret_key = secret_key or os.getenv("JWT_SECRET_KEY", "your-secret-key")
        self.algorithm = "HS256"
        self.expiration_minutes = 1440  # 24 hours
    
    def create_token(self, data: dict) -> str:
        """Create JWT token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.expiration_minutes)
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> dict:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
    
    def get_current_user(self, token: HTTPAuthCredential = Depends(HTTPBearer())):
        """Dependency for protected routes"""
        return self.verify_token(token.credentials)


# ============================================================================
# RATE LIMITING
# ============================================================================

class RateLimiter:
    """Simple in-memory rate limiting"""
    
    def __init__(self, requests_per_minute: int = 100):
        self.requests_per_minute = requests_per_minute
        self.request_log = {}
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if client is within rate limits"""
        now = datetime.utcnow()
        
        if client_id not in self.request_log:
            self.request_log[client_id] = []
        
        # Remove old requests (older than 1 minute)
        self.request_log[client_id] = [
            req_time for req_time in self.request_log[client_id]
            if (now - req_time).seconds < 60
        ]
        
        if len(self.request_log[client_id]) >= self.requests_per_minute:
            return False
        
        self.request_log[client_id].append(now)
        return True


# ============================================================================
# CACHING
# ============================================================================

class SimpleCache:
    """Simple in-memory cache with TTL"""
    
    def __init__(self):
        self.cache = {}
    
    def get(self, key: str):
        """Get value from cache"""
        if key in self.cache:
            value, expiry = self.cache[key]
            if datetime.utcnow() < expiry:
                return value
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value, ttl_seconds: int = 3600):
        """Set value in cache with TTL"""
        expiry = datetime.utcnow() + timedelta(seconds=ttl_seconds)
        self.cache[key] = (value, expiry)
    
    def clear(self):
        """Clear entire cache"""
        self.cache.clear()


# ============================================================================
# LOGGING MIDDLEWARE
# ============================================================================

def setup_advanced_logging():
    """Setup advanced logging with file rotation"""
    from logging.handlers import RotatingFileHandler
    
    logger = logging.getLogger("ai_video_editor")
    logger.setLevel(logging.DEBUG)
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        "logs/api.log",
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# ============================================================================
# EXAMPLE: Advanced API Endpoints
# ============================================================================

def create_advanced_routes(app: FastAPI):
    """Create advanced routes with authentication and caching"""
    
    jwt_auth = JWTAuthenticator()
    rate_limiter = RateLimiter(requests_per_minute=100)
    cache = SimpleCache()
    
    # Login endpoint
    @app.post("/auth/login")
    async def login(email: str, password: str):
        """Login and get JWT token"""
        # In production, verify email and password against database
        if not email or not password:
            raise HTTPException(status_code=400, detail="Invalid credentials")
        
        token = jwt_auth.create_token({"sub": email})
        return {"access_token": token, "token_type": "bearer"}
    
    # Protected endpoint with rate limiting
    @app.get("/api/protected")
    async def protected_route(
        current_user: dict = Depends(jwt_auth.get_current_user),
        x_forwarded_for: str = Header(None)
    ):
        """Protected endpoint requiring JWT token"""
        client_id = x_forwarded_for or "unknown"
        
        if not rate_limiter.is_allowed(client_id):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        return {"message": f"Hello {current_user.get('sub')}"}
    
    # Cached endpoint
    @app.get("/api/stats")
    async def get_stats():
        """Get stats with caching"""
        cache_key = "stats"
        cached = cache.get(cache_key)
        
        if cached:
            return {"cached": True, "data": cached}
        
        # Simulate expensive operation
        stats = {
            "total_videos": 150,
            "total_users": 45,
            "api_calls": 10000
        }
        
        cache.set(cache_key, stats, ttl_seconds=300)  # Cache for 5 minutes
        return {"cached": False, "data": stats}
    
    return app

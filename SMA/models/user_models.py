"""User-related models for the SMA system"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON, Float
from sqlalchemy.sql import func
from datetime import datetime
from .database import Base

class UserProfile(Base):
    """User profile information"""
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20))
    date_of_birth = Column(DateTime)
    gender = Column(String(20))
    location = Column(String(255))
    avatar_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class UserPreferences(Base):
    """User preferences and settings"""
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), index=True, nullable=False)
    language = Column(String(10), default="fr")
    currency = Column(String(3), default="EUR")
    timezone = Column(String(50))
    notification_email = Column(Boolean, default=True)
    notification_sms = Column(Boolean, default=False)
    notification_push = Column(Boolean, default=True)
    marketing_emails = Column(Boolean, default=False)
    theme = Column(String(20), default="light")
    accessibility_features = Column(JSON)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class UserBehavior(Base):
    """User behavior tracking"""
    __tablename__ = "user_behaviors"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), index=True, nullable=False)
    session_id = Column(String(100), index=True)
    action_type = Column(String(100), nullable=False)
    action_details = Column(JSON)
    timestamp = Column(DateTime, default=func.now())
    ip_address = Column(String(45))
    user_agent = Column(Text)
    page_url = Column(String(500))
    referrer = Column(String(500))

class UserSegment(Base):
    """User segmentation information"""
    __tablename__ = "user_segments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), index=True, nullable=False)
    segment_name = Column(String(100), nullable=False)
    segment_value = Column(String(100))
    confidence_score = Column(Float, default=0.0)
    assigned_at = Column(DateTime, default=func.now())
    expires_at = Column(DateTime)
    meta_data = Column(JSON)

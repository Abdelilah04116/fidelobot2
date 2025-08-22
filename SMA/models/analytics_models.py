"""Analytics-related models for the SMA system"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON, Float, ForeignKey
from sqlalchemy.sql import func
from datetime import datetime
from .database import Base

class ConversationAnalytics(Base):
    """Conversation analytics data"""
    __tablename__ = "conversation_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), index=True)
    user_id = Column(String(50), index=True)
    conversation_start = Column(DateTime)
    conversation_end = Column(DateTime)
    message_count = Column(Integer, default=0)
    agent_interactions = Column(JSON)
    intent_detected = Column(String(100))
    satisfaction_score = Column(Float)
    created_at = Column(DateTime, default=func.now())

class UserAnalytics(Base):
    """User behavior analytics"""
    __tablename__ = "user_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), index=True)
    session_count = Column(Integer, default=0)
    total_conversation_time = Column(Integer, default=0)  # in seconds
    products_viewed = Column(JSON)
    search_queries = Column(JSON)
    conversion_rate = Column(Float, default=0.0)
    last_activity = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class ProductAnalytics(Base):
    """Product performance analytics"""
    __tablename__ = "product_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    view_count = Column(Integer, default=0)
    search_appearances = Column(Integer, default=0)
    conversion_count = Column(Integer, default=0)
    average_rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    last_updated = Column(DateTime, default=func.now(), onupdate=func.now())

class SystemMetrics(Base):
    """System performance metrics"""
    __tablename__ = "system_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float)
    metric_unit = Column(String(20))
    timestamp = Column(DateTime, default=func.now())
    meta_data = Column(JSON)

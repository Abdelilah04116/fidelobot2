from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, DateTime, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from redis import Redis
from pymongo import MongoClient
import asyncio
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import json

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True)
    status = Column(String, default="visitor")
    profile = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    gdpr_consent = Column(Boolean, default=False)
    consent_date = Column(DateTime)

class Product(Base):
    __tablename__ = "products"
    
    id = Column(String, primary_key=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    price = Column(Float)
    description = Column(String)
    in_stock = Column(Boolean, default=True)
    rating = Column(Float, default=0.0)
    tags = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(String, primary_key=True)
    session_id = Column(String, index=True)
    user_id = Column(String, index=True)
    messages = Column(JSON)
    intent = Column(String, index=True)
    sentiment_score = Column(Float, default=0.0)
    escalated = Column(Boolean, default=False)
    escalation_reason = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    status = Column(String, default="pending")
    total = Column(Float)
    items = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"
    
    id = Column(String, primary_key=True)
    category = Column(String, index=True)
    question = Column(String)
    answer = Column(Text)
    keywords = Column(JSON)
    confidence_score = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)

class DatabaseManager:
    def __init__(self, config):
        self.config = config
        self.engine = create_engine(config.database.postgres_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Redis pour cache et sessions
        self.redis_client = Redis.from_url(config.database.redis_url)
        
        # MongoDB pour analytics
        self.mongo_client = MongoClient(config.database.mongo_url)
        self.mongo_db = self.mongo_client[config.database.mongo_db]
        
        # Créer les tables
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self) -> Session:
        return self.SessionLocal()
    
    def close_connections(self):
        self.redis_client.close()
        self.mongo_client.close()
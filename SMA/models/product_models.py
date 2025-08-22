"""Product-related models for the SMA system"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

# Product class is already defined in database.py
# class Product(Base):
#     """Product information"""
#     __tablename__ = "products"
#     
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(255), nullable=False, index=True)
#     description = Column(Text)
#     price = Column(Float, nullable=False)
#     category = Column(String(100), index=True)
#     brand = Column(String(100), index=True)
#     stock_quantity = Column(Integer, default=0)
#     image_url = Column(String(500))
#     specifications = Column(JSON)
#     is_active = Column(Boolean, default=True)
#     created_at = Column(DateTime, default=func.now())
#     updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class ProductCategory(Base):
    """Product categories"""
    __tablename__ = "product_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey("product_categories.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())

class ProductRecommendation(Base):
    """Product recommendations"""
    __tablename__ = "product_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    recommendation_score = Column(Float, default=0.0)
    recommendation_type = Column(String(50))
    created_at = Column(DateTime, default=func.now())

class ProductSearchResult(Base):
    """Product search results cache"""
    __tablename__ = "product_search_results"
    
    id = Column(Integer, primary_key=True, index=True)
    search_query = Column(String(255), index=True)
    search_filters = Column(JSON)
    result_count = Column(Integer)
    search_timestamp = Column(DateTime, default=func.now())
    user_id = Column(String(50), index=True)
    session_id = Column(String(100), index=True)

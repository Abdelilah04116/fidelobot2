"""Order-related models for the SMA system"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

# Order class is already defined in database.py
# class Order(Base):
#     """Order information"""
#     __tablename__ = "orders"
#     
#     id = Column(Integer, primary_key=True, index=True)
#     order_number = Column(String(50), unique=True, index=True)
#     user_id = Column(String(50), index=True, nullable=False)
#     status = Column(String(50), default="pending")
#     total_amount = Column(Float, nullable=False)
#     currency = Column(String(3), default="EUR")
#     shipping_address = Column(JSON)
#     billing_address = Column(JSON)
#     payment_method = Column(String(100))
#     payment_status = Column(String(50), default="pending")
#     created_at = Column(DateTime, default=func.now())
#     updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

# OrderItem class is already defined in database.py
# class OrderItem(Base):
#     """Order items"""
#     __tablename__ = "order_items"
#     
#     id = Column(Integer, primary_key=True, index=True)
#     order_id = Column(Integer, ForeignKey("orders.id"))
#     product_id = Column(Integer, ForeignKey("products.id"))
#     quantity = Column(Integer, nullable=False)
#     unit_price = Column(Float, nullable=False)
#     total_price = Column(Float, nullable=False)
#     created_at = Column(DateTime, default=func.now())

class OrderStatus(Base):
    """Order status tracking"""
    __tablename__ = "order_statuses"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    status = Column(String(50), nullable=False)
    status_details = Column(Text)
    timestamp = Column(DateTime, default=func.now())
    updated_by = Column(String(50))

class OrderHistory(Base):
    """Order history and audit trail"""
    __tablename__ = "order_history"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    action = Column(String(100), nullable=False)
    action_details = Column(JSON)
    performed_by = Column(String(50))
    timestamp = Column(DateTime, default=func.now())

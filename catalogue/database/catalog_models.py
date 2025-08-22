"""
Modèles de base de données relationnelle pour le catalogue des produits
Structure complète pour un site e-commerce avec produits, catégories, variantes, etc.
"""

from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, ForeignKey, JSON, Enum, Computed
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from typing import Optional, List
from datetime import datetime

Base = declarative_base()

class ProductStatus(PyEnum):
    """Statuts possibles d'un produit"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    OUT_OF_STOCK = "out_of_stock"
    DISCONTINUED = "discontinued"
    DRAFT = "draft"

class ProductType(PyEnum):
    """Types de produits"""
    PHYSICAL = "physical"
    DIGITAL = "digital"
    SERVICE = "service"
    SUBSCRIPTION = "subscription"

class Category(Base):
    """Table des catégories de produits"""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    image_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    parent = relationship("Category", remote_side=[id], back_populates="children")
    children = relationship("Category", back_populates="parent")
    products = relationship("Product", back_populates="category")

class Brand(Base):
    """Table des marques"""
    __tablename__ = "brands"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    logo_url = Column(String(500))
    website = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    products = relationship("Product", back_populates="brand")

class Product(Base):
    """Table principale des produits"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False, index=True)
    slug = Column(String(200), unique=True, nullable=False, index=True)
    description = Column(Text)
    short_description = Column(String(500))
    
    # Informations de base
    product_type = Column(Enum(ProductType), default=ProductType.PHYSICAL)
    status = Column(Enum(ProductStatus), default=ProductStatus.ACTIVE)
    
    # Prix et stock
    base_price = Column(Float, nullable=False)
    sale_price = Column(Float)
    cost_price = Column(Float)
    weight = Column(Float)  # en grammes
    dimensions = Column(JSON)  # {"length": 10, "width": 5, "height": 2}
    
    # Stock
    stock_quantity = Column(Integer, default=0)
    low_stock_threshold = Column(Integer, default=5)
    track_stock = Column(Boolean, default=True)
    
    # SEO et marketing
    meta_title = Column(String(200))
    meta_description = Column(String(500))
    meta_keywords = Column(String(500))
    
    # Images
    main_image_url = Column(String(500))
    image_urls = Column(JSON)  # ["url1", "url2", ...]
    
    # Relations
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    published_at = Column(DateTime(timezone=True))
    
    # Relations
    category = relationship("Category", back_populates="products")
    brand = relationship("Brand", back_populates="products")
    variants = relationship("ProductVariant", back_populates="product", cascade="all, delete-orphan")
    attributes = relationship("ProductAttribute", back_populates="product", cascade="all, delete-orphan")
    reviews = relationship("ProductReview", back_populates="product", cascade="all, delete-orphan")
    tags = relationship("ProductTag", secondary="product_tag_association", back_populates="products")

class ProductVariant(Base):
    """Variantes de produits (couleur, taille, etc.)"""
    __tablename__ = "product_variants"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    sku = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    
    # Attributs spécifiques
    attributes = Column(JSON)  # {"color": "red", "size": "L"}
    
    # Prix et stock spécifiques
    price_adjustment = Column(Float, default=0.0)  # Différence avec le prix de base
    stock_quantity = Column(Integer, default=0)
    
    # Images spécifiques
    image_url = Column(String(500))
    
    # Relations
    product = relationship("Product", back_populates="variants")

class ProductAttribute(Base):
    """Attributs personnalisables des produits"""
    __tablename__ = "product_attributes"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    name = Column(String(100), nullable=False)
    value = Column(Text, nullable=False)
    display_order = Column(Integer, default=0)
    
    # Relations
    product = relationship("Product", back_populates="attributes")

class ProductTag(Base):
    """Tags pour catégoriser les produits"""
    __tablename__ = "product_tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True, index=True)
    slug = Column(String(50), unique=True, nullable=False, index=True)
    color = Column(String(7))  # Code couleur hex
    description = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    products = relationship("Product", secondary="product_tag_association", back_populates="tags")

class ProductTagAssociation(Base):
    """Table d'association entre produits et tags (many-to-many)"""
    __tablename__ = "product_tag_association"
    
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("product_tags.id"), primary_key=True)

class ProductReview(Base):
    """Avis et évaluations des produits"""
    __tablename__ = "product_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Contenu de l'avis
    rating = Column(Integer, nullable=False)  # 1-5 étoiles
    title = Column(String(200))
    comment = Column(Text)
    
    # Modération
    is_verified_purchase = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=False)
    is_helpful = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    product = relationship("Product", back_populates="reviews")

class ProductImage(Base):
    """Images des produits avec métadonnées"""
    __tablename__ = "product_images"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    variant_id = Column(Integer, ForeignKey("product_variants.id"), nullable=True)
    
    # Informations de l'image
    url = Column(String(500), nullable=False)
    alt_text = Column(String(200))
    title = Column(String(200))
    
    # Métadonnées
    file_size = Column(Integer)  # en bytes
    dimensions = Column(JSON)  # {"width": 800, "height": 600}
    mime_type = Column(String(100))
    
    # Ordre d'affichage
    display_order = Column(Integer, default=0)
    is_main = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Inventory(Base):
    """Gestion avancée des stocks"""
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    variant_id = Column(Integer, ForeignKey("product_variants.id"), nullable=True)
    
    # Stock
    quantity = Column(Integer, default=0)
    reserved_quantity = Column(Integer, default=0)  # Commandes en cours
    available_quantity = Column(Integer, Computed("quantity - reserved_quantity"))
    
    # Seuils d'alerte
    low_stock_threshold = Column(Integer, default=5)
    reorder_point = Column(Integer, default=10)
    reorder_quantity = Column(Integer, default=50)
    
    # Localisation
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=True)
    location = Column(String(100))  # Aisle, shelf, etc.
    
    # Timestamps
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    warehouse = relationship("Warehouse", back_populates="inventory_items")

class Warehouse(Base):
    """Entrepôts de stockage"""
    __tablename__ = "warehouses"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    address = Column(Text)
    city = Column(String(100))
    country = Column(String(100))
    is_active = Column(Boolean, default=True)
    
    # Relations
    inventory_items = relationship("Inventory", back_populates="warehouse")

# Modèle utilisateur simplifié pour les relations
class User(Base):
    """Utilisateur simplifié pour les relations"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)

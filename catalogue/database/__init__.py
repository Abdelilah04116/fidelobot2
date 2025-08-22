"""
Module Database du Catalogue - Gestion de la base de données relationnelle
"""

from .catalog_models import (
    Base, Category, Brand, Product, ProductVariant, 
    ProductAttribute, ProductTag, ProductTagAssociation,
    ProductReview, ProductImage, Inventory, Warehouse, User,
    ProductStatus, ProductType
)

from .catalog_database import (
    CatalogDatabase, catalog_db, get_catalog_session, close_catalog_database
)

__all__ = [
    # Modèles
    "Base", "Category", "Brand", "Product", "ProductVariant",
    "ProductAttribute", "ProductTag", "ProductTagAssociation", 
    "ProductReview", "ProductImage", "Inventory", "Warehouse", "User",
    "ProductStatus", "ProductType",
    
    # Base de données
    "CatalogDatabase", "catalog_db", "get_catalog_session", "close_catalog_database"
]

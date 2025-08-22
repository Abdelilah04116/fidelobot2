"""
Gestionnaire Principal du Catalogue - Opérations CRUD complètes
Interface principale pour gérer les produits, catégories, marques, etc.
"""

from typing import List, Optional, Dict, Any, Union
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc
from sqlalchemy.exc import SQLAlchemyError
import logging
from datetime import datetime

from .database.catalog_models import (
    Product, Category, Brand, ProductVariant, ProductAttribute,
    ProductTag, ProductReview, Inventory, Warehouse
)
from .database.catalog_database import get_catalog_session

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CatalogManager:
    """Gestionnaire principal du catalogue des produits"""
    
    def __init__(self):
        """Initialise le gestionnaire de catalogue"""
        self.logger = logging.getLogger(__name__)
    
    # ==================== GESTION DES PRODUITS ====================
    
    def create_product(self, product_data: Dict[str, Any]) -> Optional[Product]:
        """
        Crée un nouveau produit
        
        Args:
            product_data: Données du produit
            
        Returns:
            Product: Produit créé ou None en cas d'erreur
        """
        try:
            with get_catalog_session() as session:
                product = Product(**product_data)
                session.add(product)
                session.commit()
                session.refresh(product)
                self.logger.info(f"Produit créé: {product.name}")
                return product
        except SQLAlchemyError as e:
            self.logger.error(f"Erreur lors de la création du produit: {e}")
            return None
    
    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Récupère un produit par son ID"""
        try:
            with get_catalog_session() as session:
                return session.query(Product).filter(Product.id == product_id).first()
        except SQLAlchemyError as e:
            self.logger.error(f"Erreur lors de la récupération du produit {product_id}: {e}")
            return None
    
    def get_product_by_sku(self, sku: str) -> Optional[Product]:
        """Récupère un produit par son SKU"""
        try:
            with get_catalog_session() as session:
                return session.query(Product).filter(Product.sku == sku).first()
        except SQLAlchemyError as e:
            self.logger.error(f"Erreur lors de la récupération du produit SKU {sku}: {e}")
            return None
    
    def get_product_by_slug(self, slug: str) -> Optional[Product]:
        """Récupère un produit par son slug"""
        try:
            with get_catalog_session() as session:
                return session.query(Product).filter(Product.slug == slug).first()
        except SQLAlchemyError as e:
            self.logger.error(f"Erreur lors de la récupération du produit slug {slug}: {e}")
            return None
    
    def search_products(self, 
                       query: str = None,
                       category_id: int = None,
                       brand_id: int = None,
                       min_price: float = None,
                       max_price: float = None,
                       in_stock: bool = None,
                       status: str = None,
                       limit: int = 50,
                       offset: int = 0) -> List[Product]:
        """
        Recherche avancée de produits
        
        Args:
            query: Terme de recherche
            category_id: ID de la catégorie
            brand_id: ID de la marque
            min_price: Prix minimum
            max_price: Prix maximum
            in_stock: En stock uniquement
            status: Statut du produit
            limit: Nombre maximum de résultats
            offset: Décalage pour la pagination
            
        Returns:
            List[Product]: Liste des produits correspondants
        """
        try:
            with get_catalog_session() as session:
                query_obj = session.query(Product)
                
                # Filtres de base
                if query:
                    search_term = f"%{query}%"
                    query_obj = query_obj.filter(
                        or_(
                            Product.name.ilike(search_term),
                            Product.description.ilike(search_term),
                            Product.short_description.ilike(search_term)
                        )
                    )
                
                if category_id:
                    query_obj = query_obj.filter(Product.category_id == category_id)
                
                if brand_id:
                    query_obj = query_obj.filter(Product.brand_id == brand_id)
                
                if min_price is not None:
                    query_obj = query_obj.filter(Product.base_price >= min_price)
                
                if max_price is not None:
                    query_obj = query_obj.filter(Product.base_price <= max_price)
                
                if in_stock is not None:
                    if in_stock:
                        query_obj = query_obj.filter(Product.stock_quantity > 0)
                    else:
                        query_obj = query_obj.filter(Product.stock_quantity == 0)
                
                if status:
                    query_obj = query_obj.filter(Product.status == status)
                
                # Tri et pagination
                query_obj = query_obj.order_by(desc(Product.created_at))
                query_obj = query_obj.offset(offset).limit(limit)
                
                return query_obj.all()
                
        except SQLAlchemyError as e:
            self.logger.error(f"Erreur lors de la recherche de produits: {e}")
            return []
    
    def update_product(self, product_id: int, update_data: Dict[str, Any]) -> bool:
        """Met à jour un produit"""
        try:
            with get_catalog_session() as session:
                product = session.query(Product).filter(Product.id == product_id).first()
                if not product:
                    return False
                
                for key, value in update_data.items():
                    if hasattr(product, key):
                        setattr(product, key, value)
                
                product.updated_at = datetime.utcnow()
                session.commit()
                self.logger.info(f"Produit {product_id} mis à jour")
                return True
                
        except SQLAlchemyError as e:
            self.logger.error(f"Erreur lors de la mise à jour du produit {product_id}: {e}")
            return False
    
    def delete_product(self, product_id: int) -> bool:
        """Supprime un produit"""
        try:
            with get_catalog_session() as session:
                product = session.query(Product).filter(Product.id == product_id).first()
                if not product:
                    return False
                
                session.delete(product)
                session.commit()
                self.logger.info(f"Produit {product_id} supprimé")
                return True
                
        except SQLAlchemyError as e:
            self.logger.error(f"Erreur lors de la suppression du produit {product_id}: {e}")
            return False
    
    # ==================== GESTION DES CATÉGORIES ====================
    
    def create_category(self, category_data: Dict[str, Any]) -> Optional[Category]:
        """Crée une nouvelle catégorie"""
        try:
            with get_catalog_session() as session:
                category = Category(**category_data)
                session.add(category)
                session.commit()
                session.refresh(category)
                return category
        except SQLAlchemyError as e:
            self.logger.error(f"Erreur lors de la création de la catégorie: {e}")
            return None
    
    def get_categories(self, parent_id: Optional[int] = None, active_only: bool = True) -> List[Category]:
        """Récupère les catégories"""
        try:
            with get_catalog_session() as session:
                query = session.query(Category)
                
                if parent_id is not None:
                    query = query.filter(Category.parent_id == parent_id)
                else:
                    query = query.filter(Category.parent_id.is_(None))
                
                if active_only:
                    query = query.filter(Category.is_active == True)
                
                return query.order_by(Category.sort_order, Category.name).all()
                
        except SQLAlchemyError as e:
            self.logger.error(f"Erreur lors de la récupération des catégories: {e}")
            return []
    
    # ==================== GESTION DES MARQUES ====================
    
    def create_brand(self, brand_data: Dict[str, Any]) -> Optional[Brand]:
        """Crée une nouvelle marque"""
        try:
            with get_catalog_session() as session:
                brand = Brand(**brand_data)
                session.add(brand)
                session.commit()
                session.refresh(brand)
                return brand
        except SQLAlchemyError as e:
            self.logger.error(f"Erreur lors de la création de la marque: {e}")
            return None
    
    def get_brands(self, active_only: bool = True) -> List[Brand]:
        """Récupère toutes les marques"""
        try:
            with get_catalog_session() as session:
                query = session.query(Brand)
                if active_only:
                    query = query.filter(Brand.is_active == True)
                return query.order_by(Brand.name).all()
        except SQLAlchemyError as e:
            self.logger.error(f"Erreur lors de la récupération des marques: {e}")
            return []
    
    # ==================== GESTION DES VARIANTES ====================
    
    def create_product_variant(self, variant_data: Dict[str, Any]) -> Optional[ProductVariant]:
        """Crée une variante de produit"""
        try:
            with get_catalog_session() as session:
                variant = ProductVariant(**variant_data)
                session.add(variant)
                session.commit()
                session.refresh(variant)
                return variant
        except SQLAlchemyError as e:
            self.logger.error(f"Erreur lors de la création de la variante: {e}")
            return None
    
    def get_product_variants(self, product_id: int) -> List[ProductVariant]:
        """Récupère les variantes d'un produit"""
        try:
            with get_catalog_session() as session:
                return session.query(ProductVariant).filter(
                    ProductVariant.product_id == product_id
                ).all()
        except SQLAlchemyError as e:
            self.logger.error(f"Erreur lors de la récupération des variantes: {e}")
            return []
    
    # ==================== GESTION DES STOCKS ====================
    
    def update_stock(self, product_id: int, quantity: int, variant_id: Optional[int] = None) -> bool:
        """Met à jour le stock d'un produit"""
        try:
            with get_catalog_session() as session:
                if variant_id:
                    # Mise à jour du stock d'une variante
                    inventory = session.query(Inventory).filter(
                        and_(
                            Inventory.product_id == product_id,
                            Inventory.variant_id == variant_id
                        )
                    ).first()
                    
                    if not inventory:
                        inventory = Inventory(
                            product_id=product_id,
                            variant_id=variant_id,
                            quantity=quantity
                        )
                        session.add(inventory)
                    else:
                        inventory.quantity = quantity
                else:
                    # Mise à jour du stock principal du produit
                    product = session.query(Product).filter(Product.id == product_id).first()
                    if product:
                        product.stock_quantity = quantity
                
                session.commit()
                return True
                
        except SQLAlchemyError as e:
            self.logger.error(f"Erreur lors de la mise à jour du stock: {e}")
            return False
    
    def get_low_stock_products(self, threshold: int = 5) -> List[Product]:
        """Récupère les produits en rupture de stock"""
        try:
            with get_catalog_session() as session:
                return session.query(Product).filter(
                    and_(
                        Product.stock_quantity <= threshold,
                        Product.track_stock == True
                    )
                ).all()
        except SQLAlchemyError as e:
            self.logger.error(f"Erreur lors de la récupération des produits en rupture: {e}")
            return []
    
    # ==================== STATISTIQUES ET RAPPORTS ====================
    
    def get_catalog_statistics(self) -> Dict[str, Any]:
        """Récupère les statistiques du catalogue"""
        try:
            with get_catalog_session() as session:
                total_products = session.query(Product).count()
                active_products = session.query(Product).filter(Product.status == "active").count()
                out_of_stock = session.query(Product).filter(Product.stock_quantity == 0).count()
                total_categories = session.query(Category).count()
                total_brands = session.query(Brand).count()
                
                return {
                    "total_products": total_products,
                    "active_products": active_products,
                    "out_of_stock": out_of_stock,
                    "total_categories": total_categories,
                    "total_brands": total_brands,
                    "stock_ratio": f"{(active_products - out_of_stock) / active_products * 100:.1f}%" if active_products > 0 else "0%"
                }
                
        except SQLAlchemyError as e:
            self.logger.error(f"Erreur lors de la récupération des statistiques: {e}")
            return {}

# Instance globale du gestionnaire de catalogue
catalog_manager = CatalogManager()

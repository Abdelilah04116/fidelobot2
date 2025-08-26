from .base_agent import BaseAgent
from typing import Dict, Any, List, Optional
import sys
import os

# Ajouter le chemin du projet pour importer le catalogue
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from catalogue.backend.database import SessionLocal
from catalogue.backend.models import Product, Category
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
import logging
from datetime import datetime
from catalogue.backend.qdrant_client import client as qdrant_client, search_embedding
# AGENT CONNECTÉ À QDRANT (vectoriel)
# Utilisez search_embedding(...) pour la recherche sémantique de produits

class ProductSearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="product_search_agent",
            description="Agent de recherche de produits optimisé et sécurisé"
        )
        self.logger = logging.getLogger(__name__)
        self.default_limit = 20
        self.max_limit = 100
    
    def get_system_prompt(self) -> str:
        return """
        Vous êtes un expert en recherche de produits e-commerce.
        Votre rôle est de trouver les produits les plus pertinents selon les critères.
        
        Capacités:
        - Rechercher des produits par nom, catégorie, marque
        - Vérifier la disponibilité en stock
        - Obtenir les prix et promotions
        - Analyser les avis clients
        
        Toujours fournir des informations précises et à jour.
        """
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            query = state.get("search_query", state.get("user_message", ""))
            category = state.get("category", "")
            max_price = state.get("max_price", None)
            limit = min(state.get("limit", self.default_limit), self.max_limit)
            
            # Valider les paramètres de recherche
            validation_result = self.validate_search_params(query, category, max_price, limit)
            if not validation_result["valid"]:
                state["products"] = []
                state["response_text"] = validation_result["error"]
                return state
            
            # Rechercher les produits avec gestion d'erreur
            search_result = await self.search_products_safe(query, category, max_price, limit)
            if search_result.get("error"):
                self.logger.error(f"Erreur recherche produits: {search_result['error']}")
                # Retourner une réponse utile même en cas d'erreur DB
                state["products"] = []
                state["response_text"] = f"Je ne peux pas accéder au catalogue pour le moment. Voici ce que je peux vous dire :\n\n- Votre recherche était : '{query}'\n- Je recommande de réessayer dans quelques minutes\n- En attendant, vous pouvez me demander des recommandations générales"
                return state
            
            products = search_result["products"]
            state["products"] = products
            
            # Enrichir avec les informations additionnelles
            enriched_result = await self.enrich_products_safe(products)
            if enriched_result.get("error"):
                self.logger.warning(f"Erreur enrichissement: {enriched_result['error']}")
                # Continuer avec les produits non enrichis
                products = enriched_result.get("products", products)
            else:
                products = enriched_result["products"]
            state["products"] = products
            
            # Générer un résumé simple pour la réponse utilisateur
            if products:
                state["response_text"] = f"J'ai trouvé {len(products)} produit(s) pour votre recherche '{query}'. Voici un exemple : {products[0]['name']} - {products[0].get('price', 'Prix non disponible')}"
            else:
                state["response_text"] = f"Aucun produit trouvé pour '{query}'. Essayez avec d'autres mots-clés ou demandez-moi des recommandations."
            return state
            
        except Exception as e:
            self.logger.error(f"Erreur critique dans ProductSearchAgent: {str(e)}")
            state["products"] = []
            state["response_text"] = "Désolé, je rencontre un problème technique. Pouvez-vous reformuler votre demande ?"
            return state
    
    def validate_search_params(self, query: str, category: str, max_price: float, limit: int) -> Dict[str, Any]:
        """Valider les paramètres de recherche"""
        # Validation de la requête
        if query and len(query.strip()) < 2:
            return {"valid": False, "error": "La requête de recherche doit contenir au moins 2 caractères"}
        
        # Validation du prix maximum
        if max_price is not None:
            try:
                max_price = float(max_price)
                if max_price < 0:
                    return {"valid": False, "error": "Le prix maximum ne peut pas être négatif"}
            except (ValueError, TypeError):
                return {"valid": False, "error": "Le prix maximum doit être un nombre valide"}
        
        # Validation de la limite
        if limit < 1 or limit > self.max_limit:
            return {"valid": False, "error": f"La limite doit être entre 1 et {self.max_limit}"}
        
        return {"valid": True}
    
    async def search_products_safe(self, query: str, category: str = "", max_price: float = None, limit: int = 20) -> Dict[str, Any]:
        """Rechercher des produits dans la base de données du catalogue de manière sécurisée"""
        session: Optional[Session] = None
        try:
            session = catalog_db.get_session_direct()
            
            # Construire la requête de base avec validation
            db_query = session.query(Product).filter(Product.status == ProductStatus.ACTIVE)
            
            # Ajouter les filtres de manière sécurisée
            if query and query.strip():
                search_term = f"%{query.strip()}%"
                db_query = db_query.filter(
                    or_(
                        Product.name.ilike(search_term),
                        Product.description.ilike(search_term),
                        Product.short_description.ilike(search_term)
                    )
                )
            
            if category and category.strip():
                # Rechercher par nom de catégorie
                category_query = session.query(Category).filter(
                    Category.name.ilike(f"%{category.strip()}%")
                ).first()
                if category_query:
                    db_query = db_query.filter(Product.category_id == category_query.id)
            
            if max_price is not None:
                try:
                    max_price = float(max_price)
                    db_query = db_query.filter(Product.base_price <= max_price)
                except (ValueError, TypeError):
                    self.logger.warning(f"Prix maximum invalide ignoré: {max_price}")
            
            # Appliquer la limite et récupérer les résultats
            products = db_query.limit(limit).all()
            
            # Convertir en dictionnaires de manière sécurisée
            product_dicts = []
            for product in products:
                try:
                    product_dict = self.product_to_dict_safe(product, session)
                    if product_dict:
                        product_dicts.append(product_dict)
                except Exception as e:
                    self.logger.warning(f"Erreur conversion produit {getattr(product, 'id', 'unknown')}: {str(e)}")
                    continue
            
            return {"products": product_dicts}
            
        except Exception as e:
            self.logger.error(f"Erreur recherche produits: {str(e)}")
            return {"error": str(e)}
        finally:
            if session:
                session.close()
    
    def product_to_dict_safe(self, product, session: Session) -> Optional[Dict[str, Any]]:
        """Convertir un produit en dictionnaire de manière sécurisée"""
        try:
            # Récupérer les informations de catégorie et marque
            category_name = "Inconnue"
            brand_name = "Inconnue"
            
            if hasattr(product, 'category_id') and product.category_id:
                category = session.query(Category).filter(Category.id == product.category_id).first()
                if category:
                    category_name = category.name
            
            if hasattr(product, 'brand_id') and product.brand_id:
                brand = session.query(Brand).filter(Brand.id == product.brand_id).first()
                if brand:
                    brand_name = brand.name
            
            product_dict = {
                "id": getattr(product, 'id', None),
                "sku": getattr(product, 'sku', ''),
                "name": getattr(product, 'name', 'Produit sans nom'),
                "description": getattr(product, 'description', ''),
                "short_description": getattr(product, 'short_description', ''),
                "base_price": float(getattr(product, 'base_price', 0)),
                "sale_price": float(getattr(product, 'sale_price', 0)) if getattr(product, 'sale_price', None) else None,
                "stock_quantity": int(getattr(product, 'stock_quantity', 0)),
                "category": category_name,
                "brand": brand_name,
                "main_image_url": getattr(product, 'main_image_url', ''),
                "status": getattr(product, 'status', ProductStatus.ACTIVE).value,
                "created_at": getattr(product, 'created_at', datetime.utcnow()).isoformat() if getattr(product, 'created_at', None) else None
            }
            
            # Ajouter le prix final (prix de vente ou prix de base)
            if product_dict["sale_price"] and product_dict["sale_price"] > 0:
                product_dict["final_price"] = product_dict["sale_price"]
            else:
                product_dict["final_price"] = product_dict["base_price"]
            
            return product_dict
            
        except Exception as e:
            self.logger.error(f"Erreur conversion produit en dictionnaire: {str(e)}")
            return None
    
    async def enrich_products_safe(self, products: List[Dict]) -> Dict[str, Any]:
        """Enrichir les produits avec des informations additionnelles de manière sécurisée"""
        if not products:
            return {"products": products}
        
        try:
            for product in products:
                try:
                    # Statut du stock de manière sécurisée
                    stock_quantity = product.get("stock_quantity", 0)
                    if stock_quantity > 10:
                        product["stock_status"] = "en_stock"
                        product["stock_level"] = "high"
                    elif stock_quantity > 0:
                        product["stock_status"] = "stock_limite"
                        product["stock_level"] = "medium"
                    else:
                        product["stock_status"] = "rupture"
                        product["stock_level"] = "low"
                    
                    # Ajouter des métadonnées utiles
                    product["last_updated"] = datetime.utcnow().isoformat()
                    
                    # Ajouter des informations de disponibilité
                    product["available"] = stock_quantity > 0
                    
                except Exception as e:
                    self.logger.warning(f"Erreur enrichissement produit {product.get('id', 'unknown')}: {str(e)}")
                    # Continuer avec les autres produits
                    continue
            
            return {"products": products}
            
        except Exception as e:
            self.logger.error(f"Erreur enrichissement produits: {str(e)}")
            return {"error": str(e), "products": products}
    
    async def get_categories(self) -> Dict[str, Any]:
        """Récupérer toutes les catégories disponibles"""
        session: Optional[Session] = None
        try:
            session = catalog_db.get_session_direct()
            
            categories = session.query(Category).filter(Category.is_active == True).all()
            
            category_list = []
            for category in categories:
                try:
                    category_dict = {
                        "id": getattr(category, 'id', None),
                        "name": getattr(category, 'name', ''),
                        "slug": getattr(category, 'slug', ''),
                        "description": getattr(category, 'description', ''),
                        "image_url": getattr(category, 'image_url', '')
                    }
                    category_list.append(category_dict)
                except Exception as e:
                    self.logger.warning(f"Erreur conversion catégorie {getattr(category, 'id', 'unknown')}: {str(e)}")
                    continue
            
            return {"categories": category_list, "total": len(category_list)}
            
        except Exception as e:
            self.logger.error(f"Erreur récupération catégories: {str(e)}")
            return {"error": str(e), "categories": [], "total": 0}
        finally:
            if session:
                session.close()
    
    async def get_popular_products(self, limit: int = 10) -> Dict[str, Any]:
        """Récupérer les produits populaires (en stock)"""
        session: Optional[Session] = None
        try:
            session = catalog_db.get_session_direct()
            
            # Récupérer les produits actifs avec stock
            products = session.query(Product).filter(
                and_(
                    Product.status == ProductStatus.ACTIVE,
                    Product.stock_quantity > 0
                )
            ).limit(limit).all()
            
            product_dicts = []
            for product in products:
                try:
                    product_dict = self.product_to_dict_safe(product, session)
                    if product_dict:
                        product_dicts.append(product_dict)
                except Exception as e:
                    self.logger.warning(f"Erreur conversion produit populaire {getattr(product, 'id', 'unknown')}: {str(e)}")
                    continue
            
            return {"products": product_dicts, "total": len(product_dicts)}
            
        except Exception as e:
            self.logger.error(f"Erreur récupération produits populaires: {str(e)}")
            return {"error": str(e), "products": [], "total": 0}
        finally:
            if session:
                session.close()

from .base_agent import BaseAgent
from typing import Dict, Any, List, Optional
import sys
import os
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from sentence_transformers import SentenceTransformer

# Import de la couche d'abstraction des bases de données
from ..core.db_connection import get_postgres_session, get_qdrant_client

# Import des modèles (à adapter selon ta structure)
try:
    from catalogue.backend.models import Product, Category
except ImportError:
    # Fallback si les modèles ne sont pas disponibles
    Product = Category = None
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
        # Modèle d'embedding léger compatible avec Qdrant (384)
        try:
            self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception:
            self.embedder = None
    
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
            
            # Rechercher en SQL d'abord
            search_result = await self.search_products_safe(query, category, max_price, limit)
            if search_result.get("error"):
                self.logger.error(f"Erreur recherche produits: {search_result['error']}")
                # Retourner une réponse utile même en cas d'erreur DB
                state["products"] = []
                state["response_text"] = f"Je ne peux pas accéder au catalogue pour le moment. Voici ce que je peux vous dire :\n\n- Votre recherche était : '{query}'\n- Je recommande de réessayer dans quelques minutes\n- En attendant, vous pouvez me demander des recommandations générales"
                return state
            
            products = search_result["products"]

            # Fallback: si SQL vide, essayer la similarité Qdrant sur le texte utilisateur
            if not products:
                qdrant_result = await self.semantic_search_fallback(query, limit)
                if qdrant_result.get("products"):
                    products = qdrant_result["products"]
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
            
            # Générer une réponse personnalisée selon le type de recherche
            if products:
                response_text = self.generate_personalized_response(query, products)
            else:
                response_text = f"Aucun produit trouvé pour '{query}'. Essayez avec d'autres mots-clés ou demandez-moi des recommandations."
            
            state["response_text"] = response_text
            state["response_type"] = "product_search"  # Éviter que le summarizer écrase la réponse
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

    def generate_personalized_response(self, query: str, products: List[Dict]) -> str:
        """Générer une réponse personnalisée selon le type de recherche"""
        query_lower = query.lower().strip()
        
        # Détecter le type de recherche
        if any(word in query_lower for word in ['avez', 'disponible', 'stock', 'avoir']):
            # Recherche de disponibilité
            if len(products) == 1:
                product = products[0]
                return f"✅ **Oui, nous avons le {product['name']} !**\n\n📱 **{product['name']}** - {product['price']}€\n📦 **Stock** : {product['stock_quantity']} unités disponibles\n📋 **Description** : {product['description']}\n🏷️ **Catégorie** : {product['category']}"
            else:
                # Plusieurs produits trouvés
                response = f"✅ **Oui, nous avons {len(products)} produit(s) correspondant à votre recherche !**\n\n"
                for i, product in enumerate(products[:5], 1):  # Limiter à 5 produits
                    response += f"{i}. **{product['name']}** - {product['price']}€ ({product['stock_quantity']} en stock)\n"
                if len(products) > 5:
                    response += f"\n... et {len(products) - 5} autre(s) produit(s)"
                return response
        
        elif any(word in query_lower for word in ['prix', 'coût', 'tarif', 'combien']):
            # Recherche de prix
            if len(products) == 1:
                product = products[0]
                return f"💰 **Prix du {product['name']} : {product['price']}€**\n\n📱 **{product['name']}**\n📦 **Stock** : {product['stock_quantity']} unités\n📋 **Description** : {product['description']}"
            else:
                response = f"💰 **Voici les prix pour {len(products)} produit(s) :**\n\n"
                for product in products[:5]:
                    response += f"• **{product['name']}** : {product['price']}€\n"
                return response
        
        else:
            # Recherche générale
            if len(products) == 1:
                product = products[0]
                return f"🔍 **J'ai trouvé exactement ce que vous cherchez !**\n\n📱 **{product['name']}** - {product['price']}€\n📦 **Stock** : {product['stock_quantity']} unités\n📋 **Description** : {product['description']}\n🏷️ **Catégorie** : {product['category']}"
            else:
                response = f"🔍 **J'ai trouvé {len(products)} produit(s) pour votre recherche :**\n\n"
                for i, product in enumerate(products[:5], 1):
                    response += f"{i}. **{product['name']}** - {product['price']}€\n"
                if len(products) > 5:
                    response += f"\n... et {len(products) - 5} autre(s) produit(s)"
                return response

    async def semantic_search_fallback(self, text_query: str, limit: int = 10) -> Dict[str, Any]:
        """Recherche sémantique via Qdrant et hydratation SQL des IDs retournés."""
        if not text_query or not text_query.strip():
            return {"products": []}
        if self.embedder is None:
            return {"products": []}
        try:
            # Encoder la requête
            embedding = self.embedder.encode(text_query)
            
            # Obtenir le client Qdrant via la couche d'abstraction
            qdrant_client = get_qdrant_client()
            
            # Interroger Qdrant
            search_result = qdrant_client.search(
                collection_name="produits_embeddings",
                query_vector=embedding.tolist(),
                limit=limit
            )
            
            product_ids = [hit.id for hit in search_result] if search_result else []
            if not product_ids:
                return {"products": []}
            
            # Hydrater via SQL
            with get_postgres_session() as session:
                rows = session.query(Product).filter(Product.id.in_(product_ids)).all()
                # Conserver l'ordre par score de Qdrant
                id_to_rank = {pid: i for i, pid in enumerate(product_ids)}
                hydrated = [self.product_to_dict_safe(p, session) for p in rows]
                hydrated = [p for p in hydrated if p]
                hydrated.sort(key=lambda x: id_to_rank.get(x.get("id"), 10**9))
                if hydrated:
                    return {"products": hydrated[:limit]}
                
                # Si aucune ligne SQL, retourner un fallback depuis les payloads Qdrant
                fallback = []
                for hit in search_result:
                    payload = hit.payload or {}
                    fallback.append({
                        "id": hit.id,
                        "name": payload.get("nom", f"Produit {hit.id}"),
                        "description": "",
                        "price": payload.get("prix"),
                        "stock_quantity": 0,
                        "category": payload.get("categorie", "Inconnue"),
                    })
                return {"products": fallback[:limit]}
                
        except Exception as e:
            self.logger.warning(f"Fallback Qdrant échoué: {e}")
            return {"products": []}
    
    async def search_products_safe(self, query: str, category: str = "", max_price: float = None, limit: int = 20) -> Dict[str, Any]:
        """Rechercher des produits dans la base de données du catalogue de manière sécurisée"""
        try:
            with get_postgres_session() as session:
                # Construire la requête de base avec validation
                db_query = session.query(Product)
                
                # Ajouter les filtres de manière sécurisée
                if query and query.strip():
                    # Nettoyer et extraire les mots-clés de la requête
                    clean_query = query.strip().lower()
                    
                    # Supprimer les mots de liaison courants
                    stop_words = ['est', 'ce', 'que', 'vous', 'avez', 'de', 'des', 'du', 'la', 'le', 'les', 'un', 'une', 'et', 'ou', 'avec', 'pour', 'dans', 'sur', 'par']
                    keywords = [word for word in clean_query.split() if word not in stop_words and len(word) > 2]
                    
                    if keywords:
                        # Recherche avec les mots-clés extraits
                        search_conditions = []
                        for keyword in keywords:
                            search_conditions.extend([
                                Product.nom.ilike(f"%{keyword}%"),
                                Product.description_courte.ilike(f"%{keyword}%")
                            ])
                        
                        # Recherche originale aussi (pour compatibilité)
                        search_conditions.extend([
                            Product.nom.ilike(f"%{clean_query}%"),
                            Product.description_courte.ilike(f"%{clean_query}%")
                        ])
                        
                        db_query = db_query.filter(or_(*search_conditions))
                    else:
                        # Fallback si pas de mots-clés valides
                        search_term = f"%{clean_query}%"
                        db_query = db_query.filter(
                            or_(
                                Product.nom.ilike(search_term),
                                Product.description_courte.ilike(search_term)
                            )
                        )
                
                if category and category.strip():
                    # Rechercher par nom de catégorie
                    category_query = session.query(Category).filter(
                        Category.nom.ilike(f"%{category.strip()}%")
                    ).first()
                    if category_query:
                        db_query = db_query.filter(Product.categorie_id == category_query.id)
                
                if max_price is not None:
                    try:
                        max_price = float(max_price)
                        db_query = db_query.filter(Product.prix <= max_price)
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
    
    def product_to_dict_safe(self, product, session: Session) -> Optional[Dict[str, Any]]:
        """Convertir un produit en dictionnaire de manière sécurisée"""
        try:
            # Récupérer la catégorie
            category_name = "Inconnue"
            if getattr(product, 'categorie_id', None):
                category = session.query(Category).filter(Category.id == product.categorie_id).first()
                if category:
                    category_name = getattr(category, 'nom', category_name)
            
            product_dict = {
                "id": getattr(product, 'id', None),
                "name": getattr(product, 'nom', 'Produit sans nom'),
                "description": getattr(product, 'description_courte', ''),
                "price": float(getattr(product, 'prix', 0) or 0),
                "stock_quantity": int(getattr(product, 'stock', 0) or 0),
                "category": category_name
            }
            
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
        try:
            with get_postgres_session() as session:
                categories = session.query(Category).all()
                
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
    
    async def get_popular_products(self, limit: int = 10) -> Dict[str, Any]:
        """Récupérer les produits populaires (en stock)"""
        try:
            with get_postgres_session() as session:
                # Récupérer les produits actifs avec stock
                products = session.query(Product).filter(
                    Product.stock > 0
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

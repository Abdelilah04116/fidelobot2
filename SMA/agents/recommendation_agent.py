from .base_agent import BaseAgent
from typing import Dict, Any, List, Optional
from ..models.database import SessionLocal, User, Product, Order, OrderItem, Rating
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
import logging
import math

class RecommendationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="recommendation_agent",
            description="Agent de recommandations personnalisées optimisé et sécurisé"
        )
        self.logger = logging.getLogger(__name__)
        self.default_limit = 10
        self.max_limit = 50
    
    def get_system_prompt(self) -> str:
        return """
        Vous êtes un expert en recommandations personnalisées.
        Votre rôle est de proposer les produits les plus pertinents pour chaque utilisateur.
        
        Méthodes:
        - Filtrage collaboratif (utilisateurs similaires)
        - Filtrage basé sur le contenu (produits similaires)
        - Règles métier (promotions, nouveautés, stock)
        - Analyse comportementale
        
        Personnalisez toujours selon le profil utilisateur.
        """
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            user_profile = state.get("user_profile", {})
            limit = 5
            # Appeler la logique de recommandation (à adapter selon votre projet)
            recommendations = await self.get_recommendations(user_profile, limit)
            state["recommendations"] = recommendations
            if recommendations:
                state["response_text"] = f"Voici {len(recommendations)} recommandation(s) personnalisée(s). Exemple : {recommendations[0]['name']}"
            else:
                state["response_text"] = "Aucune recommandation disponible pour le moment."
            return state
        except Exception as e:
            self.logger.error(f"Erreur dans RecommendationAgent: {str(e)}")
            state["recommendations"] = []
            state["response_text"] = "Erreur lors de la génération des recommandations."
            return state
    
    def validate_recommendation_params(self, user_id: Optional[int], recommendation_type: str, limit: int) -> Dict[str, Any]:
        """Valider les paramètres de recommandation"""
        if limit < 1 or limit > self.max_limit:
            return {"valid": False, "error": f"La limite doit être entre 1 et {self.max_limit}"}
        
        valid_types = ["general", "bestsellers", "promotions", "new", "trending", "personalized"]
        if recommendation_type not in valid_types:
            return {"valid": False, "error": f"Type de recommandation invalide. Types valides: {', '.join(valid_types)}"}
        
        return {"valid": True}
    
    async def get_personalized_recommendations_safe(self, user_id: int, rec_type: str, limit: int) -> Dict[str, Any]:
        """Recommandations personnalisées pour un utilisateur connecté de manière sécurisée"""
        db: Optional[Session] = None
        try:
            db = SessionLocal()
            
            # Vérifier que l'utilisateur existe
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return {"error": "Utilisateur non trouvé"}
            
            # Récupérer l'historique d'achat de manière optimisée
            user_orders = db.query(OrderItem).join(Order).filter(
                Order.user_id == user_id
            ).limit(100).all()  # Limiter pour éviter les surcharges
            
            if not user_orders:
                # Pas d'historique, utiliser des recommandations générales
                return await self.get_general_recommendations_safe(rec_type, limit)
            
            # Générer des recommandations basées sur différents critères
            recommendations = []
            
            # 1. Basé sur les catégories préférées
            category_recs = await self.get_category_based_recommendations(user_id, db, limit // 3)
            recommendations.extend(category_recs)
            
            # 2. Basé sur les marques préférées
            brand_recs = await self.get_brand_based_recommendations(user_id, db, limit // 3)
            recommendations.extend(brand_recs)
            
            # 3. Basé sur le comportement d'achat
            behavior_recs = await self.get_behavior_based_recommendations(user_id, db, limit // 3)
            recommendations.extend(behavior_recs)
            
            # Combiner et dédupliquer
            combined_recs = self.combine_and_deduplicate_recommendations(recommendations)
            
            return {"recommendations": combined_recs[:limit]}
            
        except Exception as e:
            self.logger.error(f"Erreur recommandations personnalisées: {str(e)}")
            return {"error": str(e)}
        finally:
            if db:
                db.close()
    
    async def get_category_based_recommendations(self, user_id: int, db: Session, limit: int) -> List[Dict]:
        """Recommandations basées sur les catégories préférées"""
        try:
            # Récupérer les catégories préférées de l'utilisateur
            user_categories = db.query(Product.category).join(OrderItem).join(Order).filter(
                Order.user_id == user_id
            ).distinct().all()
            
            categories = [cat[0] for cat in user_categories if cat[0]]
            
            if not categories:
                return []
            
            # Recommander des produits similaires dans les catégories préférées
            similar_products = db.query(Product).filter(
                Product.category.in_(categories),
                Product.is_active == True,
                Product.stock_quantity > 0
            ).order_by(desc(Product.rating)).limit(limit).all()
            
            recommendations = []
            for product in similar_products:
                recommendations.append({
                    "product_id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "category": product.category,
                    "brand": product.brand,
                    "score": 0.8,
                    "reason": f"Similaire à vos achats en {product.category}",
                    "type": "category_based"
                })
            
            return recommendations
            
        except Exception as e:
            self.logger.warning(f"Erreur recommandations par catégorie: {str(e)}")
            return []
    
    async def get_brand_based_recommendations(self, user_id: int, db: Session, limit: int) -> List[Dict]:
        """Recommandations basées sur les marques préférées"""
        try:
            # Analyser les marques préférées depuis l'historique
            brand_counts = {}
            orders = db.query(Order).filter(Order.user_id == user_id).limit(50).all()
            
            for order in orders:
                if hasattr(order, 'items') and order.items:
                    for item in order.items:
                        if hasattr(item, 'product') and item.product:
                            brand = getattr(item.product, 'brand', None)
                            if brand:
                                quantity = getattr(item, 'quantity', 1)
                                brand_counts[brand] = brand_counts.get(brand, 0) + quantity
            
            preferred_brands = sorted(brand_counts.items(), key=lambda x: x[1], reverse=True)[:3]
            
            if not preferred_brands:
                return []
            
            # Recommander des produits des marques préférées
            brand_names = [brand[0] for brand in preferred_brands]
            brand_products = db.query(Product).filter(
                Product.brand.in_(brand_names),
                Product.is_active == True,
                Product.stock_quantity > 0
            ).order_by(desc(Product.rating)).limit(limit).all()
            
            recommendations = []
            for product in brand_products:
                recommendations.append({
                    "product_id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "category": product.category,
                    "brand": product.brand,
                    "score": 0.7,
                    "reason": f"De votre marque préférée {product.brand}",
                    "type": "brand_based"
                })
            
            return recommendations
            
        except Exception as e:
            self.logger.warning(f"Erreur recommandations par marque: {str(e)}")
            return []
    
    async def get_behavior_based_recommendations(self, user_id: int, db: Session, limit: int) -> List[Dict]:
        """Recommandations basées sur le comportement d'achat"""
        try:
            # Analyser le comportement d'achat
            orders = db.query(Order).filter(Order.user_id == user_id).limit(20).all()
            
            if not orders:
                return []
            
            # Calculer la gamme de prix préférée
            total_spent = sum(getattr(order, 'total_amount', 0) for order in orders)
            avg_order_value = total_spent / len(orders) if orders else 0
            
            # Recommander des produits dans la même gamme de prix
            price_range = (avg_order_value * 0.5, avg_order_value * 1.5)
            
            behavior_products = db.query(Product).filter(
                Product.is_active == True,
                Product.stock_quantity > 0,
                Product.price.between(price_range[0], price_range[1])
            ).order_by(desc(Product.rating)).limit(limit).all()
            
            recommendations = []
            for product in behavior_products:
                recommendations.append({
                    "product_id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "category": product.category,
                    "brand": product.brand,
                    "score": 0.6,
                    "reason": "Similaire à vos habitudes d'achat",
                    "type": "behavior_based"
                })
            
            return recommendations
            
        except Exception as e:
            self.logger.warning(f"Erreur recommandations comportementales: {str(e)}")
            return []
    
    def combine_and_deduplicate_recommendations(self, recommendations: List[Dict]) -> List[Dict]:
        """Combiner et dédupliquer les recommandations"""
        seen_products = set()
        combined = []
        
        for rec in recommendations:
            product_id = rec.get("product_id")
            if product_id and product_id not in seen_products:
                seen_products.add(product_id)
                combined.append(rec)
        
        # Trier par score
        combined.sort(key=lambda x: x.get("score", 0), reverse=True)
        
        return combined
    
    async def get_general_recommendations_safe(self, rec_type: str, limit: int) -> Dict[str, Any]:
        """Recommandations générales pour les utilisateurs non connectés de manière sécurisée"""
        db: Optional[Session] = None
        try:
            db = SessionLocal()
            
            if rec_type == "bestsellers":
                # Produits les plus vendus
                products = db.query(Product).join(OrderItem).filter(
                    Product.is_active == True,
                    Product.stock_quantity > 0
                ).group_by(Product.id).order_by(
                    func.count(OrderItem.id).desc()
                ).limit(limit).all()
                
            elif rec_type == "promotions":
                # Produits en promotion (critères simplifiés)
                products = db.query(Product).filter(
                    Product.is_active == True,
                    Product.stock_quantity > 0,
                    Product.price < 100  # Critère de promotion simplifié
                ).order_by(desc(Product.rating)).limit(limit).all()
                
            elif rec_type == "new":
                # Nouveaux produits
                products = db.query(Product).filter(
                    Product.is_active == True,
                    Product.stock_quantity > 0
                ).order_by(desc(Product.created_at)).limit(limit).all()
                
            elif rec_type == "trending":
                # Produits tendance (basés sur les notes)
                products = db.query(Product).filter(
                    Product.is_active == True,
                    Product.stock_quantity > 0,
                    Product.rating >= 4.0
                ).order_by(desc(Product.rating)).limit(limit).all()
                
            else:
                # Recommandations par défaut
                products = db.query(Product).filter(
                    Product.is_active == True,
                    Product.stock_quantity > 0
                ).order_by(desc(Product.rating)).limit(limit).all()
            
            recommendations = []
            for product in products:
                recommendations.append({
                    "product_id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "category": product.category,
                    "brand": product.brand,
                    "score": 0.5,
                    "reason": f"Recommandé {rec_type}",
                    "type": rec_type
                })
            
            return {"recommendations": recommendations}
            
        except Exception as e:
            self.logger.error(f"Erreur recommandations générales: {str(e)}")
            return {"error": str(e)}
        finally:
            if db:
                db.close()
    
    async def apply_business_rules_safe(self, recommendations: List[Dict], user_profile: Dict) -> List[Dict]:
        """Appliquer les règles métier aux recommandations de manière sécurisée"""
        try:
            if not recommendations:
                return []
            
            # Prioriser les produits en stock
            in_stock_recs = [r for r in recommendations if r.get("stock_quantity", 0) > 0]
            
            # Appliquer les préférences utilisateur si disponibles
            if user_profile and user_profile.get("preferred_brands"):
                preferred_brands = user_profile["preferred_brands"]
                for rec in in_stock_recs:
                    if rec.get("brand") in preferred_brands:
                        rec["score"] = rec.get("score", 0) + 0.2
                        rec["reason"] += " (Marque préférée)"
            
            # Appliquer les préférences de catégorie
            if user_profile and user_profile.get("favorite_categories"):
                favorite_categories = user_profile["favorite_categories"]
                for rec in in_stock_recs:
                    if rec.get("category") in favorite_categories:
                        rec["score"] = rec.get("score", 0) + 0.1
                        rec["reason"] += " (Catégorie préférée)"
            
            # Trier par score final
            final_recs = sorted(in_stock_recs, key=lambda x: x.get("score", 0), reverse=True)
            
            return final_recs
            
        except Exception as e:
            self.logger.error(f"Erreur application règles métier: {str(e)}")
            return recommendations  # Retourner les recommandations originales en cas d'erreur
    
    def product_to_dict_safe(self, product: Product) -> Optional[Dict]:
        """Convertir un produit en dictionnaire de manière sécurisée"""
        try:
            return {
                "product_id": getattr(product, 'id', None),
                "name": getattr(product, 'name', 'Nom non disponible'),
                "description": getattr(product, 'description', 'Description non disponible'),
                "price": round(float(getattr(product, 'price', 0)), 2),
                "category": getattr(product, 'category', 'Catégorie non définie'),
                "brand": getattr(product, 'brand', 'Marque non définie'),
                "stock_quantity": int(getattr(product, 'stock_quantity', 0)),
                "image_url": getattr(product, 'image_url', None),
                "rating": round(float(getattr(product, 'rating', 0)), 1),
                "score": 0.5,  # Score par défaut
                "reason": "Recommandé pour vous",
                "type": "general"
            }
        except Exception as e:
            self.logger.error(f"Erreur conversion produit: {str(e)}")
            return None

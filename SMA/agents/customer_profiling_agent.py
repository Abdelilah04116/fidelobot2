from .base_agent import BaseAgent
from typing import Dict, Any, Optional
from catalogue.backend.database import SessionLocal
from catalogue.backend.models import User, Order, OrderItem, Product
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
import logging
from catalogue.backend.qdrant_client import client as qdrant_client, search_embedding
# AGENT CONNECTÉ À QDRANT (vectoriel)
# Utilisez search_embedding(...) pour la recherche de profils utilisateurs

class CustomerProfilingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="customer_profiling_agent",
            description="Agent de profilage client optimisé et sécurisé"
        )
        self.logger = logging.getLogger(__name__)
    
    def get_system_prompt(self) -> str:
        return """
        Vous êtes un expert en analyse de profils clients.
        Votre rôle est d'analyser le comportement d'achat et les préférences.
        
        Analyses:
        - Historique d'achats
        - Préférences déclarées
        - Comportement de navigation
        - Feedback et évaluations
        - Segmentation client
        
        Utilisez ces données pour personnaliser l'expérience.
        """
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            user_id = state.get("user_id")
            
            if not user_id:
                return {"profile": self.get_anonymous_profile()}
            
            # Analyser le profil complet avec gestion d'erreur
            profile = await self.analyze_user_profile_safe(user_id)
            
            if profile.get("error"):
                self.logger.error(f"Erreur lors de l'analyse du profil: {profile['error']}")
                return {"profile": self.get_anonymous_profile(), "error": profile["error"]}
            
            # Mettre à jour le profil en base de manière sécurisée
            update_result = await self.update_user_profile_safe(user_id, profile)
            
            return {"profile": profile, "update_success": update_result.get("success", False)}
            
        except Exception as e:
            self.logger.error(f"Erreur critique dans CustomerProfilingAgent: {str(e)}")
            return {"profile": self.get_anonymous_profile(), "error": "Erreur technique"}
    
    async def analyze_user_profile_safe(self, user_id: int) -> Dict[str, Any]:
        """Analyser le profil complet d'un utilisateur avec gestion d'erreur robuste"""
        db: Optional[Session] = None
        try:
            db = SessionLocal()
            
            # Vérifier que l'utilisateur existe
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return {"error": "Utilisateur non trouvé"}
            
            # Analyser l'historique d'achat avec gestion d'erreur
            purchase_history = await self.analyze_purchase_history_safe(user_id, db)
            if purchase_history.get("error"):
                return {"error": f"Erreur analyse historique: {purchase_history['error']}"}
            
            # Analyser les préférences avec gestion d'erreur
            preferences = await self.analyze_preferences_safe(user_id, db)
            if preferences.get("error"):
                return {"error": f"Erreur analyse préférences: {preferences['error']}"}
            
            # Calculer la valeur client avec gestion d'erreur
            customer_value = await self.calculate_customer_value_safe(user_id, db)
            if customer_value.get("error"):
                return {"error": f"Erreur calcul valeur: {customer_value['error']}"}
            
            # Déterminer le segment client avec gestion d'erreur
            segment = await self.determine_customer_segment_safe(user_id, db)
            if segment.get("error"):
                return {"error": f"Erreur segmentation: {segment['error']}"}
            
            profile = {
                "user_id": user_id,
                "username": getattr(user, 'username', 'Unknown'),
                "is_vip": getattr(user, 'is_vip', False),
                "purchase_history": purchase_history,
                "preferences": preferences,
                "customer_value": customer_value,
                "segment": segment,
                "last_updated": datetime.utcnow().isoformat()
            }
            
            return profile
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'analyse du profil: {str(e)}")
            return {"error": f"Erreur technique: {str(e)}"}
        finally:
            if db:
                db.close()
    
    async def analyze_purchase_history_safe(self, user_id: int, db: Session) -> Dict[str, Any]:
        """Analyser l'historique d'achat de manière sécurisée"""
        try:
            # Requête optimisée avec index sur user_id et created_at
            orders = db.query(Order).filter(
                Order.user_id == user_id
            ).order_by(Order.created_at.desc()).limit(100).all()  # Limiter pour éviter les surcharges
            
            if not orders:
                return {"total_orders": 0, "total_spent": 0, "favorite_categories": []}
            
            total_spent = sum(getattr(order, 'total_amount', 0) for order in orders)
            total_orders = len(orders)
            
            # Analyser les catégories favorites de manière optimisée
            category_counts = {}
            for order in orders:
                if hasattr(order, 'items') and order.items:
                    for item in order.items:
                        if hasattr(item, 'product') and item.product:
                            category = getattr(item.product, 'category', 'unknown')
                            quantity = getattr(item, 'quantity', 1)
                            category_counts[category] = category_counts.get(category, 0) + quantity
            
            favorite_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
            
            # Calculs RFM sécurisés
            last_order_date = max(getattr(order, 'created_at', datetime.utcnow()) for order in orders)
            days_since_last_order = (datetime.utcnow() - last_order_date).days
            
            return {
                "total_orders": total_orders,
                "total_spent": round(total_spent, 2),
                "average_order_value": round(total_spent / total_orders, 2) if total_orders > 0 else 0,
                "favorite_categories": [cat[0] for cat in favorite_categories[:5]],
                "days_since_last_order": days_since_last_order,
                "order_frequency": round(total_orders / max(1, days_since_last_order / 30), 2)
            }
            
        except Exception as e:
            self.logger.error(f"Erreur analyse historique: {str(e)}")
            return {"error": str(e)}
    
    async def analyze_preferences_safe(self, user_id: int, db: Session) -> Dict[str, Any]:
        """Analyser les préférences utilisateur de manière sécurisée"""
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return {"error": "Utilisateur non trouvé"}
            
            stored_preferences = getattr(user, 'preferences', {}) or {}
            
            # Analyser les marques préférées de manière optimisée
            brand_counts = {}
            orders = db.query(Order).filter(Order.user_id == user_id).limit(50).all()  # Limiter les requêtes
            
            for order in orders:
                if hasattr(order, 'items') and order.items:
                    for item in order.items:
                        if hasattr(item, 'product') and item.product:
                            brand = getattr(item.product, 'brand', None)
                            if brand:
                                quantity = getattr(item, 'quantity', 1)
                                brand_counts[brand] = brand_counts.get(brand, 0) + quantity
            
            preferred_brands = sorted(brand_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            
            # Analyser les gammes de prix de manière sécurisée
            price_ranges = {"low": 0, "medium": 0, "high": 0}
            for order in orders:
                if hasattr(order, 'items') and order.items:
                    for item in order.items:
                        price = getattr(item, 'price', 0)
                        if price < 50:
                            price_ranges["low"] += 1
                        elif price < 200:
                            price_ranges["medium"] += 1
                        else:
                            price_ranges["high"] += 1
            
            preferred_price_range = max(price_ranges, key=price_ranges.get) if any(price_ranges.values()) else "medium"
            
            return {
                **stored_preferences,
                "preferred_brands": [brand[0] for brand in preferred_brands],
                "preferred_price_range": preferred_price_range,
                "price_sensitivity": price_ranges
            }
            
        except Exception as e:
            self.logger.error(f"Erreur analyse préférences: {str(e)}")
            return {"error": str(e)}
    
    async def calculate_customer_value_safe(self, user_id: int, db: Session) -> Dict[str, Any]:
        """Calculer la valeur du client de manière sécurisée"""
        try:
            orders = db.query(Order).filter(Order.user_id == user_id).limit(100).all()
            
            if not orders:
                return {"ltv": 0, "clv_score": "low"}
            
            total_spent = sum(getattr(order, 'total_amount', 0) for order in orders)
            num_orders = len(orders)
            
            # Calculer la durée de relation client de manière sécurisée
            order_dates = [getattr(order, 'created_at', datetime.utcnow()) for order in orders]
            first_order = min(order_dates)
            customer_age_days = (datetime.utcnow() - first_order).days
            customer_age_months = max(1, customer_age_days / 30)
            
            # LTV estimée avec validation
            monthly_value = total_spent / customer_age_months if customer_age_months > 0 else 0
            estimated_ltv = monthly_value * 24  # Projection sur 2 ans
            
            # Score CLV avec validation
            if estimated_ltv > 1000:
                clv_score = "high"
            elif estimated_ltv > 500:
                clv_score = "medium"
            else:
                clv_score = "low"
            
            return {
                "ltv": round(estimated_ltv, 2),
                "clv_score": clv_score,
                "monthly_value": round(monthly_value, 2),
                "customer_age_months": round(customer_age_months, 1)
            }
            
        except Exception as e:
            self.logger.error(f"Erreur calcul valeur client: {str(e)}")
            return {"error": str(e)}
    
    async def determine_customer_segment_safe(self, user_id: int, db: Session) -> Dict[str, Any]:
        """Déterminer le segment client de manière sécurisée"""
        try:
            orders = db.query(Order).filter(Order.user_id == user_id).limit(50).all()
            
            if not orders:
                return {"segment": "new_customer", "confidence": 1.0}
            
            # Analyser la récence et fréquence de manière sécurisée
            order_dates = [getattr(order, 'created_at', datetime.utcnow()) for order in orders]
            last_order = max(order_dates)
            days_since_last_order = (datetime.utcnow() - last_order).days
            total_spent = sum(getattr(order, 'total_amount', 0) for order in orders)
            num_orders = len(orders)
            
            # Segmentation RFM améliorée avec validation
            if days_since_last_order <= 30 and total_spent > 500 and num_orders >= 5:
                segment = "champion"
                confidence = 0.9
            elif days_since_last_order <= 60 and total_spent > 200:
                segment = "loyal_customer"
                confidence = 0.8
            elif days_since_last_order <= 90:
                segment = "potential_loyalist"
                confidence = 0.7
            elif days_since_last_order <= 180:
                segment = "at_risk"
                confidence = 0.6
            else:
                segment = "hibernating"
                confidence = 0.5
            
            return {
                "segment": segment,
                "confidence": confidence,
                "rfm_score": {
                    "recency_days": days_since_last_order,
                    "frequency_orders": num_orders,
                    "monetary_total": round(total_spent, 2)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Erreur segmentation client: {str(e)}")
            return {"error": str(e)}
    
    def get_anonymous_profile(self) -> Dict[str, Any]:
        """Profil par défaut pour les utilisateurs anonymes"""
        return {
            "user_id": None,
            "segment": "anonymous",
            "preferences": {},
            "customer_value": {"ltv": 0, "clv_score": "unknown"},
            "purchase_history": {"total_orders": 0, "total_spent": 0}
        }
    
    async def update_user_profile_safe(self, user_id: int, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Mettre à jour le profil utilisateur en base de manière sécurisée"""
        db: Optional[Session] = None
        try:
            db = SessionLocal()
            user = db.query(User).filter(User.id == user_id).first()
            
            if not user:
                return {"success": False, "error": "Utilisateur non trouvé"}
            
            # Extraire seulement les préférences pour le stockage de manière sécurisée
            preferences_to_store = {
                "preferred_brands": profile.get("preferences", {}).get("preferred_brands", []),
                "preferred_price_range": profile.get("preferences", {}).get("preferred_price_range", "medium"),
                "favorite_categories": profile.get("purchase_history", {}).get("favorite_categories", []),
                "segment": profile.get("segment", {}).get("segment", "unknown"),
                "clv_score": profile.get("customer_value", {}).get("clv_score", "unknown"),
                "last_updated": datetime.utcnow().isoformat()
            }
            
            # Mettre à jour de manière sécurisée
            if hasattr(user, 'preferences'):
                user.preferences = preferences_to_store
                db.commit()
                return {"success": True, "updated_fields": list(preferences_to_store.keys())}
            else:
                return {"success": False, "error": "Champ preferences non disponible"}
                
        except Exception as e:
            if db:
                db.rollback()
            self.logger.error(f"Erreur mise à jour profil: {str(e)}")
            return {"success": False, "error": str(e)}
        finally:
            if db:
                db.close()

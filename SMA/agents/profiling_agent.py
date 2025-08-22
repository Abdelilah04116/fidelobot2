"""
Agent de profilage client - analyse le comportement utilisateur
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import numpy as np

from .base_agent import BaseAgent
from models.message_models import AgentMessage, MessageType, MessageMetadata
from models.agent_models import AgentType, AgentCapability, AgentResponse
from models.context_models import UserContext

logger = logging.getLogger(__name__)

class CustomerProfilingAgent(BaseAgent):
    """Agent de profilage et analyse comportementale des clients"""
    
    def __init__(self, config: Dict[str, Any], db_manager):
        super().__init__("profiling", AgentType.PROFILING, config)
        self.db_manager = db_manager
        self.capabilities = [
            AgentCapability.PROFILING
        ]
    
    def can_handle(self, message: AgentMessage) -> bool:
        """Peut gérer les demandes de profilage et d'analyse comportementale"""
        # Cet agent fonctionne en arrière-plan, pas directement avec les messages utilisateur
        return False
    
    async def process(self, message: AgentMessage, context: UserContext) -> AgentResponse:
        """Traite une demande de profilage (appelé par d'autres agents)"""
        try:
            # 1. Analyser le comportement utilisateur
            user_profile = await self._analyze_user_behavior(context.user_id)
            
            # 2. Mettre à jour le profil utilisateur
            await self._update_user_profile(context.user_id, user_profile)
            
            # 3. Générer des insights
            insights = await self._generate_insights(user_profile, context)
            
            return AgentResponse(
                success=True,
                content="Profil utilisateur mis à jour",
                metadata={
                    "user_profile": user_profile,
                    "insights": insights
                }
            )
            
        except Exception as e:
            logger.error(f"Error in profiling agent: {str(e)}")
            return AgentResponse(
                success=False,
                content="Erreur lors de l'analyse du profil",
                error_message=str(e)
            )
    
    async def _analyze_user_behavior(self, user_id: str) -> Dict[str, Any]:
        """Analyse le comportement d'un utilisateur"""
        try:
            # Récupérer les données utilisateur
            user_data = await self._collect_user_data(user_id)
            
            # Analyser les patterns
            profile = {
                "user_id": user_id,
                "last_updated": datetime.now(),
                "behavior_patterns": {},
                "preferences": {},
                "segments": [],
                "engagement_score": 0.0,
                "lifetime_value": 0.0
            }
            
            # Analyser les commandes
            if user_data.get("orders"):
                profile.update(await self._analyze_order_behavior(user_data["orders"]))
            
            # Analyser les conversations
            if user_data.get("conversations"):
                profile.update(await self._analyze_conversation_behavior(user_data["conversations"]))
            
            # Analyser les produits consultés
            if user_data.get("viewed_products"):
                profile.update(await self._analyze_product_behavior(user_data["viewed_products"]))
            
            # Calculer le score d'engagement
            profile["engagement_score"] = self._calculate_engagement_score(user_data)
            
            # Déterminer les segments
            profile["segments"] = self._determine_user_segments(profile)
            
            return profile
            
        except Exception as e:
            logger.error(f"Error analyzing user behavior: {e}")
            return {"user_id": user_id, "error": str(e)}
    
    async def _collect_user_data(self, user_id: str) -> Dict[str, Any]:
        """Collecte toutes les données d'un utilisateur"""
        try:
            with self.db_manager.get_session() as session:
                # Récupérer l'utilisateur
                user = session.query(User).filter_by(id=user_id).first()
                
                # Récupérer les commandes
                orders = session.query(Order).filter_by(user_id=user_id).all()
                
                # Récupérer les conversations
                conversations = session.query(Conversation).filter_by(user_id=user_id).all()
                
                # Récupérer les produits consultés (simulation)
                viewed_products = self._get_viewed_products(user_id)
                
                return {
                    "user": user,
                    "orders": [
                        {
                            "id": order.id,
                            "status": order.status,
                            "total": order.total,
                            "items": order.items or [],
                            "created_at": order.created_at
                        }
                        for order in orders
                    ],
                    "conversations": [
                        {
                            "id": conv.id,
                            "messages": conv.messages or [],
                            "intent": conv.intent,
                            "sentiment_score": conv.sentiment_score,
                            "created_at": conv.created_at
                        }
                        for conv in conversations
                    ],
                    "viewed_products": viewed_products
                }
                
        except Exception as e:
            logger.error(f"Error collecting user data: {e}")
            return {}
    
    def _get_viewed_products(self, user_id: str) -> List[Dict[str, Any]]:
        """Récupère les produits consultés par l'utilisateur (simulation)"""
        # En réalité, cela viendrait d'une table de tracking
        return [
            {"product_id": "prod_001", "category": "électronique", "viewed_at": datetime.now() - timedelta(days=1)},
            {"product_id": "prod_002", "category": "vêtements", "viewed_at": datetime.now() - timedelta(days=2)},
            {"product_id": "prod_003", "category": "électronique", "viewed_at": datetime.now() - timedelta(days=3)}
        ]
    
    async def _analyze_order_behavior(self, orders: List[Dict]) -> Dict[str, Any]:
        """Analyse le comportement d'achat"""
        if not orders:
            return {}
        
        # Calculer les métriques d'achat
        total_orders = len(orders)
        total_spent = sum(order["total"] for order in orders)
        avg_order_value = total_spent / total_orders if total_orders > 0 else 0
        
        # Analyser les catégories préférées
        category_counts = {}
        for order in orders:
            for item in order.get("items", []):
                category = item.get("category", "unknown")
                category_counts[category] = category_counts.get(category, 0) + 1
        
        # Analyser la fréquence d'achat
        if len(orders) > 1:
            order_dates = [order["created_at"] for order in orders]
            order_dates.sort()
            
            intervals = []
            for i in range(1, len(order_dates)):
                interval = (order_dates[i] - order_dates[i-1]).days
                intervals.append(interval)
            
            avg_interval = np.mean(intervals) if intervals else 0
        else:
            avg_interval = 0
        
        return {
            "order_behavior": {
                "total_orders": total_orders,
                "total_spent": total_spent,
                "avg_order_value": avg_order_value,
                "preferred_categories": sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:3],
                "avg_days_between_orders": avg_interval,
                "last_order_date": max(order["created_at"] for order in orders) if orders else None
            }
        }
    
    async def _analyze_conversation_behavior(self, conversations: List[Dict]) -> Dict[str, Any]:
        """Analyse le comportement de conversation"""
        if not conversations:
            return {}
        
        # Analyser les intentions
        intent_counts = {}
        sentiment_scores = []
        message_counts = []
        
        for conv in conversations:
            intent = conv.get("intent", "unknown")
            intent_counts[intent] = intent_counts.get(intent, 0) + 1
            
            sentiment = conv.get("sentiment_score", 0)
            sentiment_scores.append(sentiment)
            
            message_count = len(conv.get("messages", []))
            message_counts.append(message_count)
        
        # Calculer les métriques
        avg_sentiment = np.mean(sentiment_scores) if sentiment_scores else 0
        avg_message_count = np.mean(message_counts) if message_counts else 0
        total_conversations = len(conversations)
        
        return {
            "conversation_behavior": {
                "total_conversations": total_conversations,
                "avg_sentiment": avg_sentiment,
                "avg_messages_per_conversation": avg_message_count,
                "common_intents": sorted(intent_counts.items(), key=lambda x: x[1], reverse=True)[:3],
                "last_conversation_date": max(conv["created_at"] for conv in conversations) if conversations else None
            }
        }
    
    async def _analyze_product_behavior(self, viewed_products: List[Dict]) -> Dict[str, Any]:
        """Analyse le comportement de consultation de produits"""
        if not viewed_products:
            return {}
        
        # Analyser les catégories consultées
        category_counts = {}
        for product in viewed_products:
            category = product.get("category", "unknown")
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # Analyser la fréquence de consultation
        view_dates = [product["viewed_at"] for product in viewed_products]
        view_dates.sort()
        
        if len(view_dates) > 1:
            intervals = []
            for i in range(1, len(view_dates)):
                interval = (view_dates[i] - view_dates[i-1]).days
                intervals.append(interval)
            
            avg_interval = np.mean(intervals) if intervals else 0
        else:
            avg_interval = 0
        
        return {
            "product_behavior": {
                "total_products_viewed": len(viewed_products),
                "preferred_categories": sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:3],
                "avg_days_between_views": avg_interval,
                "last_view_date": max(product["viewed_at"] for product in viewed_products) if viewed_products else None
            }
        }
    
    def _calculate_engagement_score(self, user_data: Dict[str, Any]) -> float:
        """Calcule un score d'engagement utilisateur"""
        score = 0.0
        
        # Score basé sur les commandes
        orders = user_data.get("orders", [])
        if orders:
            score += min(len(orders) * 10, 50)  # Max 50 points pour les commandes
        
        # Score basé sur les conversations
        conversations = user_data.get("conversations", [])
        if conversations:
            score += min(len(conversations) * 5, 25)  # Max 25 points pour les conversations
        
        # Score basé sur les produits consultés
        viewed_products = user_data.get("viewed_products", [])
        if viewed_products:
            score += min(len(viewed_products) * 2, 15)  # Max 15 points pour les consultations
        
        # Score basé sur la récence
        if orders:
            last_order = max(order["created_at"] for order in orders)
            days_since_last_order = (datetime.now() - last_order).days
            if days_since_last_order <= 7:
                score += 10
            elif days_since_last_order <= 30:
                score += 5
        
        return min(score, 100)  # Cap à 100
    
    def _determine_user_segments(self, profile: Dict[str, Any]) -> List[str]:
        """Détermine les segments utilisateur"""
        segments = []
        
        # Segment basé sur la valeur
        order_behavior = profile.get("order_behavior", {})
        total_spent = order_behavior.get("total_spent", 0)
        
        if total_spent > 1000:
            segments.append("high_value")
        elif total_spent > 100:
            segments.append("medium_value")
        else:
            segments.append("low_value")
        
        # Segment basé sur l'engagement
        engagement_score = profile.get("engagement_score", 0)
        
        if engagement_score > 70:
            segments.append("high_engagement")
        elif engagement_score > 30:
            segments.append("medium_engagement")
        else:
            segments.append("low_engagement")
        
        # Segment basé sur la fréquence
        avg_interval = order_behavior.get("avg_days_between_orders", 0)
        
        if avg_interval <= 7:
            segments.append("frequent_buyer")
        elif avg_interval <= 30:
            segments.append("regular_buyer")
        else:
            segments.append("occasional_buyer")
        
        # Segment basé sur les préférences
        preferred_categories = order_behavior.get("preferred_categories", [])
        if preferred_categories:
            top_category = preferred_categories[0][0]
            segments.append(f"{top_category}_lover")
        
        return segments
    
    async def _update_user_profile(self, user_id: str, profile: Dict[str, Any]):
        """Met à jour le profil utilisateur dans la base de données"""
        try:
            with self.db_manager.get_session() as session:
                user = session.query(User).filter_by(id=user_id).first()
                
                if user:
                    user.profile = profile
                    session.commit()
                    
                    # Sauvegarder aussi dans MongoDB pour l'analytics
                    self.db_manager.mongo_db.user_profiles.update_one(
                        {"user_id": user_id},
                        {"$set": profile},
                        upsert=True
                    )
                    
        except Exception as e:
            logger.error(f"Error updating user profile: {e}")
    
    async def _generate_insights(self, profile: Dict[str, Any], context: UserContext) -> List[str]:
        """Génère des insights basés sur le profil"""
        insights = []
        
        # Insight sur la valeur client
        order_behavior = profile.get("order_behavior", {})
        total_spent = order_behavior.get("total_spent", 0)
        
        if total_spent > 500:
            insights.append("client_high_value")
        elif total_spent == 0:
            insights.append("client_no_purchase")
        
        # Insight sur l'engagement
        engagement_score = profile.get("engagement_score", 0)
        
        if engagement_score < 20:
            insights.append("client_low_engagement")
        elif engagement_score > 80:
            insights.append("client_high_engagement")
        
        # Insight sur les préférences
        preferred_categories = order_behavior.get("preferred_categories", [])
        if preferred_categories:
            top_category = preferred_categories[0][0]
            insights.append(f"prefers_{top_category}")
        
        # Insight sur la récence
        last_order_date = order_behavior.get("last_order_date")
        if last_order_date:
            days_since_last_order = (datetime.now() - last_order_date).days
            if days_since_last_order > 90:
                insights.append("client_at_risk")
            elif days_since_last_order > 30:
                insights.append("client_needs_reactivation")
        
        return insights
    
    async def get_user_recommendations(self, user_id: str) -> List[Dict[str, Any]]:
        """Génère des recommandations personnalisées pour un utilisateur"""
        try:
            # Récupérer le profil utilisateur
            profile_doc = self.db_manager.mongo_db.user_profiles.find_one({"user_id": user_id})
            
            if not profile_doc:
                return []
            
            profile = profile_doc
            
            # Générer des recommandations basées sur le profil
            recommendations = []
            
            # Recommandations basées sur les catégories préférées
            order_behavior = profile.get("order_behavior", {})
            preferred_categories = order_behavior.get("preferred_categories", [])
            
            for category, count in preferred_categories[:2]:
                recommendations.append({
                    "type": "category_based",
                    "category": category,
                    "reason": f"Basé sur vos achats précédents dans {category}",
                    "priority": "high"
                })
            
            # Recommandations basées sur le segment
            segments = profile.get("segments", [])
            if "high_value" in segments:
                recommendations.append({
                    "type": "segment_based",
                    "category": "premium",
                    "reason": "Produits premium pour clients fidèles",
                    "priority": "medium"
                })
            
            # Recommandations basées sur l'engagement
            engagement_score = profile.get("engagement_score", 0)
            if engagement_score < 30:
                recommendations.append({
                    "type": "engagement_based",
                    "category": "popular",
                    "reason": "Produits populaires pour vous faire découvrir",
                    "priority": "high"
                })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting user recommendations: {e}")
            return []
    
    async def get_segment_analytics(self) -> Dict[str, Any]:
        """Retourne les analytics par segment"""
        try:
            pipeline = [
                {"$group": {
                    "_id": "$segments",
                    "count": {"$sum": 1},
                    "avg_engagement": {"$avg": "$engagement_score"},
                    "avg_order_value": {"$avg": "$order_behavior.total_spent"}
                }},
                {"$sort": {"count": -1}}
            ]
            
            results = list(self.db_manager.mongo_db.user_profiles.aggregate(pipeline))
            
            return {
                "segment_analytics": results,
                "total_profiled_users": sum(result["count"] for result in results)
            }
            
        except Exception as e:
            logger.error(f"Error getting segment analytics: {e}")
            return {} 

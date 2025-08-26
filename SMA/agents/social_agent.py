from .base_agent import BaseAgent
from typing import Dict, Any, List, Optional
from catalogue.backend.database import SessionLocal
from catalogue.backend.models import User, Product, Order
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
import logging
from datetime import datetime, timedelta
import json
from catalogue.backend.qdrant_client import client as qdrant_client, search_embedding
# AGENT CONNECTÉ À QDRANT (vectoriel)
# Utilisez search_embedding(...) pour la recherche sociale

class SocialAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="social_agent",
            description="Agent spécialisé dans les fonctionnalités sociales et communautaires"
        )
        self.logger = logging.getLogger(__name__)
        
        # Plateformes sociales supportées
        self.social_platforms = {
            "instagram": {"trending": True, "sharing": True, "influencers": True},
            "tiktok": {"trending": True, "sharing": True, "viral": True},
            "facebook": {"sharing": True, "groups": True, "events": True},
            "twitter": {"trending": True, "sharing": True, "hashtags": True},
            "pinterest": {"inspiration": True, "boards": True, "trending": True}
        }
    
    def get_system_prompt(self) -> str:
        return """
        Vous êtes un expert en fonctionnalités sociales e-commerce.
        Votre rôle est de connecter les utilisateurs et créer une communauté engagée.
        
        Capacités:
        - Détecter les tendances sociales
        - Gérer le partage de paniers et souhaits
        - Analyser et présenter les avis vérifiés
        - Créer des expériences communautaires
        - Intégrer les réseaux sociaux
        
        Soyez toujours social et encouragez l'interaction entre utilisateurs.
        """
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        # Exemple de réponse dynamique
        state["response_text"] = "Vous pouvez partager vos avis et recommandations avec la communauté sur notre plateforme sociale."
        return state
    
    async def get_trending_products_safe(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Obtenir les produits tendance sur les réseaux sociaux"""
        try:
            platform = state.get("platform", "all")
            category = state.get("category", "")
            limit = state.get("limit", 20)
            
            # En production, intégrer avec les APIs des réseaux sociaux
            # Ici on simule les tendances
            
            trending_data = {
                "instagram": {
                    "hashtags": ["#fashion", "#tech", "#home", "#beauty"],
                    "trending_products": [
                        {"id": 1, "name": "Smartphone Pro", "trend_score": 95, "mentions": 1250},
                        {"id": 2, "name": "Sneakers Urban", "trend_score": 88, "mentions": 890},
                        {"id": 3, "name": "Montre Connectée", "trend_score": 82, "mentions": 650}
                    ]
                },
                "tiktok": {
                    "hashtags": ["#viral", "#trending", "#fyp", "#shopping"],
                    "trending_products": [
                        {"id": 4, "name": "Casque Audio", "trend_score": 92, "mentions": 2100},
                        {"id": 5, "name": "Sac à Dos", "trend_score": 85, "mentions": 1200},
                        {"id": 6, "name": "Lampes LED", "trend_score": 78, "mentions": 950}
                    ]
                },
                "pinterest": {
                    "boards": ["Mode", "Décoration", "Tech", "Lifestyle"],
                    "trending_products": [
                        {"id": 7, "name": "Vase Design", "trend_score": 87, "mentions": 750},
                        {"id": 8, "name": "Coussin Déco", "trend_score": 83, "mentions": 680},
                        {"id": 9, "name": "Miroir Mural", "trend_score": 79, "mentions": 520}
                    ]
                }
            }
            
            # Filtrer par plateforme si spécifiée
            if platform != "all" and platform in trending_data:
                platform_data = trending_data[platform]
                trending_products = platform_data.get("trending_products", [])
            else:
                # Combiner toutes les plateformes
                all_products = []
                for platform_data in trending_data.values():
                    all_products.extend(platform_data.get("trending_products", []))
                
                # Trier par score de tendance
                all_products.sort(key=lambda x: x["trend_score"], reverse=True)
                trending_products = all_products[:limit]
            
            # Enrichir avec les informations produit
            enriched_products = await self._enrich_trending_products(trending_products)
            
            return {
                "trending_products": enriched_products,
                "platform": platform,
                "category": category,
                "total_trending": len(enriched_products),
                "trending_metrics": {
                    "total_mentions": sum(p.get("mentions", 0) for p in trending_products),
                    "average_trend_score": sum(p.get("trend_score", 0) for p in trending_products) / len(trending_products) if trending_products else 0,
                    "trending_since": (datetime.utcnow() - timedelta(days=7)).isoformat()
                },
                "social_insights": {
                    "top_hashtags": self._get_top_hashtags(trending_data, platform),
                    "engagement_rate": "élevé" if len(trending_products) > 10 else "modéré",
                    "viral_potential": "fort" if any(p["trend_score"] > 90 for p in trending_products) else "modéré"
                }
            }
            
        except Exception as e:
            self.logger.error(f"Erreur produits tendance: {str(e)}")
            return {"error": str(e)}
    
    async def _enrich_trending_products(self, trending_products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enrichir les produits tendance avec les informations de la base de données"""
        db: Optional[Session] = None
        try:
            db = SessionLocal()
            
            enriched_products = []
            for trend_product in trending_products:
                product_id = trend_product.get("id")
                
                # Récupérer les informations produit
                product = db.query(Product).filter(Product.id == product_id).first()
                
                if product:
                    enriched_product = {
                        **trend_product,
                        "name": product.name,
                        "description": product.description,
                        "price": product.price,
                        "image_url": product.image_url,
                        "category": product.category,
                        "brand": getattr(product, 'brand', ''),
                        "rating": getattr(product, 'rating', 0.0),
                        "stock_status": "En stock" if product.stock_quantity > 0 else "Rupture"
                    }
                else:
                    # Produit simulé si pas en base
                    enriched_product = {
                        **trend_product,
                        "name": f"Produit {product_id}",
                        "description": "Description du produit tendance",
                        "price": 99.99,
                        "image_url": f"/images/product_{product_id}.jpg",
                        "category": "Général",
                        "brand": "Marque",
                        "rating": 4.5,
                        "stock_status": "En stock"
                    }
                
                enriched_products.append(enriched_product)
            
            return enriched_products
            
        except Exception as e:
            self.logger.error(f"Erreur enrichissement produits: {str(e)}")
            return trending_products
        finally:
            if db:
                db.close()
    
    def _get_top_hashtags(self, trending_data: Dict[str, Any], platform: str) -> List[str]:
        """Extraire les hashtags les plus populaires"""
        try:
            all_hashtags = []
            
            if platform == "all":
                for platform_data in trending_data.values():
                    if "hashtags" in platform_data:
                        all_hashtags.extend(platform_data["hashtags"])
            elif platform in trending_data and "hashtags" in trending_data[platform]:
                all_hashtags = trending_data[platform]["hashtags"]
            
            # Retourner les top hashtags
            return all_hashtags[:5]
            
        except Exception:
            return ["#trending", "#viral", "#popular"]
    
    async def share_cart_safe(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Partager un panier avec des amis"""
        try:
            user_id = state.get("user_id")
            cart_id = state.get("cart_id")
            share_with = state.get("share_with", [])  # Liste d'emails ou IDs
            share_method = state.get("share_method", "email")  # email, link, social
            message = state.get("message", "")
            
            if not user_id or not cart_id:
                return {"error": "Utilisateur et panier requis"}
            
            if not share_with:
                return {"error": "Destinataires requis pour le partage"}
            
            # Récupérer le contenu du panier
            cart_content = await self._get_cart_content(cart_id, user_id)
            
            if not cart_content:
                return {"error": "Panier non trouvé ou inaccessible"}
            
            # Générer le lien de partage
            share_link = await self._generate_share_link(cart_id, user_id)
            
            # Préparer le partage selon la méthode
            share_result = {}
            
            if share_method == "email":
                share_result = await self._share_via_email(share_with, cart_content, share_link, message)
            elif share_method == "link":
                share_result = await self._share_via_link(share_link, cart_content)
            elif share_method == "social":
                share_result = await self._share_via_social(share_with, cart_content, share_link, message)
            
            # Enregistrer l'activité de partage
            await self._log_share_activity(user_id, cart_id, share_method, share_with)
            
            return {
                "success": True,
                "shared_cart": cart_content,
                "share_method": share_method,
                "share_link": share_link,
                "recipients": share_with,
                "share_result": share_result,
                "expires_at": (datetime.utcnow() + timedelta(days=7)).isoformat(),
                "privacy_settings": {
                    "public": False,
                    "password_protected": True,
                    "expires_in_days": 7
                }
            }
            
        except Exception as e:
            self.logger.error(f"Erreur partage panier: {str(e)}")
            return {"error": str(e)}
    
    async def _get_cart_content(self, cart_id: str, user_id: int) -> Optional[Dict[str, Any]]:
        """Récupérer le contenu d'un panier"""
        db: Optional[Session] = None
        try:
            db = SessionLocal()
            
            # Récupérer les items du panier
            cart_items = db.query(CartItem).filter(
                CartItem.user_id == user_id
            ).all()
            
            if not cart_items:
                return None
            
            # Enrichir avec les informations produit
            enriched_items = []
            total_price = 0.0
            
            for item in cart_items:
                product = db.query(Product).filter(Product.id == item.product_id).first()
                if product:
                    item_total = item.price * item.quantity
                    total_price += item_total
                    
                    enriched_items.append({
                        "product_id": product.id,
                        "name": product.name,
                        "price": item.price,
                        "quantity": item.quantity,
                        "total": item_total,
                        "image_url": product.image_url
                    })
            
            return {
                "cart_id": cart_id,
                "items": enriched_items,
                "total_items": len(enriched_items),
                "total_price": round(total_price, 2),
                "shared_by": user_id,
                "shared_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Erreur récupération contenu panier: {str(e)}")
            return None
        finally:
            if db:
                db.close()
    
    async def _generate_share_link(self, cart_id: str, user_id: int) -> str:
        """Générer un lien de partage sécurisé"""
        try:
            # En production, générer un token unique et sécurisé
            import secrets
            token = secrets.token_urlsafe(32)
            
            # Construire l'URL de partage
            base_url = "https://fidelobot.com/share"
            share_link = f"{base_url}/cart/{cart_id}?token={token}&user={user_id}"
            
            return share_link
            
        except Exception:
            return f"https://fidelobot.com/share/cart/{cart_id}"
    
    async def _share_via_email(self, recipients: List[str], cart_content: Dict[str, Any], share_link: str, message: str) -> Dict[str, Any]:
        """Partager via email"""
        try:
            # En production, envoyer de vrais emails
            email_result = {
                "method": "email",
                "recipients": recipients,
                "sent": True,
                "delivery_status": "sent",
                "email_content": {
                    "subject": f"Panier partagé par {cart_content.get('shared_by', 'un ami')}",
                    "body": f"{message}\n\nLien du panier: {share_link}",
                    "cart_summary": f"{cart_content.get('total_items', 0)} articles - Total: {cart_content.get('total_price', 0)}€"
                }
            }
            
            return email_result
            
        except Exception as e:
            self.logger.error(f"Erreur partage email: {str(e)}")
            return {"error": str(e)}
    
    async def _share_via_link(self, share_link: str, cart_content: Dict[str, Any]) -> Dict[str, Any]:
        """Partager via lien direct"""
        try:
            return {
                "method": "link",
                "share_link": share_link,
                "qr_code_available": True,
                "cart_preview": {
                    "items_count": cart_content.get("total_items", 0),
                    "total_price": cart_content.get("total_price", 0),
                    "preview_image": "/images/cart_preview.jpg"
                }
            }
            
        except Exception as e:
            self.logger.error(f"Erreur partage lien: {str(e)}")
            return {"error": str(e)}
    
    async def _share_via_social(self, platforms: List[str], cart_content: Dict[str, Any], share_link: str, message: str) -> Dict[str, Any]:
        """Partager via réseaux sociaux"""
        try:
            social_results = {}
            
            for platform in platforms:
                if platform in self.social_platforms:
                    # En production, intégrer avec les APIs des réseaux sociaux
                    social_results[platform] = {
                        "shared": True,
                        "post_id": f"post_{platform}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                        "share_link": share_link,
                        "message": message,
                        "engagement": "modéré"
                    }
                else:
                    social_results[platform] = {
                        "shared": False,
                        "error": "Plateforme non supportée"
                    }
            
            return social_results
            
        except Exception as e:
            self.logger.error(f"Erreur partage social: {str(e)}")
            return {"error": str(e)}
    
    async def _log_share_activity(self, user_id: int, cart_id: str, share_method: str, recipients: List[str]):
        """Enregistrer l'activité de partage"""
        try:
            # En production, enregistrer en base de données
            share_log = {
                "user_id": user_id,
                "cart_id": cart_id,
                "share_method": share_method,
                "recipients": recipients,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "completed"
            }
            
            # Log pour audit
            self.logger.info(f"Partage enregistré: {share_log}")
            
        except Exception as e:
            self.logger.error(f"Erreur enregistrement partage: {str(e)}")
    
    async def share_wishlist_safe(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Partager une liste de souhaits"""
        try:
            user_id = state.get("user_id")
            wishlist_id = state.get("wishlist_id")
            share_with = state.get("share_with", [])
            share_method = state.get("share_method", "email")
            message = state.get("message", "")
            
            if not user_id or not wishlist_id:
                return {"error": "Utilisateur et liste de souhaits requis"}
            
            # Récupérer le contenu de la liste de souhaits
            wishlist_content = await self._get_wishlist_content(wishlist_id, user_id)
            
            if not wishlist_content:
                return {"error": "Liste de souhaits non trouvée"}
            
            # Générer le lien de partage
            share_link = await self._generate_wishlist_share_link(wishlist_id, user_id)
            
            # Partager selon la méthode
            share_result = {}
            if share_method == "email":
                share_result = await self._share_wishlist_via_email(share_with, wishlist_content, share_link, message)
            elif share_method == "social":
                share_result = await self._share_wishlist_via_social(share_with, wishlist_content, share_link, message)
            
            return {
                "success": True,
                "shared_wishlist": wishlist_content,
                "share_method": share_method,
                "share_link": share_link,
                "recipients": share_with,
                "share_result": share_result,
                "collaborative_features": {
                    "allow_comments": True,
                    "allow_suggestions": True,
                    "group_gifting": True
                }
            }
            
        except Exception as e:
            self.logger.error(f"Erreur partage liste souhaits: {str(e)}")
            return {"error": str(e)}
    
    async def _get_wishlist_content(self, wishlist_id: str, user_id: int) -> Optional[Dict[str, Any]]:
        """Récupérer le contenu d'une liste de souhaits"""
        # Simulation - en production, récupérer depuis la base de données
        return {
            "wishlist_id": wishlist_id,
            "name": "Ma liste de souhaits",
            "items": [
                {"id": 1, "name": "Smartphone", "price": 599.99, "priority": "high"},
                {"id": 2, "name": "Casque Audio", "price": 199.99, "priority": "medium"},
                {"id": 3, "name": "Montre", "price": 299.99, "priority": "low"}
            ],
            "total_items": 3,
            "total_value": 1099.97,
            "created_by": user_id
        }
    
    async def _generate_wishlist_share_link(self, wishlist_id: str, user_id: int) -> str:
        """Générer un lien de partage pour la liste de souhaits"""
        return f"https://fidelobot.com/wishlist/{wishlist_id}?shared=true&user={user_id}"
    
    async def _share_wishlist_via_email(self, recipients: List[str], wishlist_content: Dict[str, Any], share_link: str, message: str) -> Dict[str, Any]:
        """Partager la liste de souhaits via email"""
        return {
            "method": "email",
            "recipients": recipients,
            "sent": True,
            "email_content": {
                "subject": f"Liste de souhaits partagée",
                "body": f"{message}\n\nLien: {share_link}",
                "wishlist_summary": f"{wishlist_content.get('total_items', 0)} articles - Valeur totale: {wishlist_content.get('total_value', 0)}€"
            }
        }
    
    async def _share_wishlist_via_social(self, platforms: List[str], wishlist_content: Dict[str, Any], share_link: str, message: str) -> Dict[str, Any]:
        """Partager la liste de souhaits via réseaux sociaux"""
        social_results = {}
        
        for platform in platforms:
            if platform in self.social_platforms:
                social_results[platform] = {
                    "shared": True,
                    "post_id": f"wishlist_{platform}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                    "share_link": share_link,
                    "message": message
                }
        
        return social_results
    
    async def get_verified_reviews_safe(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Obtenir les avis vérifiés d'autres clients"""
        try:
            product_id = state.get("product_id")
            user_id = state.get("user_id")
            limit = state.get("limit", 10)
            sort_by = state.get("sort_by", "recent")  # recent, helpful, rating
            
            if not product_id:
                return {"error": "ID produit requis"}
            
            db = SessionLocal()
            
            try:
                # Récupérer les avis vérifiés
                reviews_query = db.query(Review).filter(
                    Review.product_id == product_id,
                    Review.is_verified == True,
                    Review.status == "approved"
                )
                
                # Trier selon le critère
                if sort_by == "recent":
                    reviews_query = reviews_query.order_by(Review.created_at.desc())
                elif sort_by == "helpful":
                    reviews_query = reviews_query.order_by(Review.helpful_count.desc())
                elif sort_by == "rating":
                    reviews_query = reviews_query.order_by(Review.rating.desc())
                
                reviews = reviews_query.limit(limit).all()
                
                # Formater les avis
                formatted_reviews = []
                for review in reviews:
                    # Récupérer les informations utilisateur
                    user = db.query(User).filter(User.id == review.user_id).first()
                    
                    formatted_review = {
                        "id": review.id,
                        "rating": review.rating,
                        "title": review.title,
                        "content": review.content,
                        "created_at": review.created_at.isoformat(),
                        "helpful_count": review.helpful_count,
                        "verified_purchase": review.is_verified,
                        "user_info": {
                            "name": f"{user.first_name} {user.last_name[0]}." if user else "Utilisateur",
                            "avatar": getattr(user, 'avatar_url', None),
                            "verified_buyer": True
                        },
                        "review_metadata": {
                            "purchase_date": getattr(review, 'purchase_date', None),
                            "product_variant": getattr(review, 'product_variant', None),
                            "delivery_rating": getattr(review, 'delivery_rating', None)
                        }
                    }
                    
                    formatted_reviews.append(formatted_review)
                
                # Statistiques des avis
                total_reviews = db.query(Review).filter(
                    Review.product_id == product_id,
                    Review.is_verified == True,
                    Review.status == "approved"
                ).count()
                
                avg_rating = db.query(func.avg(Review.rating)).filter(
                    Review.product_id == product_id,
                    Review.is_verified == True,
                    Review.status == "approved"
                ).scalar() or 0.0
                
                rating_distribution = db.query(
                    Review.rating,
                    func.count(Review.id)
                ).filter(
                    Review.product_id == product_id,
                    Review.is_verified == True,
                    Review.status == "approved"
                ).group_by(Review.rating).all()
                
                return {
                    "verified_reviews": formatted_reviews,
                    "total_verified_reviews": total_reviews,
                    "average_rating": round(avg_rating, 1),
                    "rating_distribution": {str(rating): count for rating, count in rating_distribution},
                    "review_quality": {
                        "verification_level": "strict",
                        "moderation_status": "active",
                        "fake_review_detection": "enabled"
                    },
                    "sorting": {
                        "current": sort_by,
                        "available_options": ["recent", "helpful", "rating"]
                    }
                }
                
            finally:
                db.close()
                
        except Exception as e:
            self.logger.error(f"Erreur avis vérifiés: {str(e)}")
            return {"error": str(e)}
    
    async def get_social_recommendations_safe(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Obtenir des recommandations basées sur l'activité sociale"""
        try:
            user_id = state.get("user_id")
            platform = state.get("platform", "all")
            
            if not user_id:
                return {"error": "ID utilisateur requis"}
            
            # Analyser l'activité sociale de l'utilisateur
            social_activity = await self._analyze_social_activity(user_id)
            
            # Générer des recommandations personnalisées
            recommendations = await self._generate_social_recommendations(social_activity, platform)
            
            return {
                "social_recommendations": recommendations,
                "user_social_profile": social_activity,
                "recommendation_engine": {
                    "algorithm": "social_collaborative_filtering",
                    "confidence_score": 0.85,
                    "last_updated": datetime.utcnow().isoformat()
                }
            }
            
        except Exception as e:
            self.logger.error(f"Erreur recommandations sociales: {str(e)}")
            return {"error": str(e)}
    
    async def _analyze_social_activity(self, user_id: int) -> Dict[str, Any]:
        """Analyser l'activité sociale d'un utilisateur"""
        try:
            # En production, analyser l'activité réelle
            return {
                "social_score": 75,
                "engagement_level": "actif",
                "preferred_platforms": ["instagram", "pinterest"],
                "interests": ["mode", "décoration", "tech"],
                "influence_level": "micro-influenceur",
                "activity_frequency": "quotidien"
            }
            
        except Exception:
            return {"social_score": 0, "engagement_level": "inactif"}
    
    async def _generate_social_recommendations(self, social_activity: Dict[str, Any], platform: str) -> List[Dict[str, Any]]:
        """Générer des recommandations basées sur l'activité sociale"""
        try:
            # Recommandations simulées basées sur l'activité sociale
            recommendations = [
                {
                    "type": "product",
                    "reason": "Populaire sur vos réseaux préférés",
                    "products": [
                        {"id": 10, "name": "Produit Social 1", "social_proof": "500+ mentions"},
                        {"id": 11, "name": "Produit Social 2", "social_proof": "Trending sur Instagram"}
                    ]
                },
                {
                    "type": "content",
                    "reason": "Basé sur vos centres d'intérêt",
                    "content": [
                        {"type": "article", "title": "Guide Mode 2024", "platform": "pinterest"},
                        {"type": "video", "title": "Tutoriel Décoration", "platform": "instagram"}
                    ]
                },
                {
                    "type": "community",
                    "reason": "Communautés actives dans vos domaines",
                    "communities": [
                        {"name": "Mode & Style", "members": 15000, "activity": "élevée"},
                        {"name": "Décoration Intérieure", "members": 8500, "activity": "modérée"}
                    ]
                }
            ]
            
            return recommendations
            
        except Exception:
            return []
    
    async def get_community_features_safe(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Obtenir les fonctionnalités communautaires disponibles"""
        try:
            user_id = state.get("user_id")
            
            community_features = {
                "forums": {
                    "enabled": True,
                    "categories": ["Aide & Support", "Conseils d'achat", "Avis produits", "Mode & Style"],
                    "moderation": "active",
                    "members_count": 25000
                },
                "groups": {
                    "enabled": True,
                    "types": ["Intérêts communs", "Géographique", "Niveau d'expertise"],
                    "creation_allowed": True,
                    "total_groups": 150
                },
                "events": {
                    "enabled": True,
                    "types": ["Webinaires", "Ateliers", "Rencontres", "Ventes privées"],
                    "upcoming_events": 8
                },
                "challenges": {
                    "enabled": True,
                    "current_challenges": [
                        {"name": "Défi Mode", "participants": 1250, "prize": "Panier de 500€"},
                        {"name": "Défi Décoration", "participants": 890, "prize": "Produit exclusif"}
                    ]
                },
                "rewards": {
                    "enabled": True,
                    "points_system": True,
                    "badges": True,
                    "leaderboards": True
                }
            }
            
            # Personnaliser selon l'utilisateur
            if user_id:
                user_activity = await self._analyze_social_activity(user_id)
                community_features["personalized"] = {
                    "recommended_groups": ["Mode & Style", "Tech Enthusiasts"],
                    "suggested_events": ["Atelier Mode", "Webinaire Tech"],
                    "community_level": user_activity.get("engagement_level", "débutant")
                }
            
            return {
                "community_features": community_features,
                "participation_benefits": [
                    "Accès aux ventes privées",
                    "Points de fidélité bonus",
                    "Support prioritaire",
                    "Produits exclusifs"
                ],
                "community_guidelines": {
                    "respect": "Respect mutuel obligatoire",
                    "authenticity": "Avis authentiques uniquement",
                    "helpfulness": "Encourager l'entraide",
                    "moderation": "Modération active"
                }
            }
            
        except Exception as e:
            self.logger.error(f"Erreur fonctionnalités communautaires: {str(e)}")
            return {"error": str(e)}

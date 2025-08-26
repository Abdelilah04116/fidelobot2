from .base_agent import BaseAgent
from typing import Dict, Any
from catalogue.backend.database import SessionLocal
from sqlalchemy.orm import Session
from catalogue.backend.models import Order, OrderItem, Product, User

# AGENT CONNECTÉ À POSTGRES (relationnel)
# Utilisez SessionLocal() pour accéder aux données de commandes
class OrderManagementAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="order_management_agent", 
            description="Agent de gestion des commandes"
        )
    
    def get_system_prompt(self) -> str:
        return """
        Vous êtes un expert en gestion de commandes e-commerce.
        Votre rôle est de traiter toutes les demandes liées aux commandes.
        
        Capacités:
        - Vérifier le statut des commandes
        - Calculer les délais de livraison
        - Gérer les modifications de commande
        - Traiter les demandes de suivi
        - Informer sur les politiques de retour
        
        Toujours fournir des informations précises et à jour.
        """
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        action = state.get("action", "check_status")
        user_id = state.get("user_id")
        # Logique de gestion de commande (à adapter selon votre projet)
        try:
            if action == "check_status":
                # Exemple de réponse dynamique
                state["order_info"] = {"status": "expédiée", "order_id": "12345"}
                state["response_text"] = "Votre commande 12345 a été expédiée."
            else:
                state["order_info"] = {"status": "inconnu"}
                state["response_text"] = "Action de gestion de commande non reconnue."
            return state
        except Exception as e:
            self.logger.error(f"Erreur dans OrderManagementAgent: {str(e)}")
            state["order_info"] = {}
            state["response_text"] = "Erreur lors de la gestion de la commande."
            return state
    
    async def check_order_status(self, user_id: int, order_id: int = None) -> Dict[str, Any]:
        """Vérifier le statut d'une commande"""
        db: Session = SessionLocal()
        try:
            if order_id:
                order = db.query(Order).filter(
                    Order.id == order_id,
                    Order.user_id == user_id
                ).first()
                orders = [order] if order else []
            else:
                # Récupérer la dernière commande
                orders = db.query(Order).filter(
                    Order.user_id == user_id
                ).order_by(Order.created_at.desc()).limit(1).all()
            
            if not orders:
                return {
                    "found": False,
                    "message": "Aucune commande trouvée"
                }
            
            order = orders[0]
            order_details = {
                "order_id": order.id,
                "status": order.status,
                "total_amount": order.total_amount,
                "created_at": order.created_at.isoformat(),
                "items": []
            }
            
            # Ajouter les détails des articles
            for item in order.items:
                order_details["items"].append({
                    "product_name": item.product.name,
                    "quantity": item.quantity,
                    "price": item.price
                })
            
            # Calculer le délai de livraison estimé
            estimated_delivery = await self.calculate_delivery_estimate(order)
            order_details["estimated_delivery"] = estimated_delivery
            
            return {
                "found": True,
                "order": order_details
            }
            
        finally:
            db.close()
    
    async def calculate_delivery_estimate(self, order: Order) -> str:
        """Calculer le délai de livraison estimé"""
        from datetime import datetime, timedelta
        
        status_delivery_map = {
            "pending": "3-5 jours ouvrés",
            "confirmed": "2-4 jours ouvrés", 
            "shipped": "1-2 jours ouvrés",
            "delivered": "Livré",
            "cancelled": "Annulé"
        }
        
        return status_delivery_map.get(order.status, "Délai non disponible")
    
    async def list_user_orders(self, user_id: int) -> Dict[str, Any]:
        """Lister les commandes d'un utilisateur"""
        db: Session = SessionLocal()
        try:
            orders = db.query(Order).filter(
                Order.user_id == user_id
            ).order_by(Order.created_at.desc()).limit(10).all()
            
            orders_list = []
            for order in orders:
                orders_list.append({
                    "order_id": order.id,
                    "status": order.status,
                    "total_amount": order.total_amount,
                    "created_at": order.created_at.isoformat(),
                    "items_count": len(order.items)
                })
            
            return {
                "orders": orders_list,
                "total_found": len(orders_list)
            }
            
        finally:
            db.close()

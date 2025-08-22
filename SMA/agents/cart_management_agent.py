from .base_agent import BaseAgent
from typing import Dict, Any, List, Optional
from ..models.database import SessionLocal, User, Product, Order, OrderItem, CartItem
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
import logging
from datetime import datetime, timedelta

class CartManagementAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="cart_management_agent",
            description="Agent spécialisé dans la gestion du panier et des commandes"
        )
        self.logger = logging.getLogger(__name__)
    
    def get_system_prompt(self) -> str:
        return """
        Vous êtes un expert en gestion de panier e-commerce.
        Votre rôle est d'aider les clients à gérer leur panier et finaliser leurs commandes.
        
        Capacités:
        - Afficher le contenu du panier
        - Vérifier l'existence des produits avant ajout
        - Ajouter/supprimer des produits du panier
        - Gérer les quantités et modifications
        - Calculer les totaux et appliquer les promotions
        - Proposer des produits complémentaires
        - Accompagner le processus de commande
        - Gérer les moyens de paiement
        - Rappeler les articles abandonnés
        
        Soyez toujours serviable et guidez le client vers une expérience d'achat optimale.
        """
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            action = state.get("cart_action", "view")
            user_message = state.get("user_message", "").lower()
            
            # Détection intelligente de l'action basée sur le message
            if not action or action == "view":
                if any(word in user_message for word in ["ajouter", "add", "mettre"]):
                    action = "add"
                elif any(word in user_message for word in ["supprimer", "retirer", "enlever", "remove"]):
                    action = "remove"
                elif any(word in user_message for word in ["modifier", "changer", "update"]):
                    action = "update"
                elif any(word in user_message for word in ["vider", "clear", "empty"]):
                    action = "clear"
                else:
                    action = "view"
            
            # Exécution de l'action
            if action == "add":
                result = await self._handle_add_to_cart(state)
            elif action == "remove":
                result = await self._handle_remove_from_cart(state)
            elif action == "update":
                result = await self._handle_update_quantity(state)
            elif action == "clear":
                result = await self._handle_clear_cart(state)
            else:
                result = await self._handle_view_cart(state)
            
            # Mise à jour de l'état
            state.update(result)
            return state
            
        except Exception as e:
            self.logger.error(f"Erreur critique dans CartManagementAgent: {str(e)}")
            state["cart"] = {
                "items": [],
                "total_items": 0,
                "total_price": 0.0,
                "is_empty": True
            }
            state["response_text"] = "Désolé, un problème technique empêche la gestion du panier pour le moment."
            return state
    
    async def _handle_add_to_cart(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Gérer l'ajout au panier avec vérification d'existence du produit"""
        product_id = state.get("product_id")
        quantity = state.get("quantity", 1)
        user_id = state.get("user_id")
        session_id = state.get("session_id")
        
        if not product_id:
            return {
                "response_text": "Pour ajouter un produit au panier, veuillez spécifier l'ID du produit (ex: 'ajouter produit 123').",
                "cart": await self._get_cart_data(user_id, session_id)
            }
        
        # Vérifier l'existence du produit
        product_exists = await self._verify_product_exists(product_id)
        if not product_exists:
            return {
                "response_text": f"Le produit avec l'ID {product_id} n'existe pas dans notre catalogue. Veuillez vérifier l'ID ou rechercher un autre produit.",
                "cart": await self._get_cart_data(user_id, session_id)
            }
        
        # Vérifier si le produit est déjà dans le panier
        cart_data = await self._get_cart_data(user_id, session_id)
        existing_item = None
        if cart_data.get("items"):
            existing_item = next((item for item in cart_data["items"] if item.get("product_id") == product_id), None)
        
        if existing_item:
            # Mettre à jour la quantité
            new_quantity = existing_item["quantity"] + quantity
            result = await self.update_quantity_safe({
                **state,
                "quantity": new_quantity
            })
            if result.get("success"):
                return {
                    "response_text": f"Quantité mise à jour pour le produit {existing_item['name']}. Nouvelle quantité: {new_quantity}",
                    "cart": result.get("cart", {})
                }
        else:
            # Ajouter le produit
            result = await self.add_to_cart_safe(state)
            if result.get("success"):
                product_name = result.get("product_added", {}).get("name", f"Produit {product_id}")
                return {
                    "response_text": f"Produit '{product_name}' ajouté au panier avec succès !",
                    "cart": result.get("cart", {})
                }
        
        return {
            "response_text": "Impossible d'ajouter le produit au panier. Veuillez réessayer.",
            "cart": await self._get_cart_data(user_id, session_id)
        }
    
    async def _handle_remove_from_cart(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Gérer la suppression du panier"""
        product_id = state.get("product_id")
        user_id = state.get("user_id")
        session_id = state.get("session_id")
        
        if not product_id:
            return {
                "response_text": "Pour supprimer un produit du panier, veuillez spécifier l'ID du produit (ex: 'supprimer produit 123').",
                "cart": await self._get_cart_data(user_id, session_id)
            }
        
        # Vérifier si le produit est dans le panier
        cart_data = await self._get_cart_data(user_id, session_id)
        existing_item = None
        if cart_data.get("items"):
            existing_item = next((item for item in cart_data["items"] if item.get("product_id") == product_id), None)
        
        if not existing_item:
            return {
                "response_text": f"Le produit avec l'ID {product_id} n'est pas dans votre panier.",
                "cart": cart_data
            }
        
        # Supprimer le produit
        result = await self.remove_from_cart_safe(state)
        if result.get("success"):
            return {
                "response_text": f"Produit '{existing_item['name']}' supprimé du panier avec succès !",
                "cart": result.get("cart", {})
            }
        
        return {
            "response_text": "Impossible de supprimer le produit du panier. Veuillez réessayer.",
            "cart": await self._get_cart_data(user_id, session_id)
        }
    
    async def _handle_update_quantity(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Gérer la modification de quantité"""
        product_id = state.get("product_id")
        quantity = state.get("quantity", 1)
        user_id = state.get("user_id")
        session_id = state.get("session_id")
        
        if not product_id:
            return {
                "response_text": "Pour modifier la quantité, veuillez spécifier l'ID du produit et la nouvelle quantité (ex: 'modifier quantité produit 123 x2').",
                "cart": await self._get_cart_data(user_id, session_id)
            }
        
        if quantity <= 0:
            # Supprimer le produit si quantité = 0
            return await self._handle_remove_from_cart(state)
        
        # Vérifier si le produit est dans le panier
        cart_data = await self._get_cart_data(user_id, session_id)
        existing_item = None
        if cart_data.get("items"):
            existing_item = next((item for item in cart_data["items"] if item.get("product_id") == product_id), None)
        
        if not existing_item:
            return {
                "response_text": f"Le produit avec l'ID {product_id} n'est pas dans votre panier.",
                "cart": cart_data
            }
        
        # Mettre à jour la quantité
        result = await self.update_quantity_safe(state)
        if result.get("success"):
            return {
                "response_text": f"Quantité mise à jour pour '{existing_item['name']}'. Nouvelle quantité: {quantity}",
                "cart": result.get("cart", {})
            }
        
        return {
            "response_text": "Impossible de modifier la quantité. Veuillez réessayer.",
            "cart": await self._get_cart_data(user_id, session_id)
        }
    
    async def _handle_clear_cart(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Gérer le vidage du panier"""
        user_id = state.get("user_id")
        session_id = state.get("session_id")
        
        result = await self.clear_cart_safe(user_id, session_id)
        if result.get("success"):
            deleted_count = result.get("deleted_count", 0)
            return {
                "response_text": f"Panier vidé avec succès ! {deleted_count} article(s) supprimé(s).",
                "cart": {
                    "items": [],
                    "total_items": 0,
                    "total_price": 0.0,
                    "is_empty": True
                }
            }
        
        return {
            "response_text": "Impossible de vider le panier. Veuillez réessayer.",
            "cart": await self._get_cart_data(user_id, session_id)
        }
    
    async def _handle_view_cart(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Gérer l'affichage du panier"""
        user_id = state.get("user_id")
        session_id = state.get("session_id")
        
        cart_data = await self._get_cart_data(user_id, session_id)
        
        if cart_data.get("is_empty"):
            return {
                "response_text": "Votre panier est vide. Vous pouvez ajouter des produits en recherchant dans notre catalogue !",
                "cart": cart_data
            }
        else:
            items_count = cart_data.get("total_items", 0)
            total_price = cart_data.get("total_price", 0.0)
            return {
                "response_text": f"Votre panier contient {items_count} article(s) pour un total de {total_price}€. Vous pouvez modifier les quantités ou supprimer des articles.",
                "cart": cart_data
            }
    
    async def _verify_product_exists(self, product_id: int) -> bool:
        """Vérifier l'existence d'un produit dans la base de données"""
        db: Optional[Session] = None
        try:
            db = SessionLocal()
            product = db.query(Product).filter(
                Product.id == product_id,
                Product.is_active == True
            ).first()
            return product is not None
        except Exception as e:
            self.logger.error(f"Erreur vérification produit {product_id}: {str(e)}")
            return False
        finally:
            if db:
                db.close()
    
    async def _get_cart_data(self, user_id: Optional[int], session_id: Optional[str]) -> Dict[str, Any]:
        """Récupérer les données du panier"""
        result = await self.view_cart_safe(user_id, session_id)
        if result.get("error"):
            return {
                "items": [],
                "total_items": 0,
                "total_price": 0.0,
                "is_empty": True
            }
        return result.get("cart", {})
    
    async def add_to_cart_safe(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Ajouter un produit au panier de manière sécurisée"""
        db: Optional[Session] = None
        try:
            user_id = state.get("user_id")
            session_id = state.get("session_id")
            product_id = state.get("product_id")
            quantity = state.get("quantity", 1)
            
            if not product_id:
                return {"error": "ID produit requis"}
            
            if quantity <= 0:
                return {"error": "Quantité doit être positive"}
            
            db = SessionLocal()
            
            # Vérifier que le produit existe et est disponible
            product = db.query(Product).filter(
                Product.id == product_id,
                Product.is_active == True,
                Product.stock_quantity > 0
            ).first()
            
            if not product:
                return {"error": "Produit non disponible"}
            
            if product.stock_quantity < quantity:
                return {"error": f"Stock insuffisant. Disponible: {product.stock_quantity}"}
            
            # Vérifier si le produit est déjà dans le panier
            existing_item = db.query(CartItem).filter(
                CartItem.user_id == user_id,
                CartItem.product_id == product_id
            ).first()
            
            if existing_item:
                # Mettre à jour la quantité
                new_quantity = existing_item.quantity + quantity
                if new_quantity > product.stock_quantity:
                    return {"error": f"Quantité totale dépasserait le stock disponible"}
                
                existing_item.quantity = new_quantity
                existing_item.updated_at = datetime.utcnow()
                message = "Quantité mise à jour dans le panier"
            else:
                # Créer un nouvel item
                cart_item = CartItem(
                    user_id=user_id,
                    session_id=session_id,
                    product_id=product_id,
                    quantity=quantity,
                    price=product.price,
                    added_at=datetime.utcnow()
                )
                db.add(cart_item)
                message = "Produit ajouté au panier"
            
            db.commit()
            
            # Récupérer le panier mis à jour
            updated_cart = await self.view_cart_safe(user_id, session_id)
            
            return {
                "success": True,
                "message": message,
                "cart": updated_cart.get("cart", {}),
                "product_added": {
                    "id": product.id,
                    "name": product.name,
                    "quantity": quantity,
                    "price": product.price
                }
            }
            
        except Exception as e:
            if db:
                db.rollback()
            self.logger.error(f"Erreur ajout au panier: {str(e)}")
            return {"error": str(e)}
        finally:
            if db:
                db.close()
    
    async def remove_from_cart_safe(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Supprimer un produit du panier de manière sécurisée"""
        db: Optional[Session] = None
        try:
            user_id = state.get("user_id")
            product_id = state.get("product_id")
            
            if not product_id:
                return {"error": "ID produit requis"}
            
            db = SessionLocal()
            
            # Supprimer l'item du panier
            deleted = db.query(CartItem).filter(
                CartItem.user_id == user_id,
                CartItem.product_id == product_id
            ).delete()
            
            if deleted == 0:
                return {"error": "Produit non trouvé dans le panier"}
            
            db.commit()
            
            # Récupérer le panier mis à jour
            updated_cart = await self.view_cart_safe(user_id, state.get("session_id"))
            
            return {
                "success": True,
                "message": "Produit supprimé du panier",
                "cart": updated_cart.get("cart", {})
            }
            
        except Exception as e:
            if db:
                db.rollback()
            self.logger.error(f"Erreur suppression du panier: {str(e)}")
            return {"error": str(e)}
        finally:
            if db:
                db.close()
    
    async def update_quantity_safe(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Mettre à jour la quantité d'un produit dans le panier"""
        db: Optional[Session] = None
        try:
            user_id = state.get("user_id")
            product_id = state.get("product_id")
            new_quantity = state.get("quantity")
            
            if not all([user_id, product_id, new_quantity]):
                return {"error": "Tous les paramètres sont requis"}
            
            if new_quantity <= 0:
                return await self.remove_from_cart_safe(state)
            
            db = SessionLocal()
            
            # Vérifier le stock disponible
            product = db.query(Product).filter(
                Product.id == product_id,
                Product.is_active == True
            ).first()
            
            if not product:
                return {"error": "Produit non trouvé"}
            
            if product.stock_quantity < new_quantity:
                return {"error": f"Stock insuffisant. Disponible: {product.stock_quantity}"}
            
            # Mettre à jour la quantité
            cart_item = db.query(CartItem).filter(
                CartItem.user_id == user_id,
                CartItem.product_id == product_id
            ).first()
            
            if not cart_item:
                return {"error": "Produit non trouvé dans le panier"}
            
            cart_item.quantity = new_quantity
            cart_item.updated_at = datetime.utcnow()
            
            db.commit()
            
            # Récupérer le panier mis à jour
            updated_cart = await self.view_cart_safe(user_id, state.get("session_id"))
            
            return {
                "success": True,
                "message": "Quantité mise à jour",
                "cart": updated_cart.get("cart", {})
            }
            
        except Exception as e:
            if db:
                db.rollback()
            self.logger.error(f"Erreur mise à jour quantité: {str(e)}")
            return {"error": str(e)}
        finally:
            if db:
                db.close()
    
    async def view_cart_safe(self, user_id: Optional[int], session_id: Optional[str]) -> Dict[str, Any]:
        """Afficher le contenu du panier de manière sécurisée"""
        db: Optional[Session] = None
        try:
            db = SessionLocal()
            
            # Construire la requête selon l'identifiant disponible
            query = db.query(CartItem)
            if user_id:
                query = query.filter(CartItem.user_id == user_id)
            elif session_id:
                query = query.filter(CartItem.session_id == session_id)
            else:
                return {"error": "Identifiant utilisateur ou session requis"}
            
            cart_items = query.all()
            
            if not cart_items:
                return {
                    "cart": {
                        "items": [],
                        "total_items": 0,
                        "total_price": 0.0,
                        "is_empty": True
                    }
                }
            
            # Enrichir avec les informations produit
            enriched_items = []
            total_price = 0.0
            total_items = 0
            
            for item in cart_items:
                product = db.query(Product).filter(Product.id == item.product_id).first()
                if product:
                    item_total = item.price * item.quantity
                    total_price += item_total
                    total_items += item.quantity
                    
                    enriched_items.append({
                        "id": item.id,
                        "product_id": product.id,
                        "name": product.name,
                        "description": product.description,
                        "price": item.price,
                        "quantity": item.quantity,
                        "total": item_total,
                        "image_url": product.image_url,
                        "stock_available": product.stock_quantity,
                        "added_at": item.added_at.isoformat()
                    })
            
            return {
                "cart": {
                    "items": enriched_items,
                    "total_items": total_items,
                    "total_price": round(total_price, 2),
                    "is_empty": False,
                    "item_count": len(enriched_items)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Erreur affichage panier: {str(e)}")
            return {"error": str(e)}
        finally:
            if db:
                db.close()
    
    async def clear_cart_safe(self, user_id: Optional[int], session_id: Optional[str]) -> Dict[str, Any]:
        """Vider le panier de manière sécurisée"""
        db: Optional[Session] = None
        try:
            db = SessionLocal()
            
            # Construire la requête selon l'identifiant disponible
            query = db.query(CartItem)
            if user_id:
                query = query.filter(CartItem.user_id == user_id)
            elif session_id:
                query = query.filter(CartItem.session_id == session_id)
            else:
                return {"error": "Identifiant utilisateur ou session requis"}
            
            deleted_count = query.delete()
            db.commit()
            
            return {
                "success": True,
                "message": f"Panier vidé ({deleted_count} articles supprimés)",
                "deleted_count": deleted_count
            }
            
        except Exception as e:
            if db:
                db.rollback()
            self.logger.error(f"Erreur vidage panier: {str(e)}")
            return {"error": str(e)}
        finally:
            if db:
                db.close()
    
    async def get_complementary_products_safe(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Obtenir des produits complémentaires pour le panier"""
        db: Optional[Session] = None
        try:
            user_id = state.get("user_id")
            limit = state.get("limit", 5)
            
            db = SessionLocal()
            
            # Récupérer les produits dans le panier
            cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
            
            if not cart_items:
                return {"complementary_products": []}
            
            # Analyser les catégories et marques du panier
            cart_categories = set()
            cart_brands = set()
            
            for item in cart_items:
                product = db.query(Product).filter(Product.id == item.product_id).first()
                if product:
                    cart_categories.add(product.category)
                    if product.brand:
                        cart_brands.add(product.brand)
            
            # Trouver des produits complémentaires
            complementary_query = db.query(Product).filter(
                Product.is_active == True,
                Product.stock_quantity > 0,
                Product.id.notin_([item.product_id for item in cart_items])
            )
            
            # Prioriser par catégorie puis par marque
            complementary_products = []
            
            # Produits de même catégorie
            category_products = complementary_query.filter(
                Product.category.in_(cart_categories)
            ).limit(limit // 2).all()
            
            for product in category_products:
                complementary_products.append({
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "category": product.category,
                    "reason": f"Complémentaire à vos achats en {product.category}",
                    "type": "category_complement"
                })
            
            # Produits de même marque
            brand_products = complementary_query.filter(
                Product.brand.in_(cart_brands)
            ).limit(limit - len(complementary_products)).all()
            
            for product in brand_products:
                if len(complementary_products) < limit:
                    complementary_products.append({
                        "id": product.id,
                        "name": product.name,
                        "price": product.price,
                        "brand": product.brand,
                        "reason": f"De votre marque préférée {product.brand}",
                        "type": "brand_complement"
                    })
            
            return {
                "complementary_products": complementary_products,
                "total_found": len(complementary_products),
                "cart_analysis": {
                    "categories": list(cart_categories),
                    "brands": list(cart_brands),
                    "total_items": len(cart_items)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Erreur produits complémentaires: {str(e)}")
            return {"error": str(e)}
        finally:
            if db:
                db.close()
    
    async def get_abandoned_cart_reminder_safe(self, user_id: int) -> Dict[str, Any]:
        """Récupérer le rappel du panier abandonné"""
        db: Optional[Session] = None
        try:
            db = SessionLocal()
            
            # Vérifier s'il y a un panier abandonné (plus de 24h)
            cutoff_time = datetime.utcnow() - timedelta(hours=24)
            
            abandoned_items = db.query(CartItem).filter(
                CartItem.user_id == user_id,
                CartItem.updated_at < cutoff_time
            ).all()
            
            if not abandoned_items:
                return {"has_abandoned_cart": False}
            
            # Enrichir avec les informations produit
            reminder_items = []
            total_value = 0.0
            
            for item in abandoned_items:
                product = db.query(Product).filter(Product.id == item.product_id).first()
                if product and product.is_active and product.stock_quantity > 0:
                    item_value = item.price * item.quantity
                    total_value += item_value
                    
                    reminder_items.append({
                        "product_id": product.id,
                        "name": product.name,
                        "price": item.price,
                        "quantity": item.quantity,
                        "total": item_value,
                        "image_url": product.image_url,
                        "still_available": product.stock_quantity >= item.quantity
                    })
            
            return {
                "has_abandoned_cart": True,
                "abandoned_items": reminder_items,
                "total_value": round(total_value, 2),
                "item_count": len(reminder_items),
                "message": f"Vous avez {len(reminder_items)} article(s) dans votre panier abandonné d'une valeur de {round(total_value, 2)}€"
            }
            
        except Exception as e:
            self.logger.error(f"Erreur rappel panier abandonné: {str(e)}")
            return {"error": str(e)}
        finally:
            if db:
                db.close()
    
    async def calculate_cart_total_safe(self, user_id: Optional[int], session_id: Optional[str]) -> Dict[str, Any]:
        """Calculer le total du panier avec promotions"""
        try:
            cart_data = await self.view_cart_safe(user_id, session_id)
            
            if cart_data.get("error"):
                return cart_data
            
            cart = cart_data.get("cart", {})
            subtotal = cart.get("total_price", 0.0)
            
            # Calculer les réductions (exemple simplifié)
            discount_percentage = 0.0
            if subtotal > 100:
                discount_percentage = 10.0  # 10% de réduction au-dessus de 100€
            elif subtotal > 50:
                discount_percentage = 5.0   # 5% de réduction au-dessus de 50€
            
            discount_amount = (subtotal * discount_percentage) / 100
            total_with_discount = subtotal - discount_amount
            
            # Frais de livraison (exemple simplifié)
            shipping_cost = 0.0
            if subtotal < 50:
                shipping_cost = 5.99
            
            final_total = total_with_discount + shipping_cost
            
            return {
                "subtotal": round(subtotal, 2),
                "discount_percentage": discount_percentage,
                "discount_amount": round(discount_amount, 2),
                "shipping_cost": round(shipping_cost, 2),
                "final_total": round(final_total, 2),
                "savings": round(discount_amount, 2),
                "free_shipping_threshold": 50.0,
                "next_discount_threshold": 100.0 if subtotal < 100 else None
            }
            
        except Exception as e:
            self.logger.error(f"Erreur calcul total: {str(e)}")
            return {"error": str(e)}
    
    async def get_payment_options_safe(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Obtenir les options de paiement disponibles"""
        try:
            user_id = state.get("user_id")
            cart_total = state.get("cart_total", 0.0)
            
            # Options de paiement de base
            payment_options = [
                {
                    "id": "card",
                    "name": "Carte bancaire",
                    "description": "Visa, Mastercard, American Express",
                    "icon": "💳",
                    "available": True,
                    "processing_time": "immédiat"
                },
                {
                    "id": "paypal",
                    "name": "PayPal",
                    "description": "Paiement sécurisé via PayPal",
                    "icon": "🔒",
                    "available": True,
                    "processing_time": "immédiat"
                },
                {
                    "id": "apple_pay",
                    "name": "Apple Pay",
                    "description": "Paiement mobile Apple",
                    "icon": "📱",
                    "available": True,
                    "processing_time": "immédiat"
                },
                {
                    "id": "google_pay",
                    "name": "Google Pay",
                    "description": "Paiement mobile Google",
                    "icon": "📱",
                    "available": True,
                    "processing_time": "immédiat"
                }
            ]
            
            # Ajouter le paiement en plusieurs fois si le montant le permet
            if cart_total > 200:
                payment_options.append({
                    "id": "installments",
                    "name": "Paiement en 3x",
                    "description": "Paiement en 3 fois sans frais",
                    "icon": "📅",
                    "available": True,
                    "processing_time": "immédiat",
                    "installment_count": 3,
                    "installment_amount": round(cart_total / 3, 2)
                })
            
            # Ajouter le paiement à la livraison pour les montants modérés
            if cart_total < 100:
                payment_options.append({
                    "id": "cash_on_delivery",
                    "name": "Paiement à la livraison",
                    "description": "Payer en espèces à la réception",
                    "icon": "💰",
                    "available": True,
                    "processing_time": "à la livraison",
                    "additional_fee": 2.99
                })
            
            return {
                "payment_options": payment_options,
                "total_options": len(payment_options),
                "recommended": "card" if cart_total < 100 else "installments",
                "cart_total": cart_total,
                "currency": "EUR"
            }
            
        except Exception as e:
            self.logger.error(f"Erreur options de paiement: {str(e)}")
            return {"error": str(e)}

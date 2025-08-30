from .base_agent import BaseAgent
from fastapi import APIRouter, FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
import logging

# Import des modèles (à adapter selon ta structure)
try:
    from catalogue.backend.database import SessionLocal
    from catalogue.backend.models import Panier, PanierProduit, Product, Utilisateur
except ImportError:
    # Fallback si les modèles ne sont pas disponibles
    SessionLocal = None
    Panier = PanierProduit = Product = Utilisateur = None

# Agent de gestion du panier
class CartManagementAgent(BaseAgent):
    """
    Agent pour la gestion du panier e-commerce (PostgreSQL).

    Exemples d'utilisation :
    >>> agent = CartManagementAgent()
    >>> agent.add_to_cart(user_id=1, product_id=2, quantite=3)
    >>> agent.get_cart(user_id=1)
    >>> agent.remove_from_cart(user_id=1, product_id=2)
    >>> agent.clear_cart(user_id=1)
    """
    def __init__(self):
        super().__init__(
            name="cart_management_agent",
            description="Agent de gestion du panier e-commerce"
        )
        self.logger = logging.getLogger("cart_management_agent")

    def get_system_prompt(self) -> str:
        return """
        Vous êtes un expert en gestion de panier e-commerce.
        Votre rôle est d'aider les utilisateurs à gérer leur panier d'achat.
        
        Capacités:
        - Ajouter des produits au panier
        - Retirer des produits du panier
        - Voir le contenu du panier
        - Vider le panier
        - Calculer les totaux
        
        Soyez toujours précis et sécurisé dans la gestion des données.
        """

    def get_db(self):
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    async def execute(self, state: dict) -> dict:
        """
        Exécution orchestrée par le SMA.
        Attend dans state: cart_action in {view, add, remove, clear}, user_id, product_id, quantity
        """
        action = state.get("cart_action", "view")
        user_id = state.get("user_id")
        product_id = state.get("product_id")
        quantity = state.get("quantity", 1)
        if not isinstance(user_id, int) or user_id <= 0:
            return {
                "response_text": "Pour gérer le panier, veuillez vous connecter ou fournir un identifiant utilisateur.",
                "cart": {"items": [], "total_items": 0, "total_price": 0.0, "is_empty": True}
            }
        db: Optional[Session] = None
        try:
            db = SessionLocal()
            if action == "add":
                if not product_id:
                    return {"response_text": "Spécifiez l'ID du produit à ajouter (ex: ajouter produit 58)", "cart": self.get_cart(db, user_id)}
                cart = self.add_to_cart(db, user_id, product_id, quantite=quantity)
                return {"response_text": f"Produit {product_id} ajouté au panier.", "cart": cart}
            elif action == "remove":
                if not product_id:
                    return {"response_text": "Spécifiez l'ID du produit à retirer (ex: retirer produit 58)", "cart": self.get_cart(db, user_id)}
                cart = self.remove_from_cart(db, user_id, product_id)
                return {"response_text": f"Produit {product_id} retiré du panier.", "cart": cart}
            elif action == "clear":
                self.clear_cart(db, user_id)
                return {"response_text": "Panier vidé avec succès.", "cart": {"items": [], "total_items": 0, "total_price": 0.0, "is_empty": True}}
            else:  # view
                cart = self.get_cart(db, user_id)
                items = cart.get("produits", [])
                if not items:
                    return {"response_text": "Votre panier est vide.", "cart": {"items": [], "total_items": 0, "total_price": 0.0, "is_empty": True}}
                total = cart.get("total", 0.0)
                # Adapter la structure à l'UI SMA (items, total_price)
                ui_cart = {
                    "items": [{"product_id": it["id"], "name": it["nom"], "quantity": it["quantite"], "total": it["total_partiel"]} for it in items],
                    "total_items": sum(it["quantite"] for it in items),
                    "total_price": total,
                    "is_empty": False,
                }
                return {"response_text": "Voici votre panier.", "cart": ui_cart}
        except HTTPException as e:
            return {"response_text": e.detail, "cart": {"items": [], "total_items": 0, "total_price": 0.0, "is_empty": True}}
        except Exception as e:
            self.logger.error(f"Erreur execute panier: {e}")
            return {"response_text": "Erreur lors de la gestion du panier.", "cart": {"items": [], "total_items": 0, "total_price": 0.0, "is_empty": True}}
        finally:
            if db:
                db.close()
    
    def _get_or_create_panier(self, db: Session, user_id: int) -> Panier:
        panier = db.query(Panier).filter_by(utilisateur_id=user_id).first()
        if not panier:
            panier = Panier(utilisateur_id=user_id, date_creation=datetime.utcnow())
            db.add(panier)
            db.commit()
            db.refresh(panier)
        return panier

    def add_to_cart(self, db: Session, user_id: int, product_id: int, quantite: int = 1):
        if quantite <= 0:
            raise HTTPException(status_code=400, detail="La quantité doit être positive.")
        product = db.query(Product).filter_by(id=product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Produit introuvable.")
        if product.stock < quantite:
            raise HTTPException(status_code=400, detail="Stock insuffisant.")
        panier = self._get_or_create_panier(db, user_id)
        panier_produit = db.query(PanierProduit).filter_by(id_panier=panier.id, id_produit=product_id).first()
        if panier_produit:
            panier_produit.quantite += quantite
        else:
            panier_produit = PanierProduit(id_panier=panier.id, id_produit=product_id, quantite=quantite)
            db.add(panier_produit)
        db.commit()
        return self.get_cart(db, user_id)

    def remove_from_cart(self, db: Session, user_id: int, product_id: int):
        panier = db.query(Panier).filter_by(utilisateur_id=user_id).first()
        if not panier:
            raise HTTPException(status_code=404, detail="Panier introuvable.")
        panier_produit = db.query(PanierProduit).filter_by(id_panier=panier.id, id_produit=product_id).first()
        if not panier_produit:
            raise HTTPException(status_code=404, detail="Produit non présent dans le panier.")
        if panier_produit.quantite > 1:
            panier_produit.quantite -= 1
        else:
            db.delete(panier_produit)
        db.commit()
        return self.get_cart(db, user_id)

    def get_cart(self, db: Session, user_id: int):
        panier = db.query(Panier).filter_by(utilisateur_id=user_id).first()
        if not panier:
            return {"produits": [], "total": 0.0}
        items = db.query(PanierProduit).filter_by(id_panier=panier.id).all()
        produits = []
        total = 0.0
        for item in items:
            produit = db.query(Product).filter_by(id=item.id_produit).first()
            if produit:
                sous_total = float(produit.prix) * item.quantite
                total += sous_total
                produits.append({
                    "id": produit.id,
                    "nom": produit.nom,
                    "prix": float(produit.prix),
                    "quantite": item.quantite,
                    "total_partiel": sous_total
                })
        return {"produits": produits, "total": round(total, 2)}

    def clear_cart(self, db: Session, user_id: int):
        panier = db.query(Panier).filter_by(utilisateur_id=user_id).first()
        if not panier:
            return {"message": "Panier déjà vide."}
        db.query(PanierProduit).filter_by(id_panier=panier.id).delete()
        db.commit()
        return {"message": "Panier vidé avec succès."}

# --- FastAPI endpoints ---

class AddToCartRequest(BaseModel):
    user_id: int
    product_id: int
    quantite: int = 1

class RemoveFromCartRequest(BaseModel):
    user_id: int
    product_id: int

class ClearCartRequest(BaseModel):
    user_id: int

agent = CartManagementAgent()
router = APIRouter()

@router.post("/cart/add")
def add_to_cart(req: AddToCartRequest, db: Session = Depends(agent.get_db)):
    """Ajouter un produit au panier."""
    return agent.add_to_cart(db, req.user_id, req.product_id, req.quantite)

@router.post("/cart/remove")
def remove_from_cart(req: RemoveFromCartRequest, db: Session = Depends(agent.get_db)):
    """Supprimer un produit du panier (décrémente ou retire)."""
    return agent.remove_from_cart(db, req.user_id, req.product_id)

@router.get("/cart/view")
def view_cart(user_id: int, db: Session = Depends(agent.get_db)):
    """Afficher le contenu du panier et le total."""
    return agent.get_cart(db, user_id)

@router.post("/cart/clear")
def clear_cart(req: ClearCartRequest, db: Session = Depends(agent.get_db)):
    """Vider le panier."""
    return agent.clear_cart(db, req.user_id)

# Pour intégration directe dans FastAPI
app = FastAPI()
app.include_router(router)

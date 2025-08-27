from fastapi import APIRouter, FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from catalogue.backend.database import SessionLocal
from catalogue.backend.models import Panier, PanierProduit, Product, Utilisateur
from datetime import datetime
import logging

# Agent de gestion du panier
class CartManagementAgent:
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
        self.logger = logging.getLogger("cart_management_agent")

    def get_db(self):
            db = SessionLocal()
        try:
            yield db
        finally:
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

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from catalogue.backend.database import SessionLocal
from catalogue.backend.models import Panier, PanierProduit, Product
from datetime import datetime

router = APIRouter()

# --- Schemas ---
class AddToCartRequest(BaseModel):
    user_id: int
    product_id: int
    quantite: int = 1

class RemoveFromCartRequest(BaseModel):
    user_id: int
    product_id: int

class UpdateCartRequest(BaseModel):
    user_id: int
    product_id: int
    quantite: int

class ClearCartRequest(BaseModel):
    user_id: int

# DB dep

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helpers

def _get_or_create_panier(db: Session, user_id: int) -> Panier:
    panier = db.query(Panier).filter_by(utilisateur_id=user_id).first()
    if not panier:
        panier = Panier(utilisateur_id=user_id, date_creation=datetime.utcnow())
        db.add(panier)
        db.commit()
        db.refresh(panier)
    return panier

@router.get("/{user_id}")
def get_cart(user_id: int, db: Session = Depends(get_db)):
    panier = db.query(Panier).filter_by(utilisateur_id=user_id).first()
    if not panier:
        return {"produits": [], "total": 0.0}
    items = db.query(PanierProduit).filter_by(id_panier=panier.id).all()
    total = 0.0
    produits = []
    for item in items:
        p = db.query(Product).filter_by(id=item.id_produit).first()
        if p:
            st = float(p.prix) * item.quantite
            total += st
            produits.append({
                "id": p.id,
                "nom": p.nom,
                "prix": float(p.prix),
                "quantite": item.quantite,
                "total_partiel": st
            })
    return {"produits": produits, "total": round(total, 2)}

@router.post("/add")
def add_to_cart(req: AddToCartRequest, db: Session = Depends(get_db)):
    if req.quantite <= 0:
        raise HTTPException(status_code=400, detail="Quantité invalide")
    prod = db.query(Product).filter_by(id=req.product_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    if prod.stock < req.quantite:
        raise HTTPException(status_code=400, detail="Stock insuffisant")
    panier = _get_or_create_panier(db, req.user_id)
    item = db.query(PanierProduit).filter_by(id_panier=panier.id, id_produit=req.product_id).first()
    if item:
        item.quantite += req.quantite
    else:
        item = PanierProduit(id_panier=panier.id, id_produit=req.product_id, quantite=req.quantite)
        db.add(item)
    db.commit()
    return get_cart(req.user_id, db)

@router.delete("/remove")
def remove_from_cart(req: RemoveFromCartRequest, db: Session = Depends(get_db)):
    panier = db.query(Panier).filter_by(utilisateur_id=req.user_id).first()
    if not panier:
        raise HTTPException(status_code=404, detail="Panier introuvable")
    item = db.query(PanierProduit).filter_by(id_panier=panier.id, id_produit=req.product_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Produit non présent")
    if item.quantite > 1:
        item.quantite -= 1
    else:
        db.delete(item)
    db.commit()
    return get_cart(req.user_id, db)

@router.put("/update")
def update_cart(req: UpdateCartRequest, db: Session = Depends(get_db)):
    if req.quantite < 0:
        raise HTTPException(status_code=400, detail="Quantité invalide")
    panier = db.query(Panier).filter_by(utilisateur_id=req.user_id).first()
    if not panier:
        raise HTTPException(status_code=404, detail="Panier introuvable")
    item = db.query(PanierProduit).filter_by(id_panier=panier.id, id_produit=req.product_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Produit non présent")
    if req.quantite == 0:
        db.delete(item)
    else:
        prod = db.query(Product).filter_by(id=req.product_id).first()
        if not prod:
            raise HTTPException(status_code=404, detail="Produit introuvable")
        if prod.stock < req.quantite:
            raise HTTPException(status_code=400, detail="Stock insuffisant")
        item.quantite = req.quantite
    db.commit()
    return get_cart(req.user_id, db)

@router.delete("/clear")
def clear_cart(req: ClearCartRequest, db: Session = Depends(get_db)):
    panier = db.query(Panier).filter_by(utilisateur_id=req.user_id).first()
    if not panier:
        return {"message": "Panier déjà vide."}
    db.query(PanierProduit).filter_by(id_panier=panier.id).delete()
    db.commit()
    return {"message": "Panier vidé avec succès."}

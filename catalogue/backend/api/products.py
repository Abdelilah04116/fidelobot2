from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from catalogue.backend.database import SessionLocal
from catalogue.backend.models import Product, Category
from catalogue.backend.qdrant_client import search_embedding

# Optionnel: encodeur d'embedding
try:
    from sentence_transformers import SentenceTransformer
    _embedder = SentenceTransformer("all-MiniLM-L6-v2")
except Exception:
    _embedder = None

router = APIRouter()

# --- Schemas ---
class ProductCreateRequest(BaseModel):
    nom: str
    prix: float
    stock: int
    categorie_id: int
    description: Optional[str] = None
    caracteristiques: Optional[Dict[str, Any]] = None

class ProductUpdateRequest(BaseModel):
    nom: Optional[str] = None
    prix: Optional[float] = None
    stock: Optional[int] = None
    categorie_id: Optional[int] = None
    description: Optional[str] = None
    caracteristiques: Optional[Dict[str, Any]] = None

class ProductSearchRequest(BaseModel):
    query: str
    filters: Optional[Dict[str, Any]] = None
    limit: int = 10

# Dépendance DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Endpoints ---
@router.get("/")
def get_products(db: Session = Depends(get_db), skip: int = 0, limit: int = 20,
                 categorie_id: Optional[int] = Query(None), q: Optional[str] = Query(None)):
    query = db.query(Product)
    if categorie_id is not None:
        query = query.filter(Product.categorie_id == categorie_id)
    if q:
        like = f"%{q}%"
        query = query.filter(Product.nom.ilike(like))
    items = query.offset(skip).limit(limit).all()
    return [{
        "id": p.id,
        "nom": p.nom,
        "prix": float(p.prix),
        "stock": p.stock,
        "categorie_id": p.categorie_id,
        "description": p.description_courte,
        "caracteristiques": p.caracteristiques_structurees
    } for p in items]

@router.get("/{id}")
def get_product(id: int, db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.id == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    return {
        "id": p.id,
        "nom": p.nom,
        "prix": float(p.prix),
        "stock": p.stock,
        "categorie_id": p.categorie_id,
        "description": p.description_courte,
        "caracteristiques": p.caracteristiques_structurees
    }

@router.post("/search")
def search_products(req: ProductSearchRequest, db: Session = Depends(get_db)):
    if _embedder is None:
        raise HTTPException(status_code=503, detail="Embedder indisponible")
    try:
        vector = _embedder.encode(req.query)
        hits = search_embedding("produits_embeddings", vector, top_k=req.limit)
        ids = [int(hit.id) for hit in hits]
        if not ids:
            return []
        products = db.query(Product).filter(Product.id.in_(ids)).all()
        # Conserver l'ordre par score
        score_by_id = {int(hit.id): float(hit.score) for hit in hits}
        products_sorted = sorted(products, key=lambda p: score_by_id.get(p.id, 0.0), reverse=True)
        return [{
            "id": p.id,
            "nom": p.nom,
            "prix": float(p.prix),
            "stock": p.stock,
            "categorie_id": p.categorie_id,
            "description": p.description_courte,
            "score": score_by_id.get(p.id, 0.0)
        } for p in products_sorted]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur recherche sémantique: {e}")

@router.get("/recommendations")
def get_recommendations(user_id: Optional[int] = None, limit: int = 10, db: Session = Depends(get_db)):
    # Recommandations basiques: produits en stock les moins chers
    products = db.query(Product).filter(Product.stock > 0).order_by(Product.prix.asc()).limit(limit).all()
    return [{"id": p.id, "nom": p.nom, "prix": float(p.prix)} for p in products]

@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    cats = db.query(Category).all()
    return [{"id": c.id, "nom": c.nom} for c in cats]

@router.get("/brands")
def get_brands():
    # Pas de colonne marque dans le modèle actuel
    return []

@router.get("/stats")
def get_product_stats(db: Session = Depends(get_db)):
    count = db.query(func.count(Product.id)).scalar() or 0
    avg_price = db.query(func.avg(Product.prix)).scalar()
    min_price = db.query(func.min(Product.prix)).scalar()
    max_price = db.query(func.max(Product.prix)).scalar()
    return {
        "count": int(count),
        "avg_price": float(avg_price) if avg_price is not None else 0.0,
        "min_price": float(min_price) if min_price is not None else 0.0,
        "max_price": float(max_price) if max_price is not None else 0.0
    }

@router.post("/")
def create_product(req: ProductCreateRequest, db: Session = Depends(get_db)):
    p = Product(
        nom=req.nom,
        prix=req.prix,
        stock=req.stock,
        categorie_id=req.categorie_id,
        description_courte=req.description,
        caracteristiques_structurees=req.caracteristiques or {}
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return {"id": p.id}

@router.put("/{id}")
def update_product(id: int, req: ProductUpdateRequest, db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.id == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    if req.nom is not None:
        p.nom = req.nom
    if req.prix is not None:
        p.prix = req.prix
    if req.stock is not None:
        p.stock = req.stock
    if req.categorie_id is not None:
        p.categorie_id = req.categorie_id
    if req.description is not None:
        p.description_courte = req.description
    if req.caracteristiques is not None:
        p.caracteristiques_structurees = req.caracteristiques
    db.commit()
    return {"success": True}

@router.delete("/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.id == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    db.delete(p)
    db.commit()
    return {"success": True}

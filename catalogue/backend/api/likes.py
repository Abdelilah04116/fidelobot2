from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Set

router = APIRouter()

# Démo en mémoire: mapping product_id -> set(user_ids)
_likes_by_product: Dict[int, Set[int]] = {}

class ToggleLikeRequest(BaseModel):
    user_id: int
    product_id: int

class CheckLikeRequest(BaseModel):
    user_id: int
    product_id: int

@router.post("/toggle")
def toggle_like(req: ToggleLikeRequest):
    users = _likes_by_product.setdefault(req.product_id, set())
    if req.user_id in users:
        users.remove(req.user_id)
        liked = False
    else:
        users.add(req.user_id)
        liked = True
    return {"liked": liked, "count": len(users)}

@router.get("/user/{user_id}")
def get_user_likes(user_id: int):
    products = [pid for pid, users in _likes_by_product.items() if user_id in users]
    return {"user_id": user_id, "products": products, "count": len(products)}

@router.get("/product/{product_id}")
def get_product_like_count(product_id: int):
    users = _likes_by_product.get(product_id, set())
    return {"product_id": product_id, "count": len(users)}

@router.post("/check")
def check_user_like(req: CheckLikeRequest):
    users = _likes_by_product.get(req.product_id, set())
    return {"liked": req.user_id in users}

@router.get("/popular")
def get_popular_likes(top: int = 10):
    ranked = sorted(((pid, len(users)) for pid, users in _likes_by_product.items()), key=lambda x: x[1], reverse=True)
    ranked = ranked[:top]
    return [{"product_id": pid, "count": count} for pid, count in ranked]

from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def api_health():
    return {"status": "ok"}

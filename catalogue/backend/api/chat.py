from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from SMA.core.orchestrator import chatbot_orchestrator

router = APIRouter()

# --- Schemas ---
class ChatMessageRequest(BaseModel):
    session_id: str
    user_id: Optional[int] = None
    message: str

# Mémoire simple en process pour l'historique (à remplacer par DB si besoin)
_chat_histories = {}

@router.post("/message")
async def send_message(req: ChatMessageRequest):
    try:
        result = await chatbot_orchestrator.process_message(
            message=req.message,
            session_id=req.session_id,
            user_id=req.user_id
        )
        # Stocker historique simple
        _chat_histories.setdefault(req.session_id, []).append({
            "user": req.user_id,
            "message": req.message,
            "response": result.get("response")
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{session_id}")
def get_chat_history(session_id: str):
    return _chat_histories.get(session_id, [])

@router.get("/sessions")
def get_user_sessions():
    # Implémentation minimale: retourne les clés connues
    return list(_chat_histories.keys())

@router.delete("/sessions/{id}")
def delete_chat_session(id: str):
    _chat_histories.pop(id, None)
    return {"success": True}

@router.post("/sessions/{id}/clear")
def clear_chat_history(id: str):
    _chat_histories[id] = []
    return {"success": True}

@router.get("/health")
def chat_health():
    return {"status": "ok", "sessions": len(_chat_histories)}

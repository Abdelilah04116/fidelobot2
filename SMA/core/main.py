"""
Application principale FastAPI pour le SMA
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import json
import logging
import base64
from datetime import datetime

# Import des modules du SMA
from .orchestrator import chatbot_orchestrator
from .voice_endpoints import voice_router  # Nouveau import

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Création de l'application FastAPI
app = FastAPI(
    title="SMA - Système Multi-Agent Fidelo",
    description="API pour le système multi-agent avec traitement vocal",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routers
app.include_router(voice_router)  # Nouveau router vocal

# Modèles Pydantic
class ChatMessage(BaseModel):
    message: str
    session_id: str
    user_id: Optional[int] = None
    audio_data: Optional[str] = None  # Base64 encoded audio
    audio_format: Optional[str] = "webm"

class ChatResponse(BaseModel):
    success: bool
    response: str
    intent: Optional[str] = None
    escalate: bool = False
    agents_used: List[str] = []
    processing_time: float = 0.0
    products: List[Dict] = []
    recommendations: List[Dict] = []

# Gestionnaire de connexions WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket
        logger.info(f"WebSocket connecté pour session {session_id}")

    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]
            logger.info(f"WebSocket déconnecté pour session {session_id}")
    
    async def send_message(self, session_id: str, message: Dict[str, Any]):
        if session_id in self.active_connections:
            try:
                await self.active_connections[session_id].send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Erreur envoi message WebSocket: {e}")
                self.disconnect(session_id)

manager = ConnectionManager()

# Endpoints REST
@app.get("/")
async def root():
    """Endpoint racine"""
    return {
        "message": "SMA - Système Multi-Agent Fidelo",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Vérification de santé du système"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "agents": list(chatbot_orchestrator.agents.keys())
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatMessage):
    """
    Endpoint REST pour le chat
    Supporte les messages texte et audio
    """
    try:
        logger.info(f"[chat_endpoint] Début du traitement pour: {request.message}")
        
        # Si c'est un message audio, décoder les données
        audio_bytes = None
        if request.audio_data:
            try:
                audio_bytes = base64.b64decode(request.audio_data)
                logger.info(f"[chat_endpoint] Audio reçu pour session {request.session_id}")
            except Exception as e:
                logger.error(f"Erreur décodage audio: {e}")
                raise HTTPException(status_code=400, detail="Format audio invalide")
        
        # Traiter le message
    result = await chatbot_orchestrator.process_message(
            message=request.message,
            session_id=request.session_id,
            user_id=request.user_id,
            audio_data=audio_bytes,
            audio_format=request.audio_format
        )
        
        return ChatResponse(**result)
        
    except Exception as e:
        logger.error(f"Erreur dans chat_endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint WebSocket
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str, user_id: Optional[int] = None):
    """
    Endpoint WebSocket pour le chat en temps réel
    Supporte les messages texte et audio
    """
    await manager.connect(websocket, session_id)
    
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            user_message = message_data.get("message", "")
            audio_data = message_data.get("audio_data")
            audio_format = message_data.get("audio_format", "webm")
            
            if not user_message.strip() and not audio_data:
                continue
            
            await manager.send_message(session_id, {
                "type": "typing",
                "message": "L'assistant réfléchit...",
                "timestamp": datetime.utcnow().isoformat()
            })
            
            audio_bytes = None
            if audio_data:
                try:
                    audio_bytes = base64.b64decode(audio_data)
                    logger.info(f"Audio reçu pour session {session_id}")
                    
                    # Traiter l'audio avec l'agent voix
                    audio_result = await chatbot_orchestrator.process_message(
                        message="",
                        session_id=session_id,
                        user_id=user_id,
                        audio_data=audio_bytes,
                        audio_format=audio_format
                    )
                    
                    # Si transcription réussie, envoyer le texte transcrit
                    if audio_result.get("success") and audio_result.get("response"):
                        await manager.send_message(session_id, {
                            "type": "response",
                            "transcribed_text": audio_result["response"],
                            "timestamp": datetime.utcnow().isoformat()
                        })
                        # Ne pas continuer avec le traitement normal pour l'audio
                        continue
                    else:
                        # Erreur de transcription
                        await manager.send_message(session_id, {
                            "type": "error",
                            "message": "Erreur lors de la transcription audio. Veuillez réessayer.",
                            "timestamp": datetime.utcnow().isoformat()
                        })
                        continue
                        
                except Exception as e:
                    logger.error(f"Erreur décodage audio: {e}")
                    await manager.send_message(session_id, {
                        "type": "error",
                        "message": "Erreur lors du traitement de l'audio",
                        "timestamp": datetime.utcnow().isoformat()
                    })
                    continue
            
            # Traiter le message texte normal
            result = await chatbot_orchestrator.process_message(
                message=user_message,
                session_id=session_id,
                user_id=user_id
            )
            
            if result.get("success"):
                await manager.send_message(session_id, {
                "type": "response",
                "message": result["response"],
                    "intent": result.get("intent"),
                    "products": result.get("products", []),
                    "cart": result.get("cart", {}),
                    "timestamp": datetime.utcnow().isoformat()
                })
            else:
                await manager.send_message(session_id, {
                    "type": "error",
                    "message": result.get("response", "Une erreur s'est produite"),
                "timestamp": datetime.utcnow().isoformat()
                })
            
    except WebSocketDisconnect:
        manager.disconnect(session_id)
    except Exception as e:
        logger.error(f"Erreur WebSocket: {e}")
        try:
        await manager.send_message(session_id, {
            "type": "error",
                "message": "Erreur de connexion",
            "timestamp": datetime.utcnow().isoformat()
        })
        except:
            pass
        manager.disconnect(session_id)

# Endpoints d'information
@app.get("/agents")
async def get_agents():
    """Obtenir la liste des agents disponibles"""
    agents_info = {}
    for name, agent in chatbot_orchestrator.agents.items():
        try:
            agents_info[name] = agent.get_capabilities()
        except Exception as e:
            agents_info[name] = {"error": str(e)}
    
    return {
        "agents": agents_info,
        "total_agents": len(chatbot_orchestrator.agents)
    }

@app.get("/capabilities")
async def get_system_capabilities():
    """Obtenir les capacités du système"""
    return {
        "system": "SMA - Système Multi-Agent Fidelo",
        "capabilities": [
            "text_processing",
            "voice_processing", 
            "intent_extraction",
            "product_recommendations",
            "cart_management",
            "multilingual_support"
        ],
        "voice_endpoints": [
            "/voice/chat",
            "/voice/transcribe", 
            "/voice/synthesize",
            "/voice/intent",
            "/voice/upload",
            "/voice/capabilities",
            "/voice/languages",
            "/voice/health"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
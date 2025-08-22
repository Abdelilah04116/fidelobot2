# main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, List, Optional
import json
import asyncio
import uuid
import base64
from datetime import datetime

# Imports locaux
from .orchestrator import chatbot_orchestrator
from SMA.models.database import SessionLocal, User, Conversation
from .auth import authenticate_user, create_access_token, get_current_user
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialisation de l'application
app = FastAPI(
    title="E-Commerce Chatbot API",
    description="API pour chatbot e-commerce avec agents LangGraph et Gemini 2.0",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sécurité
security = HTTPBearer()

# Modèles Pydantic
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_id: Optional[int] = None
    audio_data: Optional[str] = None  # Base64 encoded audio
    audio_format: Optional[str] = "webm"

class ChatResponse(BaseModel):
    success: bool
    response: str
    intent: str
    session_id: str
    escalate: bool
    agents_used: List[str]
    processing_time: float
    products: List[Dict] = []
    recommendations: List[Dict] = []
    cart: Dict = {}

class UserLogin(BaseModel):
    email: str
    password: str

class WebSocketConnection:
    def __init__(self, websocket: WebSocket, session_id: str, user_id: Optional[int] = None):
        self.websocket = websocket
        self.session_id = session_id
        self.user_id = user_id
        self.is_active = True

# Gestionnaire de connexions WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocketConnection] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str, user_id: Optional[int] = None):
        await websocket.accept()
        connection = WebSocketConnection(websocket, session_id, user_id)
        self.active_connections[session_id] = connection
        logger.info(f"Nouvelle connexion WebSocket: {session_id}")
        
        # Message de bienvenue
        welcome_message = await self.get_welcome_message(user_id)
        await self.send_message(session_id, welcome_message)
    
    async def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            self.active_connections[session_id].is_active = False
            del self.active_connections[session_id]
            logger.info(f"Déconnexion WebSocket: {session_id}")
    
    async def send_message(self, session_id: str, message: Dict):
        if session_id in self.active_connections:
            connection = self.active_connections[session_id]
            if connection.is_active:
                try:
                    await connection.websocket.send_text(json.dumps(message, ensure_ascii=False))
                except:
                    await self.disconnect(session_id)
    
    async def get_welcome_message(self, user_id: Optional[int] = None) -> Dict:
        """Générer un message de bienvenue personnalisé"""
        if user_id:
            db = SessionLocal()
            try:
                user = db.query(User).filter(User.id == user_id).first()
                if user:
                    welcome_text = f"Bonjour {user.username} ! Comment puis-je vous aider aujourd'hui ?"
                    if user.is_vip:
                        welcome_text += " En tant que client VIP, vous bénéficiez de notre service prioritaire."
                else:
                    welcome_text = "Bonjour ! Comment puis-je vous aider ?"
            finally:
                db.close()
        else:
            welcome_text = ("Bonjour ! Je suis votre assistant shopping. "
                          "Je peux vous aider à trouver des produits, vérifier vos commandes, "
                          "et vous donner des recommandations personnalisées. "
                          "Que recherchez-vous aujourd'hui ?")
        
        return {
            "type": "welcome",
            "message": welcome_text,
            "timestamp": datetime.utcnow().isoformat(),
            "suggested_actions": [
                "Rechercher un produit",
                "Voir mes commandes",
                "Recommandations personnalisées",
                "Aide et support"
            ]
        }

manager = ConnectionManager()

# Routes d'authentification
@app.post("/auth/login")
async def login(user_credentials: UserLogin):
    """Connexion utilisateur"""
    user = authenticate_user(user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect"
        )
    
    access_token = create_access_token(data={"sub": user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
        "is_vip": user.is_vip
    }

@app.get("/auth/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Obtenir les informations de l'utilisateur actuel"""
    return {
        "user_id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "is_vip": current_user.is_vip,
        "preferences": current_user.preferences
    }

# Routes du chatbot
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(message: ChatMessage):
    """Endpoint REST pour le chat (utilise l'orchestrateur SMA)"""
    session_id = message.session_id or str(uuid.uuid4())
    
    # Traiter l'audio si présent
    audio_data = None
    if message.audio_data:
        try:
            audio_data = base64.b64decode(message.audio_data)
        except Exception as e:
            logger.error(f"Erreur décodage audio: {e}")
            raise HTTPException(status_code=400, detail="Format audio invalide")
    
    result = await chatbot_orchestrator.process_message(
        message=message.message,
        session_id=session_id,
        user_id=message.user_id,
        audio_data=audio_data,
        audio_format=message.audio_format
    )
    
    response = ChatResponse(
        success=result.get("success", True),
        response=result.get("response", ""),
        intent=result.get("intent", "unknown"),
        session_id=session_id,
        escalate=result.get("escalate", False),
        agents_used=result.get("agents_used", []),
        processing_time=result.get("processing_time", 0.0),
        products=result.get("products", []),
        recommendations=result.get("recommendations", []),
        cart=result.get("cart", {})
    )
    
    return response

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str, user_id: Optional[int] = None):
    """Endpoint WebSocket pour le chat en temps réel"""
    await manager.connect(websocket, session_id, user_id)
    
    try:
        while True:
            # Recevoir le message
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            user_message = message_data.get("message", "")
            audio_data = message_data.get("audio_data")
            audio_format = message_data.get("audio_format", "webm")
            
            if not user_message.strip() and not audio_data:
                continue
            
            # Envoyer une indication de frappe
            await manager.send_message(session_id, {
                "type": "typing",
                "message": "L'assistant réfléchit...",
                "timestamp": datetime.utcnow().isoformat()
            })
            
            # Traiter l'audio si présent
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
            
            # Préparer la réponse
            response_data = {
                "type": "response",
                "message": result["response"],
                "intent": result.get("intent", "unknown"),
                "escalate": result.get("escalate", False),
                "agents_used": result.get("agents_used", []),
                "processing_time": result.get("processing_time", 0.0),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Ajouter les objets complémentaires
            if result.get("products"):
                response_data["products"] = result["products"][:5]
            if result.get("recommendations"):
                response_data["recommendations"] = result["recommendations"][:5]
            if result.get("cart"):
                response_data["cart"] = result["cart"]
            
            # Envoyer la réponse
            await manager.send_message(session_id, response_data)
            
    except WebSocketDisconnect:
        await manager.disconnect(session_id)
    except Exception as e:
        logger.error(f"Erreur WebSocket: {e}")
        await manager.send_message(session_id, {
            "type": "error",
            "message": "Une erreur s'est produite. Veuillez réessayer.",
            "timestamp": datetime.utcnow().isoformat()
        })

# Routes utilitaires
@app.get("/health")
async def health_check():
    """Vérification de l'état de santé de l'API"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@app.get("/stats")
async def get_stats():
    """Statistiques des connexions actives"""
    return {
        "active_connections": len(manager.active_connections),
        "connections": list(manager.active_connections.keys())
    }

# Interface web simple
@app.get("/", response_class=HTMLResponse)
async def get_chat_interface():
    """Interface web simple pour tester le chatbot"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>E-Commerce Chatbot</title>
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .chat-container { max-width: 800px; margin: 0 auto; background: white; border-radius: 10px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .chat-messages { height: 400px; overflow-y: auto; border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; background: #fafafa; }
            .message { margin-bottom: 10px; padding: 8px; border-radius: 5px; }
            .user-message { background: #007bff; color: white; text-align: right; }
            .bot-message { background: #e9ecef; color: #333; }
            .typing { color: #666; font-style: italic; }
            .input-area { display: flex; gap: 10px; }
            .message-input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
            .send-button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
            .send-button:hover { background: #0056b3; }
            .products-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; margin-top: 10px; }
            .product-card { border: 1px solid #ddd; padding: 10px; border-radius: 5px; background: white; }
            .product-price { font-weight: bold; color: #007bff; }
            .cart-summary { border: 1px dashed #999; padding: 10px; background: #fff; margin-top: 10px; }
            .cart-item { display: flex; justify-content: space-between; padding: 4px 0; border-bottom: 1px solid #eee; }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <h1>🛒 Assistant Shopping E-Commerce</h1>
            <div id="chatMessages" class="chat-messages"></div>
            <div class="input-area">
                <input type="text" id="messageInput" class="message-input" placeholder="Tapez votre message..." onkeypress="handleKeyPress(event)">
                <button onclick="sendMessage()" class="send-button">Envoyer</button>
            </div>
        </div>

        <script>
            const sessionId = 'web-' + Math.random().toString(36).substr(2, 9);
            const ws = new WebSocket(`ws://localhost:8000/ws/${sessionId}`);
            const chatMessages = document.getElementById('chatMessages');
            const messageInput = document.getElementById('messageInput');

            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                addMessage(data);
            };

            function addMessage(data) {
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message bot-message';
                
                if (data.type === 'typing') {
                    messageDiv.className += ' typing';
                    messageDiv.innerHTML = data.message;
                    messageDiv.id = 'typing-indicator';
                } else if (data.type === 'response') {
                    // Supprimer l'indicateur de frappe
                    const typingIndicator = document.getElementById('typing-indicator');
                    if (typingIndicator) {
                        typingIndicator.remove();
                    }
                    
                    let content = `<strong>🤖 Assistant:</strong> ${data.message}`;
                    
                    // Ajouter les produits si disponibles
                    if (data.products && data.products.length > 0) {
                        content += '<div class="products-grid">';
                        data.products.forEach(product => {
                            content += `
                                <div class="product-card">
                                    <h4>${product.name}</h4>
                                    <p class="product-price">${product.price || ''}${product.price ? '€' : ''}</p>
                                    <p>${product.description ? product.description.substring(0, 100) + '...' : ''}</p>
                                </div>
                            `;
                        });
                        content += '</div>';
                    }

                    // Ajouter le panier si disponible
                    if (data.cart) {
                        content += renderCart(data.cart);
                    }
                    
                    messageDiv.innerHTML = content;
                }
                
                chatMessages.appendChild(messageDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }

            function renderCart(cart) {
                try {
                    const items = cart.items || [];
                    const totalItems = cart.total_items || 0;
                    const totalPrice = cart.total_price || 0;
                    let html = '<div class="cart-summary">';
                    html += `<div><strong>🧺 Panier:</strong> ${totalItems} article(s) — Total: ${totalPrice}€</div>`;
                    if (items.length) {
                        items.slice(0,5).forEach(it => {
                            html += `<div class="cart-item"><span>${it.name} x${it.quantity}</span><span>${it.total}€</span></div>`;
                        });
                        if (items.length > 5) {
                            html += `<div class="cart-item"><em>... et ${items.length - 5} autre(s)</em></div>`;
                        }
                    } else {
                        html += '<div class="cart-item"><em>Le panier est vide.</em></div>';
                    }
                    html += '</div>';
                    return html;
                } catch (e) {
                    return '';
                }
            }

            function addUserMessage(message) {
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message user-message';
                messageDiv.innerHTML = `<strong>Vous:</strong> ${message}`;
                chatMessages.appendChild(messageDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }

            function sendMessage() {
                const message = messageInput.value.trim();
                if (message) {
                    addUserMessage(message);
                    ws.send(JSON.stringify({ message: message }));
                    messageInput.value = '';
                }
            }

            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            }

            // Focus sur l'input au chargement
            messageInput.focus();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# Middleware de gestion d'erreurs
@app.middleware("http")
async def error_handling_middleware(request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Erreur non gérée: {e}")
        return {"error": "Erreur interne du serveur"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("SMA.core.main:app", host="0.0.0.0", port=8000, reload=True)
import uuid
from typing import Dict, List, Optional
import json
from datetime import datetime, timedelta

class ChatSession:
    def __init__(self, session_id: str, user_id: str, db_manager: DatabaseManager):
        self.session_id = session_id
        self.user_id = user_id
        self.db_manager = db_manager
        self.messages: List[AgentMessage] = []
        self.context = UserContext(
            user_id=user_id,
            session_id=session_id,
            conversation_history=[],
            current_intent=None,
            sentiment_score=0.0,
            escalated=False
        )
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
    
    def add_message(self, message: AgentMessage):
        """Ajoute un message à la session"""
        self.messages.append(message)
        self.context.conversation_history.append(message)
        self.last_activity = datetime.now()
        
        # Sauvegarder dans la base de données
        self._save_to_db()
        
        # Mise en cache Redis
        self._cache_session()
    
    def _save_to_db(self):
        """Sauvegarde la session dans PostgreSQL"""
        with self.db_manager.get_session() as session:
            conversation = session.query(Conversation).filter_by(session_id=self.session_id).first()
            
            if not conversation:
                conversation = Conversation(
                    id=str(uuid.uuid4()),
                    session_id=self.session_id,
                    user_id=self.user_id,
                    messages=[],
                    intent=self.context.current_intent,
                    sentiment_score=self.context.sentiment_score,
                    escalated=self.context.escalated
                )
                session.add(conversation)
            
            # Convertir les messages en format sérialisable
            messages_data = [
                {
                    "type": msg.type,
                    "content": msg.content,
                    "sender": msg.sender,
                    "timestamp": msg.timestamp.isoformat(),
                    "metadata": msg.metadata
                }
                for msg in self.messages
            ]
            
            conversation.messages = messages_data
            conversation.intent = self.context.current_intent
            conversation.sentiment_score = self.context.sentiment_score
            conversation.escalated = self.context.escalated
            conversation.updated_at = datetime.now()
            
            session.commit()
    
    def _cache_session(self):
        """Met en cache la session dans Redis"""
        session_data = {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "messages": [
                {
                    "type": msg.type,
                    "content": msg.content,
                    "sender": msg.sender,
                    "timestamp": msg.timestamp.isoformat(),
                    "metadata": msg.metadata
                }
                for msg in self.messages[-10:]  # Garder les 10 derniers messages
            ],
            "context": {
                "current_intent": self.context.current_intent,
                "sentiment_score": self.context.sentiment_score,
                "escalated": self.context.escalated
            },
            "last_activity": self.last_activity.isoformat()
        }
        
        # Expiration après 1 heure d'inactivité
        self.db_manager.redis_client.setex(
            f"session:{self.session_id}",
            timedelta(hours=1),
            json.dumps(session_data)
        )
    
    def is_expired(self, timeout_minutes: int = 30) -> bool:
        """Vérifie si la session a expiré"""
        return (datetime.now() - self.last_activity).total_seconds() > (timeout_minutes * 60)

class SessionManager:
    def __init__(self, db_manager: DatabaseManager, config: Any):
        self.db_manager = db_manager
        self.config = config
        self.active_sessions: Dict[str, ChatSession] = {}
    
    def create_session(self, user_id: str) -> ChatSession:
        """Crée une nouvelle session de chat"""
        session_id = str(uuid.uuid4())
        session = ChatSession(session_id, user_id, self.db_manager)
        self.active_sessions[session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Récupère une session existante"""
        # Vérifier en mémoire
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            if not session.is_expired(self.config.session_timeout_minutes):
                return session
            else:
                # Supprimer la session expirée
                del self.active_sessions[session_id]
        
        # Vérifier dans Redis
        cached_data = self.db_manager.redis_client.get(f"session:{session_id}")
        if cached_data:
            return self._restore_session_from_cache(session_id, json.loads(cached_data))
        
        return None
    
    def _restore_session_from_cache(self, session_id: str, data: Dict) -> ChatSession:
        """Restaure une session depuis le cache Redis"""
        session = ChatSession(session_id, data["user_id"], self.db_manager)
        
        # Restaurer les messages
        for msg_data in data["messages"]:
            message = AgentMessage(
                type=MessageType(msg_data["type"]),
                content=msg_data["content"],
                sender=msg_data["sender"],
                timestamp=datetime.fromisoformat(msg_data["timestamp"]),
                metadata=msg_data.get("metadata")
            )
            session.messages.append(message)
            session.context.conversation_history.append(message)
        
        # Restaurer le contexte
        context_data = data["context"]
        session.context.current_intent = context_data["current_intent"]
        session.context.sentiment_score = context_data["sentiment_score"]
        session.context.escalated = context_data["escalated"]
        
        session.last_activity = datetime.fromisoformat(data["last_activity"])
        
        # Remettre en mémoire
        self.active_sessions[session_id] = session
        
        return session
    
    def cleanup_expired_sessions(self):
        """Nettoie les sessions expirées"""
        expired_sessions = [
            session_id for session_id, session in self.active_sessions.items()
            if session.is_expired(self.config.session_timeout_minutes)
        ]
        
        for session_id in expired_sessions:
            del self.active_sessions[session_id]
            # Supprimer aussi du cache Redis
            self.db_manager.redis_client.delete(f"session:{session_id}")


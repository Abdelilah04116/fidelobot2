"""
Modèles de contexte pour maintenir l'état des conversations et utilisateurs
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from .message_models import AgentMessage

class UserContext(BaseModel):
    """Contexte utilisateur"""
    user_id: str
    session_id: str
    conversation_history: List[AgentMessage] = []
    current_intent: Optional[str] = None
    sentiment_score: float = 0.0
    escalated: bool = False
    user_profile: Optional[Dict[str, Any]] = None
    preferences: Optional[Dict[str, Any]] = None
    last_activity: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class SessionContext(BaseModel):
    """Contexte de session"""
    session_id: str
    user_id: str
    start_time: datetime = Field(default_factory=datetime.now)
    last_activity: datetime = Field(default_factory=datetime.now)
    message_count: int = 0
    current_state: str = "active"
    metadata: Dict[str, Any] = {}
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ConversationContext(BaseModel):
    """Contexte de conversation"""
    conversation_id: str
    session_id: str
    user_id: str
    messages: List[AgentMessage] = []
    current_topic: Optional[str] = None
    conversation_flow: List[str] = []
    intent_history: List[str] = []
    sentiment_history: List[float] = []
    entities_extracted: List[str] = []
    requires_follow_up: bool = False
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ProductContext(BaseModel):
    """Contexte produit"""
    product_id: Optional[str] = None
    category: Optional[str] = None
    search_query: Optional[str] = None
    filters: Dict[str, Any] = {}
    recommendations: List[str] = []
    viewed_products: List[str] = []
    cart_items: List[Dict[str, Any]] = []
    purchase_history: List[str] = [] 
"""
Modèles de messages pour la communication inter-agents
"""

from enum import Enum
from typing import Dict, Any, Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

class MessageType(str, Enum):
    """Types de messages dans le système"""
    USER_MESSAGE = "user_message"
    AGENT_MESSAGE = "agent_message"
    SYSTEM_MESSAGE = "system_message"
    ERROR_MESSAGE = "error_message"
    ESCALATION_MESSAGE = "escalation_message"
    MONITORING_MESSAGE = "monitoring_message"
    GDPR_MESSAGE = "gdpr_message"

class MessagePriority(str, Enum):
    """Priorités des messages"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

class MessageMetadata(BaseModel):
    """Métadonnées des messages"""
    intent: Optional[str] = None
    confidence: Optional[float] = None
    sentiment_score: Optional[float] = None
    entities: Optional[List[str]] = None
    context: Optional[Dict[str, Any]] = None
    processing_time: Optional[float] = None
    agent_chain: Optional[List[str]] = None
    gdpr_compliant: bool = True
    requires_human: bool = False

class AgentMessage(BaseModel):
    """Message échangé entre agents"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: MessageType
    content: str
    sender: str
    recipient: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    priority: MessagePriority = MessagePriority.NORMAL
    metadata: Optional[MessageMetadata] = None
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# Import uuid pour l'ID génération
import uuid 
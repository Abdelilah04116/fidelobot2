"""
Modèles pour les agents et leurs capacités
"""

from enum import Enum
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

class AgentType(str, Enum):
    """Types d'agents dans le système"""
    ORCHESTRATOR = "orchestrator"
    CONVERSATION = "conversation"
    RECOMMENDATION = "recommendation"
    PRODUCT_SEARCH = "product_search"
    ORDER_MANAGEMENT = "order_management"
    CUSTOMER_SERVICE = "customer_service"
    GDPR = "gdpr"
    MONITORING = "monitoring"
    ESCALATION = "escalation"
    PROFILING = "profiling"
    SUMMARIZER = "summarizer"

class AgentState(str, Enum):
    """États possibles d'un agent"""
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"

class AgentCapability(str, Enum):
    """Capacités des agents"""
    NATURAL_LANGUAGE_PROCESSING = "nlp"
    SENTIMENT_ANALYSIS = "sentiment"
    INTENT_RECOGNITION = "intent"
    ENTITY_EXTRACTION = "entities"
    PRODUCT_SEARCH = "product_search"
    RECOMMENDATION = "recommendation"
    ORDER_PROCESSING = "order_processing"
    CUSTOMER_SUPPORT = "customer_support"
    GDPR_COMPLIANCE = "gdpr"
    MONITORING = "monitoring"
    ESCALATION = "escalation"
    PROFILING = "profiling"
    SUMMARIZATION = "summarization"

class AgentResponse(BaseModel):
    """Réponse d'un agent"""
    success: bool
    content: str
    metadata: Optional[Dict[str, Any]] = None
    next_agent: Optional[str] = None
    requires_human: bool = False
    confidence: float = 0.0
    processing_time: float = 0.0
    error_message: Optional[str] = None

class AgentConfig(BaseModel):
    """Configuration d'un agent"""
    agent_id: str
    agent_type: AgentType
    capabilities: List[AgentCapability]
    max_concurrent_tasks: int = 10
    timeout_seconds: int = 30
    retry_attempts: int = 3
    priority: int = 1
    enabled: bool = True
    config: Dict[str, Any] = {} 
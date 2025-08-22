"""
Agent orchestrateur - coordonne tous les autres agents
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

from .base_agent import BaseAgent
from models.message_models import AgentMessage, MessageType, MessageMetadata, MessagePriority
from models.agent_models import AgentType, AgentCapability, AgentResponse
from models.context_models import UserContext

logger = logging.getLogger(__name__)

class OrchestratorAgent(BaseAgent):
    """Agent orchestrateur qui coordonne tous les autres agents"""
    
    def __init__(self, config: Dict[str, Any], db_manager):
        super().__init__("orchestrator", AgentType.ORCHESTRATOR, config)
        self.db_manager = db_manager
        self.agents: Dict[str, BaseAgent] = {}
        self.agent_routing_rules = self._initialize_routing_rules()
        self.capabilities = [
            AgentCapability.NATURAL_LANGUAGE_PROCESSING,
            AgentCapability.INTENT_RECOGNITION,
            AgentCapability.SENTIMENT_ANALYSIS
        ]
    
    def _initialize_routing_rules(self) -> Dict[str, List[str]]:
        """Initialise les règles de routage des messages"""
        return {
            "product_search": ["product_search", "recommendation"],
            "order_management": ["order_management", "customer_service"],
            "customer_support": ["customer_service", "escalation"],
            "recommendation": ["recommendation", "product_search"],
            "gdpr_request": ["gdpr"],
            "general_inquiry": ["conversation", "customer_service"],
            "complaint": ["customer_service", "escalation"],
            "purchase_intent": ["product_search", "recommendation", "order_management"]
        }
    
    def register_agent(self, agent_type: AgentType, agent: BaseAgent):
        """Enregistre un agent dans l'orchestrateur"""
        agent.set_db_manager(self.db_manager)
        self.agents[agent_type.value] = agent
        logger.info(f"Registered agent: {agent_type.value}")
    
    def can_handle(self, message: AgentMessage) -> bool:
        """L'orchestrateur peut gérer tous les types de messages"""
        return True
    
    async def process(self, message: AgentMessage, context: UserContext) -> AgentResponse:
        """Traite un message en orchestrant les agents appropriés"""
        start_time = datetime.now()
        
        try:
            # 1. Analyser l'intention du message
            intent = await self._analyze_intent(message.content, context)
            
            # 2. Déterminer la chaîne d'agents à utiliser
            agent_chain = self._determine_agent_chain(intent, message, context)
            
            # 3. Exécuter la chaîne d'agents
            final_response = await self._execute_agent_chain(agent_chain, message, context)
            
            # 4. Mettre à jour le contexte
            context.current_intent = intent
            context.last_activity = datetime.now()
            
            # 5. Envoyer au monitoring
            await self._send_to_monitoring(message, final_response, context)
            
            return final_response
            
        except Exception as e:
            logger.error(f"Error in orchestrator: {str(e)}")
            return AgentResponse(
                success=False,
                content="Je rencontre des difficultés techniques. Pouvez-vous reformuler votre demande ?",
                error_message=str(e)
            )
    
    async def _analyze_intent(self, content: str, context: UserContext) -> str:
        """Analyse l'intention du message utilisateur"""
        # Utiliser l'agent de conversation pour l'analyse d'intention
        if "conversation" in self.agents:
            conversation_agent = self.agents["conversation"]
            intent_message = AgentMessage(
                type=MessageType.AGENT_MESSAGE,
                content=content,
                sender="orchestrator",
                recipient="conversation",
                metadata=MessageMetadata(
                    intent="intent_analysis",
                    context={"user_context": context.dict()}
                )
            )
            
            response = await conversation_agent.handle_message(intent_message, context)
            if response.success and response.metadata:
                return response.metadata.get("detected_intent", "general_inquiry")
        
        # Fallback: analyse simple basée sur des mots-clés
        content_lower = content.lower()
        if any(word in content_lower for word in ["produit", "acheter", "commander", "prix"]):
            return "purchase_intent"
        elif any(word in content_lower for word in ["commande", "livraison", "suivi"]):
            return "order_management"
        elif any(word in content_lower for word in ["problème", "aide", "support"]):
            return "customer_support"
        elif any(word in content_lower for word in ["recommandation", "suggestion"]):
            return "recommendation"
        else:
            return "general_inquiry"
    
    def _determine_agent_chain(self, intent: str, message: AgentMessage, context: UserContext) -> List[str]:
        """Détermine la chaîne d'agents à utiliser"""
        # Règles de routage de base
        if intent in self.agent_routing_rules:
            return self.agent_routing_rules[intent]
        
        # Règles spéciales basées sur le contexte
        if context.escalated:
            return ["escalation"]
        
        if message.priority == MessagePriority.URGENT:
            return ["customer_service", "escalation"]
        
        # Par défaut
        return ["conversation", "customer_service"]
    
    async def _execute_agent_chain(self, agent_chain: List[str], message: AgentMessage, context: UserContext) -> AgentResponse:
        """Exécute la chaîne d'agents"""
        current_message = message
        final_response = None
        
        for agent_name in agent_chain:
            if agent_name not in self.agents:
                logger.warning(f"Agent {agent_name} not found, skipping")
                continue
            
            agent = self.agents[agent_name]
            
            # Vérifier si l'agent est disponible
            if not agent.health_check():
                logger.warning(f"Agent {agent_name} is not healthy, skipping")
                continue
            
            # Traiter avec l'agent
            response = await agent.handle_message(current_message, context)
            
            if not response.success:
                logger.error(f"Agent {agent_name} failed: {response.error_message}")
                # Continuer avec l'agent suivant ou retourner une erreur
                if agent_name == agent_chain[-1]:  # Dernier agent
                    return response
                continue
            
            # Mettre à jour le message pour l'agent suivant
            current_message = AgentMessage(
                type=MessageType.AGENT_MESSAGE,
                content=response.content,
                sender=agent_name,
                recipient=agent_chain[agent_chain.index(agent_name) + 1] if agent_chain.index(agent_name) + 1 < len(agent_chain) else None,
                metadata=response.metadata
            )
            
            final_response = response
            
            # Vérifier si une escalade est nécessaire
            if response.requires_human:
                logger.info(f"Escalation required by agent {agent_name}")
                break
        
        return final_response or AgentResponse(
            success=False,
            content="Je n'ai pas pu traiter votre demande. Veuillez réessayer.",
            error_message="No agents could process the request"
        )
    
    async def _send_to_monitoring(self, original_message: AgentMessage, response: AgentResponse, context: UserContext):
        """Envoie les données au monitoring"""
        if "monitoring" in self.agents:
            monitoring_message = AgentMessage(
                type=MessageType.MONITORING_MESSAGE,
                content="Conversation processed",
                sender="orchestrator",
                recipient="monitoring",
                metadata={
                    "original_message": original_message.dict(),
                    "response": response.dict(),
                    "context": context.dict(),
                    "processing_time": response.processing_time
                }
            )
            
            try:
                await self.agents["monitoring"].handle_message(monitoring_message, context)
            except Exception as e:
                logger.error(f"Failed to send to monitoring: {e}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Retourne le statut du système"""
        agent_status = {}
        for agent_name, agent in self.agents.items():
            agent_status[agent_name] = {
                "state": agent.state.value,
                "health": agent.health_check(),
                "metrics": agent.get_metrics()
            }
        
        return {
            "orchestrator_state": self.state.value,
            "total_agents": len(self.agents),
            "agent_status": agent_status,
            "system_health": all(agent.health_check() for agent in self.agents.values())
        } 

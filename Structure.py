# Système Multi-Agent pour Chatbot E-commerce
# Structure principale avec LangGraph

from typing import TypedDict, List, Optional, Dict, Any
from enum import Enum
from datetime import datetime
import asyncio
import json
import uuid
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================================================
# TYPES ET ÉNUMÉRATIONS
# =============================================================================

class UserStatus(Enum):
    VISITOR = "visitor"
    LOGGED_IN = "logged_in"
    VIP = "vip"

class Intent(Enum):
    GREETING = "greeting"
    PRODUCT_SEARCH = "product_search"
    CATEGORY_BROWSE = "category_browse"
    RECOMMENDATIONS = "recommendations"
    CART_MANAGEMENT = "cart_management"
    ORDER_STATUS = "order_status"
    COMPLAINT = "complaint"
    GDPR_REQUEST = "gdpr_request"
    ESCALATION = "escalation"
    GOODBYE = "goodbye"

class ConversationState(TypedDict):
    user_id: Optional[str]
    session_id: str
    user_status: UserStatus
    messages: List[Dict[str, Any]]
    user_profile: Dict[str, Any]
    current_intent: str
    products_context: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    sentiment_score: float
    escalation_needed: bool
    gdpr_compliant: bool
    conversation_summary: str
    last_agent: str
    agent_responses: Dict[str, Any]
    timestamp: str

# =============================================================================
# CLASSES DE BASE
# =============================================================================

@dataclass
class AgentResponse:
    agent_name: str
    success: bool
    data: Dict[str, Any]
    message: str
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"{__name__}.{name}")
    
    @abstractmethod
    async def execute(self, state: ConversationState) -> AgentResponse:
        pass
    
    def log_execution(self, state: ConversationState, response: AgentResponse):
        self.logger.info(f"Agent {self.name} executed for session {state['session_id']}")

# =============================================================================
# AGENTS SPÉCIALISÉS
# =============================================================================

class ConversationAgent(BaseAgent):
    def __init__(self):
        super().__init__("ConversationAgent")
        self.intent_patterns = {
            Intent.GREETING: ["bonjour", "salut", "hello", "bonsoir"],
            Intent.PRODUCT_SEARCH: ["cherche", "recherche", "produit", "trouve"],
            Intent.CATEGORY_BROWSE: ["catégorie", "section", "rayon"],
            Intent.RECOMMENDATIONS: ["recommande", "suggère", "conseil"],
            Intent.CART_MANAGEMENT: ["panier", "ajouter", "retirer"],
            Intent.ORDER_STATUS: ["commande", "statut", "livraison"],
            Intent.COMPLAINT: ["problème", "réclamation", "insatisfait"],
            Intent.GDPR_REQUEST: ["données", "suppression", "accès", "rgpd"],
            Intent.ESCALATION: ["humain", "conseiller", "service client"],
            Intent.GOODBYE: ["au revoir", "bye", "merci", "fin"]
        }
    
    async def execute(self, state: ConversationState) -> AgentResponse:
        try:
            # Analyse du dernier message
            last_message = state["messages"][-1]["content"] if state["messages"] else ""
            
            # Détection d'intention
            intent = self._detect_intent(last_message)
            
            # Mise à jour du state
            updated_state = {
                "current_intent": intent.value,
                "last_agent": self.name,
                "timestamp": datetime.now().isoformat()
            }
            
            response = AgentResponse(
                agent_name=self.name,
                success=True,
                data=updated_state,
                message=f"Intent détecté: {intent.value}"
            )
            
            self.log_execution(state, response)
            return response
            
        except Exception as e:
            return AgentResponse(
                agent_name=self.name,
                success=False,
                data={},
                message=f"Erreur dans ConversationAgent: {str(e)}"
            )
    
    def _detect_intent(self, message: str) -> Intent:
        message_lower = message.lower()
        
        for intent, patterns in self.intent_patterns.items():
            if any(pattern in message_lower for pattern in patterns):
                return intent
        
        return Intent.PRODUCT_SEARCH  # Intention par défaut

class CustomerProfilingAgent(BaseAgent):
    def __init__(self):
        super().__init__("CustomerProfilingAgent")
        self.user_profiles = {}  # Simulation d'une base de données
    
    async def execute(self, state: ConversationState) -> AgentResponse:
        try:
            user_id = state.get("user_id")
            session_id = state["session_id"]
            
            # Récupération ou création du profil
            if user_id and user_id in self.user_profiles:
                profile = self.user_profiles[user_id]
                user_status = UserStatus.LOGGED_IN
            else:
                profile = self._create_anonymous_profile(session_id)
                user_status = UserStatus.VISITOR
            
            # Mise à jour basée sur l'activité courante
            profile = self._update_profile(profile, state)
            
            # Segmentation client
            if user_id:
                user_status = self._segment_user(profile)
                self.user_profiles[user_id] = profile
            
            response_data = {
                "user_profile": profile,
                "user_status": user_status.value,
                "segmentation_score": profile.get("engagement_score", 0)
            }
            
            response = AgentResponse(
                agent_name=self.name,
                success=True,
                data=response_data,
                message="Résumé de conversation généré"
            )
            
            self.log_execution(state, response)
            return response
            
        except Exception as e:
            return AgentResponse(
                agent_name=self.name,
                success=False,
                data={},
                message=f"Erreur dans SummarizerAgent: {str(e)}"
            )
    
    def _generate_conversation_summary(self, state: ConversationState) -> str:
        messages = state.get("messages", [])
        intent = state.get("current_intent", "unknown")
        sentiment = state.get("sentiment_score", 0.5)
        
        summary = f"Conversation de {len(messages)} messages avec intent '{intent}'. "
        summary += f"Sentiment global: {sentiment:.2f}. "
        
        if state.get("escalation_needed"):
            summary += "Escalade vers conseiller humain requise."
        else:
            summary += "Résolution automatique."
        
        return summary
    
    def _extract_key_points(self, state: ConversationState) -> List[str]:
        key_points = []
        
        # Points basés sur l'intent
        intent = state.get("current_intent")
        if intent:
            key_points.append(f"Intent principal: {intent}")
        
        # Points basés sur les produits
        products = state.get("products_context", [])
        if products:
            key_points.append(f"Produits consultés: {len(products)}")
        
        # Points basés sur les recommandations
        recommendations = state.get("recommendations", [])
        if recommendations:
            key_points.append(f"Recommandations fournies: {len(recommendations)}")
        
        return key_points
    
    def _generate_follow_up_recommendations(self, state: ConversationState) -> List[str]:
        recommendations = []
        
        sentiment = state.get("sentiment_score", 0.5)
        if sentiment < 0.4:
            recommendations.append("Suivre satisfaction client")
        
        if state.get("escalation_needed"):
            recommendations.append("Assurer suivi par conseiller")
        
        user_status = state.get("user_status")
        if user_status == UserStatus.VISITOR.value:
            recommendations.append("Encourager création de compte")
        
        return recommendations
    
    def _calculate_quality_score(self, state: ConversationState) -> float:
        score = 0.5  # Score de base
        
        # Bonus pour résolution sans escalade
        if not state.get("escalation_needed", False):
            score += 0.2
        
        # Bonus pour sentiment positif
        sentiment = state.get("sentiment_score", 0.5)
        if sentiment > 0.6:
            score += 0.2
        
        # Malus pour conversation trop longue
        if len(state.get("messages", [])) > 20:
            score -= 0.1
        
        return max(0, min(1, score))

# =============================================================================
# ORCHESTRATEUR PRINCIPAL - LANGGRAPH
# =============================================================================

class EcommerceMultiAgentSystem:
    def __init__(self):
        self.agents = {
            "conversation": ConversationAgent(),
            "profiling": CustomerProfilingAgent(),
            "catalog": ProductCatalogAgent(),
            "recommendations": RecommendationAgent(),
            "sentiment": SentimentAnalysisAgent(),
            "escalation": EscalationAgent(),
            "security": SecurityGDPRAgent(),
            "pricing": PricingPromotionAgent(),
            "logging": LoggingMonitoringAgent(),
            "summarizer": SummarizerAgent()
        }
        
        self.workflow = self._create_workflow()
        self.memory = MemorySaver()
    
    def _create_workflow(self) -> StateGraph:
        """Création du workflow LangGraph"""
        workflow = StateGraph(ConversationState)
        
        # Ajout des nœuds
        workflow.add_node("conversation_agent", self._conversation_node)
        workflow.add_node("profiling_agent", self._profiling_node)
        workflow.add_node("sentiment_agent", self._sentiment_node)
        workflow.add_node("security_agent", self._security_node)
        workflow.add_node("catalog_agent", self._catalog_node)
        workflow.add_node("recommendations_agent", self._recommendations_node)
        workflow.add_node("pricing_agent", self._pricing_node)
        workflow.add_node("escalation_agent", self._escalation_node)
        workflow.add_node("logging_agent", self._logging_node)
        workflow.add_node("summarizer_agent", self._summarizer_node)
        workflow.add_node("response_formatter", self._response_formatter)
        
        # Définition du flux
        workflow.set_entry_point("conversation_agent")
        
        # Flux principal
        workflow.add_edge("conversation_agent", "profiling_agent")
        workflow.add_edge("profiling_agent", "sentiment_agent")
        workflow.add_edge("sentiment_agent", "security_agent")
        
        # Routage conditionnel après sécurité
        workflow.add_conditional_edges(
            "security_agent",
            self._route_after_security,
            {
                "catalog": "catalog_agent",
                "recommendations": "recommendations_agent",
                "escalation": "escalation_agent",
                "direct_response": "response_formatter"
            }
        )
        
        # Flux après catalogue
        workflow.add_edge("catalog_agent", "recommendations_agent")
        workflow.add_edge("recommendations_agent", "pricing_agent")
        workflow.add_edge("pricing_agent", "escalation_agent")
        
        # Flux final
        workflow.add_edge("escalation_agent", "logging_agent")
        workflow.add_edge("logging_agent", "summarizer_agent")
        workflow.add_edge("summarizer_agent", "response_formatter")
        workflow.add_edge("response_formatter", END)
        
        return workflow.compile(checkpointer=self.memory)
    
    async def _conversation_node(self, state: ConversationState) -> ConversationState:
        """Nœud de conversation"""
        response = await self.agents["conversation"].execute(state)
        return self._update_state(state, response)
    
    async def _profiling_node(self, state: ConversationState) -> ConversationState:
        """Nœud de profilage"""
        response = await self.agents["profiling"].execute(state)
        return self._update_state(state, response)
    
    async def _sentiment_node(self, state: ConversationState) -> ConversationState:
        """Nœud d'analyse de sentiment"""
        response = await self.agents["sentiment"].execute(state)
        return self._update_state(state, response)
    
    async def _security_node(self, state: ConversationState) -> ConversationState:
        """Nœud de sécurité GDPR"""
        response = await self.agents["security"].execute(state)
        return self._update_state(state, response)
    
    async def _catalog_node(self, state: ConversationState) -> ConversationState:
        """Nœud de catalogue"""
        response = await self.agents["catalog"].execute(state)
        return self._update_state(state, response)
    
    async def _recommendations_node(self, state: ConversationState) -> ConversationState:
        """Nœud de recommandations"""
        response = await self.agents["recommendations"].execute(state)
        return self._update_state(state, response)
    
    async def _pricing_node(self, state: ConversationState) -> ConversationState:
        """Nœud de pricing"""
        response = await self.agents["pricing"].execute(state)
        return self._update_state(state, response)
    
    async def _escalation_node(self, state: ConversationState) -> ConversationState:
        """Nœud d'escalade"""
        response = await self.agents["escalation"].execute(state)
        return self._update_state(state, response)
    
    async def _logging_node(self, state: ConversationState) -> ConversationState:
        """Nœud de logging"""
        response = await self.agents["logging"].execute(state)
        return self._update_state(state, response)
    
    async def _summarizer_node(self, state: ConversationState) -> ConversationState:
        """Nœud de résumé"""
        response = await self.agents["summarizer"].execute(state)
        return self._update_state(state, response)
    
    async def _response_formatter(self, state: ConversationState) -> ConversationState:
        """Formatage de la réponse finale"""
        formatted_response = self._format_final_response(state)
        
        # Ajout de la réponse formatée aux messages
        state["messages"].append({
            "role": "assistant",
            "content": formatted_response,
            "timestamp": datetime.now().isoformat()
        })
        
        return state
    
    def _route_after_security(self, state: ConversationState) -> str:
        """Routage après vérification sécurité"""
        intent = state.get("current_intent")
        
        if intent in [Intent.PRODUCT_SEARCH.value, Intent.CATEGORY_BROWSE.value]:
            return "catalog"
        elif intent == Intent.RECOMMENDATIONS.value:
            return "recommendations"
        elif intent in [Intent.COMPLAINT.value, Intent.ESCALATION.value]:
            return "escalation"
        elif state.get("sentiment_score", 0.5) < 0.3:
            return "escalation"
        else:
            return "catalog"  # Par défaut
    
    def _update_state(self, state: ConversationState, response: AgentResponse) -> ConversationState:
        """Mise à jour de l'état avec la réponse de l'agent"""
        if response.success:
            # Mise à jour des données spécifiques
            for key, value in response.data.items():
                if key in state or key.startswith("agent_"):
                    state[key] = value
            
            # Mise à jour des réponses d'agents
            if "agent_responses" not in state:
                state["agent_responses"] = {}
            
            state["agent_responses"][response.agent_name] = {
                "success": response.success,
                "data": response.data,
                "message": response.message,
                "timestamp": response.timestamp
            }
        
        return state
    
    def _format_final_response(self, state: ConversationState) -> str:
        """Formatage de la réponse finale à l'utilisateur"""
        intent = state.get("current_intent")
        
        if state.get("escalation_needed"):
            return self._format_escalation_response(state)
        
        if intent == Intent.PRODUCT_SEARCH.value:
            return self._format_product_search_response(state)
        elif intent == Intent.RECOMMENDATIONS.value:
            return self._format_recommendations_response(state)
        elif intent == Intent.GREETING.value:
            return self._format_greeting_response(state)
        elif intent == Intent.GDPR_REQUEST.value:
            return self._format_gdpr_response(state)
        else:
            return self._format_default_response(state)
    
    def _format_escalation_response(self, state: ConversationState) -> str:
        """Formatage pour escalade"""
        return ("Je comprends que vous avez besoin d'aide supplémentaire. "
                "Je vais vous mettre en relation avec un de nos conseillers "
                "qui pourra mieux vous assister. Veuillez patienter un moment.")
    
    def _format_product_search_response(self, state: ConversationState) -> str:
        """Formatage pour recherche produits"""
        products = state.get("products_context", [])
        
        if not products:
            return "Je n'ai pas trouvé de produits correspondant à votre recherche. Pouvez-vous préciser ce que vous cherchez ?"
        
        response = f"J'ai trouvé {len(products)} produits qui pourraient vous intéresser :\n\n"
        
        for i, product in enumerate(products[:3], 1):
            response += f"{i}. {product['name']} - {product['price']}€\n"
            response += f"   {product['description']}\n"
            if not product['in_stock']:
                response += "   ⚠️ Actuellement en rupture de stock\n"
            response += "\n"
        
        if len(products) > 3:
            response += f"... et {len(products) - 3} autres produits."
        
        return response
    
    def _format_recommendations_response(self, state: ConversationState) -> str:
        """Formatage pour recommandations"""
        recommendations = state.get("recommendations", [])
        
        if not recommendations:
            return "Je vais analyser vos préférences pour vous proposer des produits adaptés. Pouvez-vous me dire quel type de produits vous intéresse ?"
        
        response = "Voici mes recommandations personnalisées pour vous :\n\n"
        
        for i, rec in enumerate(recommendations[:3], 1):
            response += f"{i}. {rec['name']} - {rec['price']}€\n"
            response += f"   {rec['reason']}\n\n"
        
        return response
    
    def _format_greeting_response(self, state: ConversationState) -> str:
        """Formatage pour salutations"""
        user_status = state.get("user_status", UserStatus.VISITOR.value)
        
        if user_status == UserStatus.VIP.value:
            return ("Bonjour et bienvenue ! En tant que client VIP, "
                    "je suis là pour vous offrir le meilleur service. "
                    "Comment puis-je vous aider aujourd'hui ?")
        elif user_status == UserStatus.LOGGED_IN.value:
            return ("Bonjour ! Content de vous revoir. "
                    "Comment puis-je vous aider aujourd'hui ?")
        else:
            return ("Bonjour ! Bienvenue sur notre site. "
                    "Je suis votre assistant virtuel. "
                    "Comment puis-je vous aider ?")
    
    def _format_gdpr_response(self, state: ConversationState) -> str:
        """Formatage pour requêtes GDPR"""
        return ("Je comprends votre demande concernant vos données personnelles. "
                "Pour traiter votre demande dans le respect du RGPD, "
                "je vais vous mettre en relation avec notre équipe "
                "de protection des données.")
    
    def _format_default_response(self, state: ConversationState) -> str:
        """Formatage par défaut"""
        return ("Je suis là pour vous aider ! "
                "Vous pouvez me demander de rechercher des produits, "
                "obtenir des recommandations, ou toute autre question.")
    
    async def process_message(self, user_message: str, session_id: str, 
                            user_id: Optional[str] = None) -> Dict[str, Any]:
        """Traitement d'un message utilisateur"""
        
        # Création de l'état initial
        initial_state = ConversationState(
            user_id=user_id,
            session_id=session_id,
            user_status=UserStatus.VISITOR,
            messages=[{
                "role": "user",
                "content": user_message,
                "timestamp": datetime.now().isoformat()
            }],
            user_profile={},
            current_intent="",
            products_context=[],
            recommendations=[],
            sentiment_score=0.5,
            escalation_needed=False,
            gdpr_compliant=True,
            conversation_summary="",
            last_agent="",
            agent_responses={},
            timestamp=datetime.now().isoformat()
        )
        
        # Configuration du thread
        config = {"configurable": {"thread_id": session_id}}
        
        try:
            # Exécution du workflow
            final_state = await self.workflow.ainvoke(initial_state, config)
            
            # Extraction de la réponse
            assistant_message = final_state["messages"][-1]["content"]
            
            return {
                "response": assistant_message,
                "session_id": session_id,
                "intent": final_state.get("current_intent"),
                "sentiment_score": final_state.get("sentiment_score"),
                "escalation_needed": final_state.get("escalation_needed", False),
                "user_status": final_state.get("user_status"),
                "products_found": len(final_state.get("products_context", [])),
                "recommendations_count": len(final_state.get("recommendations", [])),
                "conversation_summary": final_state.get("conversation_summary"),
                "timestamp": final_state.get("timestamp")
            }
        
        except Exception as e:
            logger.error(f"Erreur lors du traitement du message: {str(e)}")
            return {
                "response": "Je rencontre un problème technique. Veuillez réessayer dans quelques instants.",
                "session_id": session_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

# =============================================================================
# INTERFACE DE CHAT (EXEMPLE D'UTILISATION)
# =============================================================================

class ChatInterface:
    def __init__(self):
        self.system = EcommerceMultiAgentSystem()
        self.active_sessions = {}
    
    async def handle_message(self, user_message: str, session_id: str = None, 
                           user_id: str = None) -> Dict[str, Any]:
        """Interface principale pour traiter les messages"""
        
        if session_id is None:
            session_id = str(uuid.uuid4())
        
        # Traitement du message
        result = await self.system.process_message(user_message, session_id, user_id)
        
        # Stockage de la session
        self.active_sessions[session_id] = {
            "last_interaction": datetime.now().isoformat(),
            "user_id": user_id,
            "message_count": self.active_sessions.get(session_id, {}).get("message_count", 0) + 1
        }
        
        return result
    
    def get_session_info(self, session_id: str) -> Dict[str, Any]:
        """Récupération d'informations sur une session"""
        return self.active_sessions.get(session_id, {})
    
    def cleanup_old_sessions(self, max_age_hours: int = 24):
        """Nettoyage des sessions anciennes"""
        current_time = datetime.now()
        sessions_to_remove = []
        
        for session_id, info in self.active_sessions.items():
            last_interaction = datetime.fromisoformat(info["last_interaction"])
            age_hours = (current_time - last_interaction).total_seconds() / 3600
            
            if age_hours > max_age_hours:
                sessions_to_remove.append(session_id)
        
        for session_id in sessions_to_remove:
            del self.active_sessions[session_id]
        
        return len(sessions_to_remove)

# =============================================================================
# EXEMPLE D'UTILISATION ET TESTS
# =============================================================================

async def main():
    """Exemple d'utilisation du système"""
    
    # Initialisation du système
    chat_interface = ChatInterface()
    
    # Simulation de conversations
    test_conversations = [
        {
            "user_id": "user123",
            "messages": [
                "Bonjour",
                "Je cherche un smartphone",
                "Avez-vous des recommandations ?",
                "Merci, au revoir"
            ]
        },
        {
            "user_id": None,  # Utilisateur anonyme
            "messages": [
                "Salut",
                "Je veux voir vos promotions",
                "C'est nul vos prix !",
                "Je veux parler à un humain"
            ]
        }
    ]
    
    print("=== DÉMARRAGE DU SYSTÈME MULTI-AGENT E-COMMERCE ===\n")
    
    for i, conversation in enumerate(test_conversations, 1):
        print(f"--- Conversation {i} ---")
        session_id = str(uuid.uuid4())
        
        for message in conversation["messages"]:
            print(f"👤 Utilisateur: {message}")
            
            # Traitement du message
            result = await chat_interface.handle_message(
                user_message=message,
                session_id=session_id,
                user_id=conversation["user_id"]
            )
            
            print(f"🤖 Assistant: {result['response']}")
            print(f"   📊 Intent: {result.get('intent', 'N/A')}")
            print(f"   😊 Sentiment: {result.get('sentiment_score', 0):.2f}")
            print(f"   🚨 Escalade: {'Oui' if result.get('escalation_needed') else 'Non'}")
            print()
        
        print(f"Session {session_id} terminée.\n")
    
    print("=== DÉMONSTRATION TERMINÉE ===")

if __name__ == "__main__":
    # Lancement du système
    asyncio.run(main())

class CustomerProfilingAgent(BaseAgent):
    def __init__(self):
        super().__init__("CustomerProfilingAgent")
        self.user_profiles = {}  # Simulation d'une base de données
    
    async def execute(self, state: ConversationState) -> AgentResponse:
        try:
            user_id = state.get("user_id")
            session_id = state["session_id"]
            
            # Récupération ou création du profil
            profile = (self.user_profiles.get(user_id) if user_id 
                      else self._create_anonymous_profile(session_id))
            
            # Mise à jour du profil
            updated_profile = self._update_profile(profile, state)
            
            # Détermination du statut utilisateur
            user_status = self._segment_user(updated_profile)
            
            # Sauvegarde du profil mis à jour si utilisateur connecté
            if user_id:
                self.user_profiles[user_id] = updated_profile
            
            response_data = {
                "user_profile": updated_profile,
                "user_status": user_status.value,
                "profile_completeness": self._calculate_profile_completeness(updated_profile)
            }
            
            response = AgentResponse(
                agent_name=self.name,
                success=True,
                data=response_data,
                message="Profil utilisateur mis à jour"
            )
            
            self.log_execution(state, response)
            return response
            
        except Exception as e:
            return AgentResponse(
                agent_name=self.name,
                success=False,
                data={},
                message=f"Erreur dans CustomerProfilingAgent: {str(e)}"
            )
    def _create_anonymous_profile(self, session_id: str) -> Dict[str, Any]:
        return {
            "session_id": session_id,
            "preferences": {},
            "behavior": {
                "page_views": 0,
                "time_spent": 0,
                "interactions": 0
            },
            "engagement_score": 0,
            "created_at": datetime.now().isoformat()
        }
    
    def _update_profile(self, profile: Dict[str, Any], state: ConversationState) -> Dict[str, Any]:
        # Simulation de mise à jour basée sur l'activité
        profile["behavior"]["interactions"] += 1
        profile["last_interaction"] = datetime.now().isoformat()
        
        # Mise à jour du score d'engagement
        profile["engagement_score"] = min(100, profile["engagement_score"] + 5)
        
        return profile
    
    def _segment_user(self, profile: Dict[str, Any]) -> UserStatus:
        engagement_score = profile.get("engagement_score", 0)
        
        if engagement_score > 80:
            return UserStatus.VIP
        elif engagement_score > 30:
            return UserStatus.LOGGED_IN
        else:
            return UserStatus.VISITOR

class ProductCatalogAgent(BaseAgent):
    def __init__(self):
        super().__init__("ProductCatalogAgent")
        self.products = self._load_sample_products()
    
    async def execute(self, state: ConversationState) -> AgentResponse:
        try:
            intent = state.get("current_intent")
            last_message = state["messages"][-1]["content"] if state["messages"] else ""
            
            if intent == Intent.PRODUCT_SEARCH.value:
                products = self._search_products(last_message)
            elif intent == Intent.CATEGORY_BROWSE.value:
                products = self._browse_category(last_message)
            else:
                products = self._get_featured_products()
            
            response_data = {
                "products": products[:10],  # Limiter à 10 résultats
                "total_found": len(products),
                "search_query": last_message
            }
            
            response = AgentResponse(
                agent_name=self.name,
                success=True,
                data=response_data,
                message=f"Trouvé {len(products)} produits"
            )
            
            self.log_execution(state, response)
            return response
            
        except Exception as e:
            return AgentResponse(
                agent_name=self.name,
                success=False,
                data={},
                message=f"Erreur dans ProductCatalogAgent: {str(e)}"
            )
    
    def _load_sample_products(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "1",
                "name": "Smartphone Premium",
                "category": "Electronics",
                "price": 699.99,
                "description": "Dernier smartphone avec écran OLED",
                "in_stock": True,
                "rating": 4.5,
                "tags": ["smartphone", "mobile", "electronics"]
            },
            {
                "id": "2", 
                "name": "Casque Audio Bluetooth",
                "category": "Electronics",
                "price": 149.99,
                "description": "Casque sans fil haute qualité",
                "in_stock": True,
                "rating": 4.3,
                "tags": ["audio", "bluetooth", "casque"]
            },
            {
                "id": "3",
                "name": "Chaussures de Running",
                "category": "Sports",
                "price": 89.99,
                "description": "Chaussures légères pour la course",
                "in_stock": False,
                "rating": 4.7,
                "tags": ["chaussures", "running", "sport"]
            }
        ]
    
    def _search_products(self, query: str) -> List[Dict[str, Any]]:
        query_lower = query.lower()
        results = []
        
        for product in self.products:
            # Recherche dans nom, description et tags
            if (query_lower in product["name"].lower() or 
                query_lower in product["description"].lower() or
                any(query_lower in tag for tag in product["tags"])):
                results.append(product)
        
        return results
    
    def _browse_category(self, query: str) -> List[Dict[str, Any]]:
        # Extraction de catégorie approximative
        categories = {
            "electronics": ["Electronics"],
            "sport": ["Sports"],
            "mode": ["Fashion"]
        }
        
        query_lower = query.lower()
        target_categories = []
        
        for key, cats in categories.items():
            if key in query_lower:
                target_categories.extend(cats)
        
        if not target_categories:
            return self.products
        
        return [p for p in self.products if p["category"] in target_categories]
    
    def _get_featured_products(self) -> List[Dict[str, Any]]:
        # Retourne les produits les mieux notés
        return sorted(self.products, key=lambda x: x["rating"], reverse=True)

class RecommendationAgent(BaseAgent):
    def __init__(self):
        super().__init__("RecommendationAgent")
    
    async def execute(self, state: ConversationState) -> AgentResponse:
        try:
            user_profile = state.get("user_profile", {})
            products_context = state.get("products_context", [])
            
            # Génération de recommandations basées sur le profil et le contexte
            recommendations = self._generate_recommendations(user_profile, products_context)
            
            response_data = {
                "recommendations": recommendations,
                "recommendation_type": "personalized" if user_profile else "popular",
                "confidence_score": self._calculate_confidence(user_profile)
            }
            
            response = AgentResponse(
                agent_name=self.name,
                success=True,
                data=response_data,
                message=f"Généré {len(recommendations)} recommandations"
            )
            
            self.log_execution(state, response)
            return response
            
        except Exception as e:
            return AgentResponse(
                agent_name=self.name,
                success=False,
                data={},
                message=f"Erreur dans RecommendationAgent: {str(e)}"
            )
    
    def _generate_recommendations(self, user_profile: Dict[str, Any], 
                                products_context: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Simulation d'algorithme de recommandation
        recommendations = [
            {
                "product_id": "rec_1",
                "name": "Produit Recommandé 1",
                "reason": "Basé sur vos achats précédents",
                "confidence": 0.85,
                "price": 29.99
            },
            {
                "product_id": "rec_2", 
                "name": "Produit Recommandé 2",
                "reason": "Populaire dans votre catégorie",
                "confidence": 0.72,
                "price": 45.50
            }
        ]
        
        return recommendations
    
    def _calculate_confidence(self, user_profile: Dict[str, Any]) -> float:
        # Calcul de confiance basé sur la richesse du profil
        if not user_profile:
            return 0.3
        
        engagement_score = user_profile.get("engagement_score", 0)
        return min(1.0, engagement_score / 100.0)

class SentimentAnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__("SentimentAnalysisAgent")
        self.negative_words = ["problème", "insatisfait", "décevant", "nul", "horrible"]
        self.positive_words = ["excellent", "parfait", "génial", "content", "satisfait"]
    
    async def execute(self, state: ConversationState) -> AgentResponse:
        try:
            messages = state.get("messages", [])
            
            if not messages:
                sentiment_score = 0.5
            else:
                last_message = messages[-1]["content"]
                sentiment_score = self._analyze_sentiment(last_message)
            
            # Analyse de l'historique pour tendance
            trend = self._analyze_trend(messages)
            
            response_data = {
                "sentiment_score": sentiment_score,
                "sentiment_label": self._get_sentiment_label(sentiment_score),
                "trend": trend,
                "requires_attention": sentiment_score < 0.3
            }
            
            response = AgentResponse(
                agent_name=self.name,
                success=True,
                data=response_data,
                message=f"Sentiment analysé: {response_data['sentiment_label']}"
            )
            
            self.log_execution(state, response)
            return response
            
        except Exception as e:
            return AgentResponse(
                agent_name=self.name,
                success=False,
                data={},
                message=f"Erreur dans SentimentAnalysisAgent: {str(e)}"
            )
    
    def _analyze_sentiment(self, text: str) -> float:
        text_lower = text.lower()
        
        positive_count = sum(1 for word in self.positive_words if word in text_lower)
        negative_count = sum(1 for word in self.negative_words if word in text_lower)
        
        if positive_count + negative_count == 0:
            return 0.5  # Neutre
        
        return positive_count / (positive_count + negative_count)
    
    def _analyze_trend(self, messages: List[Dict[str, Any]]) -> str:
        if len(messages) < 2:
            return "stable"
        
        # Analyse des 3 derniers messages
        recent_messages = messages[-3:]
        scores = [self._analyze_sentiment(msg["content"]) for msg in recent_messages]
        
        if len(scores) >= 2:
            if scores[-1] > scores[-2]:
                return "improving"
            elif scores[-1] < scores[-2]:
                return "declining"
        
        return "stable"
    
    def _get_sentiment_label(self, score: float) -> str:
        if score > 0.7:
            return "positive"
        elif score < 0.3:
            return "negative"
        else:
            return "neutral"

class EscalationAgent(BaseAgent):
    def __init__(self):
        super().__init__("EscalationAgent")
        self.escalation_triggers = [
            "conseiller humain",
            "service client",
            "manager",
            "remboursement",
            "réclamation"
        ]
    
    async def execute(self, state: ConversationState) -> AgentResponse:
        try:
            should_escalate = self._should_escalate(state)
            
            if should_escalate:
                ticket = self._create_escalation_ticket(state)
                
                response_data = {
                    "escalation_needed": True,
                    "ticket": ticket,
                    "priority": self._determine_priority(state),
                    "summary": self._generate_summary(state)
                }
                
                message = "Escalade vers conseiller humain requise"
            else:
                response_data = {
                    "escalation_needed": False,
                    "continue_bot": True
                }
                message = "Conversation peut continuer avec le bot"
            
            response = AgentResponse(
                agent_name=self.name,
                success=True,
                data=response_data,
                message=message
            )
            
            self.log_execution(state, response)
            return response
            
        except Exception as e:
            return AgentResponse(
                agent_name=self.name,
                success=False,
                data={},
                message=f"Erreur dans EscalationAgent: {str(e)}"
            )
    
    def _should_escalate(self, state: ConversationState) -> bool:
        # Vérification des triggers explicites
        messages = state.get("messages", [])
        if messages:
            last_message = messages[-1]["content"].lower()
            if any(trigger in last_message for trigger in self.escalation_triggers):
                return True
        
        # Vérification du sentiment
        sentiment_score = state.get("sentiment_score", 0.5)
        if sentiment_score < 0.3:
            return True
        
        # Vérification de la longueur de conversation
        if len(messages) > 20:  # Conversation trop longue
            return True
        
        return False
    
    def _create_escalation_ticket(self, state: ConversationState) -> Dict[str, Any]:
        return {
            "ticket_id": str(uuid.uuid4()),
            "session_id": state["session_id"],
            "user_id": state.get("user_id"),
            "created_at": datetime.now().isoformat(),
            "status": "open",
            "messages_count": len(state.get("messages", []))
        }
    
    def _determine_priority(self, state: ConversationState) -> str:
        user_status = state.get("user_status", UserStatus.VISITOR.value)
        sentiment_score = state.get("sentiment_score", 0.5)
        
        if user_status == UserStatus.VIP.value:
            return "high"
        elif sentiment_score < 0.2:
            return "high"
        elif sentiment_score < 0.4:
            return "medium"
        else:
            return "low"
    
    def _generate_summary(self, state: ConversationState) -> str:
        messages = state.get("messages", [])
        intent = state.get("current_intent", "unknown")
        
        return f"Conversation avec {len(messages)} messages. Intent: {intent}. Sentiment: {state.get('sentiment_score', 0.5):.2f}"

class SecurityGDPRAgent(BaseAgent):
    def __init__(self):
        super().__init__("SecurityGDPRAgent")
        self.gdpr_requests = ["accès", "rectification", "suppression", "portabilité"]
    
    async def execute(self, state: ConversationState) -> AgentResponse:
        try:
            # Vérification de conformité GDPR
            gdpr_compliant = self._check_gdpr_compliance(state)
            
            # Détection de requêtes GDPR
            gdpr_request = self._detect_gdpr_request(state)
            
            # Anonymisation si nécessaire
            anonymized_data = self._anonymize_if_needed(state)
            
            response_data = {
                "gdpr_compliant": gdpr_compliant,
                "gdpr_request_detected": gdpr_request is not None,
                "gdpr_request_type": gdpr_request,
                "anonymization_applied": anonymized_data is not None,
                "consent_required": self._check_consent_required(state)
            }
            
            response = AgentResponse(
                agent_name=self.name,
                success=True,
                data=response_data,
                message="Vérification GDPR terminée"
            )
            
            self.log_execution(state, response)
            return response
            
        except Exception as e:
            return AgentResponse(
                agent_name=self.name,
                success=False,
                data={},
                message=f"Erreur dans SecurityGDPRAgent: {str(e)}"
            )
    
    def _check_gdpr_compliance(self, state: ConversationState) -> bool:
        # Vérification basique de conformité
        user_id = state.get("user_id")
        
        if user_id:
            # Utilisateur connecté - vérifier les consentements
            return True  # Simulation - en réalité, vérifier en base
        else:
            # Utilisateur anonyme - OK par défaut
            return True
    
    def _detect_gdpr_request(self, state: ConversationState) -> Optional[str]:
        messages = state.get("messages", [])
        
        if not messages:
            return None
        
        last_message = messages[-1]["content"].lower()
        
        for request_type in self.gdpr_requests:
            if request_type in last_message:
                return request_type
        
        return None
    
    def _anonymize_if_needed(self, state: ConversationState) -> Optional[Dict[str, Any]]:
        # Simulation d'anonymisation
        return None
    
    def _check_consent_required(self, state: ConversationState) -> bool:
        # Vérification si consentement requis pour traitement
        user_status = state.get("user_status", UserStatus.VISITOR.value)
        return user_status == UserStatus.VISITOR.value

class PricingPromotionAgent(BaseAgent):
    def __init__(self):
        super().__init__("PricingPromotionAgent")
        self.promotions = [
            {
                "id": "promo_1",
                "name": "Réduction fidélité",
                "discount": 0.10,
                "condition": "logged_in"
            },
            {
                "id": "promo_2",
                "name": "Réduction VIP",
                "discount": 0.15,
                "condition": "vip"
            }
        ]
    
    async def execute(self, state: ConversationState) -> AgentResponse:
        try:
            user_status = state.get("user_status", UserStatus.VISITOR.value)
            products_context = state.get("products_context", [])
            
            # Calcul des prix personnalisés
            personalized_prices = self._calculate_personalized_prices(products_context, user_status)
            
            # Détection des promotions applicables
            applicable_promotions = self._find_applicable_promotions(user_status)
            
            response_data = {
                "personalized_prices": personalized_prices,
                "applicable_promotions": applicable_promotions,
                "dynamic_pricing_applied": len(personalized_prices) > 0
            }
            
            response = AgentResponse(
                agent_name=self.name,
                success=True,
                data=response_data,
                message=f"Calculé {len(personalized_prices)} prix personnalisés"
            )
            
            self.log_execution(state, response)
            return response
            
        except Exception as e:
            return AgentResponse(
                agent_name=self.name,
                success=False,
                data={},
                message=f"Erreur dans PricingPromotionAgent: {str(e)}"
            )
    
    def _calculate_personalized_prices(self, products: List[Dict[str, Any]], 
                                     user_status: str) -> List[Dict[str, Any]]:
        personalized = []
        
        for product in products:
            original_price = product.get("price", 0)
            discount = 0
            
            if user_status == UserStatus.VIP.value:
                discount = 0.15
            elif user_status == UserStatus.LOGGED_IN.value:
                discount = 0.10
            
            if discount > 0:
                new_price = original_price * (1 - discount)
                personalized.append({
                    "product_id": product.get("id"),
                    "original_price": original_price,
                    "personalized_price": new_price,
                    "discount": discount
                })
        
        return personalized
    
    def _find_applicable_promotions(self, user_status: str) -> List[Dict[str, Any]]:
        applicable = []
        
        for promo in self.promotions:
            if promo["condition"] == "logged_in" and user_status != UserStatus.VISITOR.value:
                applicable.append(promo)
            elif promo["condition"] == "vip" and user_status == UserStatus.VIP.value:
                applicable.append(promo)
        
        return applicable

class LoggingMonitoringAgent(BaseAgent):
    def __init__(self):
        super().__init__("LoggingMonitoringAgent")
        self.logs = []
        self.metrics = {
            "total_conversations": 0,
            "successful_interactions": 0,
            "escalations": 0,
            "avg_response_time": 0
        }
    
    async def execute(self, state: ConversationState) -> AgentResponse:
        try:
            # Création du log d'interaction
            log_entry = self._create_log_entry(state)
            self.logs.append(log_entry)
            
            # Mise à jour des métriques
            self._update_metrics(state)
            
            # Détection d'anomalies
            anomalies = self._detect_anomalies(state)
            
            response_data = {
                "log_entry": log_entry,
                "current_metrics": self.metrics.copy(),
                "anomalies_detected": anomalies,
                "system_health": "healthy" if not anomalies else "warning"
            }
            
            response = AgentResponse(
                agent_name=self.name,
                success=True,
                data=response_data,
                message="Logging et monitoring terminés"
            )
            
            self.log_execution(state, response)
            return response
            
        except Exception as e:
            return AgentResponse(
                agent_name=self.name,
                success=False,
                data={},
                message=f"Erreur dans LoggingMonitoringAgent: {str(e)}"
            )
    
    def _create_log_entry(self, state: ConversationState) -> Dict[str, Any]:
        return {
            "timestamp": datetime.now().isoformat(),
            "session_id": state["session_id"],
            "user_id": state.get("user_id"),
            "intent": state.get("current_intent"),
            "sentiment_score": state.get("sentiment_score"),
            "escalation_needed": state.get("escalation_needed", False),
            "agents_involved": [state.get("last_agent")],
            "message_count": len(state.get("messages", []))
        }
    
    def _update_metrics(self, state: ConversationState):
        self.metrics["total_conversations"] += 1
        
        if not state.get("escalation_needed", False):
            self.metrics["successful_interactions"] += 1
        else:
            self.metrics["escalations"] += 1
    
    def _detect_anomalies(self, state: ConversationState) -> List[str]:
        anomalies = []
        
        # Détection de sentiment très négatif
        if state.get("sentiment_score", 0.5) < 0.2:
            anomalies.append("very_negative_sentiment")
        
        # Détection de conversation trop longue
        if len(state.get("messages", [])) > 30:
            anomalies.append("conversation_too_long")
        
        return anomalies

class SummarizerAgent(BaseAgent):
    def __init__(self):
        super().__init__("SummarizerAgent")
        self.summary_templates = {
            Intent.PRODUCT_SEARCH.value: "Recherche de produits: {details}",
            Intent.RECOMMENDATIONS.value: "Recommandations fournies: {details}",
            Intent.COMPLAINT.value: "Gestion de réclamation: {details}",
            Intent.GDPR_REQUEST.value: "Demande RGPD: {details}"
        }
    
    async def execute(self, state: ConversationState) -> AgentResponse:
        try:
            # Génération du résumé de conversation
            summary = self._generate_conversation_summary(state)
            
            # Extraction des points clés
            key_points = self._extract_key_points(state)
            
            # Recommandations de suivi
            follow_up_recommendations = self._generate_follow_up_recommendations(state)
            
            # Calcul du score de qualité
            quality_score = self._calculate_quality_score(state)
            
            response_data = {
                "conversation_summary": summary,
                "key_points": key_points,
                "follow_up_recommendations": follow_up_recommendations,
                "conversation_quality_score": quality_score,
                "sentiment_trend": self._analyze_sentiment_trend(state),
                "interaction_metrics": self._get_interaction_metrics(state)
            }
            
            response = AgentResponse(
                agent_name=self.name,
                success=True,
                data=response_data,
                message=f"Résumé généré avec score qualité: {quality_score:.2f}"
            )
            
            self.log_execution(state, response)
            return response
            
        except Exception as e:
            return AgentResponse(
                agent_name=self.name,
                success=False,
                data={},
                message=f"Erreur dans SummarizerAgent: {str(e)}"
            )

    def _generate_conversation_summary(self, state: ConversationState) -> str:
        messages = state.get("messages", [])
        intent = state.get("current_intent", "unknown")
        
        # Création du résumé basé sur l'intent
        template = self.summary_templates.get(intent, "Conversation générale: {details}")
        details = self._get_conversation_details(state)
        
        summary = template.format(details=details)
        if state.get("escalation_needed"):
            summary += " (Escaladé vers service client)"
            
        return summary

    def _get_conversation_details(self, state: ConversationState) -> str:
        """Extrait les détails pertinents de la conversation."""
        details = []
        
        if products := state.get("products_context"):
            details.append(f"{len(products)} produits consultés")
            
        if recommendations := state.get("recommendations"):
            details.append(f"{len(recommendations)} recommandations")
            
        sentiment = state.get("sentiment_score", 0.5)
        details.append(f"sentiment {sentiment:.2f}")
        
        return ", ".join(details)

    def _extract_key_points(self, state: ConversationState) -> List[str]:
        points = []
        
        # Points basés sur l'intent et le contexte
        if intent := state.get("current_intent"):
            points.append(f"Intent principal: {intent}")
        
        if products := state.get("products_context"):
            points.append(f"Produits consultés: {len(products)}")
        
        # Points basés sur le sentiment et l'escalade
        sentiment = state.get("sentiment_score", 0.5)
        if sentiment < 0.3:
            points.append("⚠️ Sentiment négatif détecté")
        
        if state.get("escalation_needed"):
            points.append("🔔 Escalade requise")
            
        return points

    def _generate_follow_up_recommendations(self, state: ConversationState) -> List[str]:
        recommendations = []
        user_status = state.get("user_status")
        sentiment = state.get("sentiment_score", 0.5)
        
        # Recommandations basées sur le statut utilisateur
        if user_status == UserStatus.VISITOR.value:
            recommendations.append("Proposer création de compte")
            
        elif user_status == UserStatus.LOGGED_IN.value:
            recommendations.append("Suggérer programme fidélité")
            
        # Recommandations basées sur le sentiment
        if sentiment < 0.4:
            recommendations.append("Planifier suivi satisfaction")
            
        return recommendations

    def _calculate_quality_score(self, state: ConversationState) -> float:
        score = 0.5  # Score de base
        
        # Bonus pour résolution sans escalade
        if not state.get("escalation_needed", False):
            score += 0.2
            
        # Bonus pour sentiment positif
        sentiment = state.get("sentiment_score", 0.5)
        if sentiment > 0.6:
            score += 0.2
            
        # Malus pour conversation trop longue
        if len(state.get("messages", [])) > 20:
            score -= 0.1
            
        return round(max(0, min(1, score)), 2)

    def _analyze_sentiment_trend(self, state: ConversationState) -> str:
        """Analyse la tendance du sentiment sur la conversation."""
        messages = state.get("messages", [])
        if len(messages) < 2:
            return "stable"
        
        sentiment_scores = [msg.get("sentiment", 0.5) for msg in messages[-3:]]
        if sentiment_scores[-1] > sentiment_scores[0]:
            return "improving"
        elif sentiment_scores[-1] < sentiment_scores[0]:
            return "declining"
        return "stable"

    def _get_interaction_metrics(self, state: ConversationState) -> Dict[str, Any]:
        """Calcule les métriques d'interaction."""
        messages = state.get("messages", [])
        return {
            "total_messages": len(messages),
            "user_messages": sum(1 for m in messages if m.get("role") == "user"),
            "avg_response_time": self._calculate_avg_response_time(messages),
            "resolution_time": self._calculate_resolution_time(messages)
        }

    def _calculate_avg_response_time(self, messages: List[Dict[str, Any]]) -> float:
        """Calcule le temps de réponse moyen."""
        if len(messages) < 2:
            return 0.0
            
        response_times = []
        for i in range(1, len(messages)):
            if messages[i].get("role") == "assistant":
                time_diff = (datetime.fromisoformat(messages[i]["timestamp"]) -
                           datetime.fromisoformat(messages[i-1]["timestamp"]))
                response_times.append(time_diff.total_seconds())
                
        return round(sum(response_times) / len(response_times), 2) if response_times else 0.0

    def _calculate_resolution_time(self, messages: List[Dict[str, Any]]) -> float:
        """Calcule le temps total de résolution."""
        if len(messages) < 2:
            return 0.0
            
        start_time = datetime.fromisoformat(messages[0]["timestamp"])
        end_time = datetime.fromisoformat(messages[-1]["timestamp"])
        return round((end_time - start_time).total_seconds(), 2)
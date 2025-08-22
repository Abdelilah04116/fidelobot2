# orchestrator.py
from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledGraph
from typing import Dict, Any, List, TypedDict, Annotated
from typing_extensions import TypedDict
import operator
import asyncio

# Importation des agents
from SMA.agents.conversation_agent import ConversationAgent
from SMA.agents.product_search_agent import ProductSearchAgent
from SMA.agents.recommendation_agent import RecommendationAgent
from SMA.agents.customer_profiling_agent import CustomerProfilingAgent
from SMA.agents.summarizer_agent import SummarizerAgent
from SMA.agents.escalation_agent import EscalationAgent
from SMA.agents.order_management_agent import OrderManagementAgent
from SMA.agents.cart_management_agent import CartManagementAgent

class ChatState(TypedDict):
    """État partagé entre tous les agents"""
    # Données de base
    user_message: str
    session_id: str
    user_id: Annotated[int, operator.add]
    
    # Contexte de conversation
    conversation_history: Annotated[List[Dict], operator.add]
    intent: str
    confidence: float
    
    # Profil utilisateur
    user_profile: Dict[str, Any]
    is_authenticated: bool
    
    # Données de traitement
    agents_used: Annotated[List[str], operator.add]
    failed_attempts: int
    
    # Résultats des agents
    products: List[Dict]
    recommendations: List[Dict]
    order_info: Dict[str, Any]
    
    # Réponse finale
    response_text: str
    response_type: str
    escalate: bool
    
    # Métadonnées
    processing_time: float
    error_message: str

class ChatBotOrchestrator:
    def __init__(self):
        self.agents = {
            "conversation_agent": ConversationAgent(),
            "product_search_agent": ProductSearchAgent(),
            "recommendation_agent": RecommendationAgent(),
            "profiling_agent": CustomerProfilingAgent(),
            "summarizer_agent": SummarizerAgent(),
            "escalation_agent": EscalationAgent(),
            "order_management_agent": OrderManagementAgent(),
            "cart_management_agent": CartManagementAgent()
        }
        
        self.graph = self._build_graph()
    
    def _build_graph(self) -> CompiledGraph:
        """Construire le graphe de workflow LangGraph"""
        workflow = StateGraph(ChatState)
        
        # Ajouter les nœuds (agents)
        workflow.add_node("conversation_agent", self._conversation_node)
        workflow.add_node("profiling_agent", self._profiling_node)
        workflow.add_node("product_search_agent", self._product_search_node)
        workflow.add_node("recommendation_agent", self._recommendation_node)
        workflow.add_node("order_management_agent", self._order_management_node)
        workflow.add_node("cart_management_agent", self._cart_management_node)
        workflow.add_node("summarizer_agent", self._summarizer_node)
        workflow.add_node("escalation_agent", self._escalation_node)
        workflow.add_node("final_response", self._final_response_node)
        
        # Définir les arêtes et conditions
        workflow.set_entry_point("conversation_agent")
        
        # Flux principal
        workflow.add_edge("conversation_agent", "profiling_agent")
        workflow.add_conditional_edges(
            "profiling_agent",
            self._route_after_profiling,
            {
                "product_search_agent": "product_search_agent",
                "recommendation_agent": "recommendation_agent", 
                "order_management_agent": "order_management_agent",
                "cart_management_agent": "cart_management_agent",
                "escalation_agent": "escalation_agent",
                "summarizer_agent": "summarizer_agent",
                "conversation_agent": "conversation_agent"  # Ajout explicite du fallback
            }
        )
        
        # Flux après recherche de produits
        workflow.add_conditional_edges(
            "product_search_agent",
            self._route_after_product_search,
            {
                "summarizer_agent": "summarizer_agent",
                "recommendation_agent": "recommendation_agent"
            }
        )
        
        # Flux après recommandations
        workflow.add_edge("recommendation_agent", "summarizer_agent")
        workflow.add_edge("order_management_agent", "summarizer_agent")
        workflow.add_edge("cart_management_agent", "summarizer_agent")
        
        # Flux de finalisation
        workflow.add_conditional_edges(
            "summarizer_agent",
            self._route_after_summary,
            {
                "escalation_agent": "escalation_agent",
                "final_response": "final_response"
            }
        )
        
        workflow.add_edge("escalation_agent", "final_response")
        workflow.add_edge("final_response", END)
        
        return workflow.compile()
    
    # Nœuds d'exécution des agents
    async def _conversation_node(self, state: ChatState) -> ChatState:
        """Nœud de l'agent de conversation"""
        result = await self.agents["conversation_agent"].execute(state)
        
        state.update({
            "intent": result.get("intent", "unknown"),
            "agents_used": state.get("agents_used", []) + ["conversation_agent"],
            "confidence": result.get("confidence", 0.5)
        })
        
        return state
    
    async def _profiling_node(self, state: ChatState) -> ChatState:
        """Nœud de l'agent de profilage"""
        if state.get("user_id"):
            result = await self.agents["profiling_agent"].execute(state)
            state["user_profile"] = result.get("profile", {})
        else:
            state["user_profile"] = {"segment": "anonymous"}
        
        state["agents_used"] = state.get("agents_used", []) + ["profiling_agent"]
        return state
    
    async def _product_search_node(self, state: ChatState) -> ChatState:
        """Nœud de l'agent de recherche de produits"""
        # Extraire les critères de recherche du message
        search_criteria = await self._extract_search_criteria(state["user_message"])
        
        search_state = {
            **state,
            "search_query": search_criteria.get("query", ""),
            "category": search_criteria.get("category", ""),
            "max_price": search_criteria.get("max_price")
        }
        
        result = await self.agents["product_search_agent"].execute(search_state)
        
        state.update({
            "products": result.get("products", []),
            "agents_used": state.get("agents_used", []) + ["product_search_agent"]
        })
        
        return state
    
    async def _recommendation_node(self, state: ChatState) -> ChatState:
        """Nœud de l'agent de recommandation"""
        rec_state = {
            **state,
            "recommendation_type": self._determine_recommendation_type(state["intent"])
        }
        
        result = await self.agents["recommendation_agent"].execute(rec_state)
        
        state.update({
            "recommendations": result.get("recommendations", []),
            "agents_used": state.get("agents_used", []) + ["recommendation_agent"]
        })
        
        return state
    
    async def _order_management_node(self, state: ChatState) -> ChatState:
        """Nœud de l'agent de gestion des commandes"""
        order_action = self._determine_order_action(state["intent"], state["user_message"])
        
        order_state = {
            **state,
            "action": order_action
        }
        
        result = await self.agents["order_management_agent"].execute(order_state)
        
        state.update({
            "order_info": result,
            "agents_used": state.get("agents_used", []) + ["order_management_agent"]
        })
        
        return state
    
    async def _cart_management_node(self, state: ChatState) -> ChatState:
        """Nœud de l'agent de gestion du panier"""
        cart_action = self._determine_cart_action(state.get("intent", ""), state.get("user_message", ""))
        product_id, quantity = self._extract_cart_params(state.get("user_message", ""))
        
        cart_state = {
            **state,
            "cart_action": cart_action,
            "product_id": product_id,
            "quantity": quantity
        }
        
        # Utiliser la méthode execute améliorée du CartManagementAgent
        result = await self.agents["cart_management_agent"].execute(cart_state)
        
        # Mettre à jour l'état avec le résultat
        if isinstance(result, dict):
            if result.get("response_text"):
                state["response_text"] = result["response_text"]
            if result.get("cart"):
                state["cart"] = result["cart"]
        
        state["agents_used"] = state.get("agents_used", []) + ["cart_management_agent"]
        return state
    
    async def _summarizer_node(self, state: ChatState) -> ChatState:
        """Nœud de l'agent de synthèse"""
        # Déterminer le type de contenu à résumer
        content_type = self._determine_content_type(state)
        
        # Préparer les données pour la synthèse
        raw_data = {
            "products": state.get("products", []),
            "recommendations": state.get("recommendations", []),
            "order_info": state.get("order_info", {}),
            "intent": state.get("intent", "")
        }
        
        summary_state = {
            **state,
            "content_type": content_type,
            "raw_data": raw_data
        }
        
        result = await self.agents["summarizer_agent"].execute(summary_state)
        
        # Récupérer la meilleure réponse possible sans l'écraser par une valeur vide
        summarized_text = (
            result.get("response_text")
            if isinstance(result, dict) and result.get("response_text")
            else (
                result.get("summary")
                if isinstance(result, dict) and result.get("summary")
                else state.get("response_text", "")
            )
        )
        
        state.update({
            "response_text": summarized_text,
            "response_type": content_type,
            "agents_used": state.get("agents_used", []) + ["summarizer_agent"]
        })
        
        return state
    
    async def _escalation_node(self, state: ChatState) -> ChatState:
        """Nœud de l'agent d'escalade"""
        result = await self.agents["escalation_agent"].execute(state)
        
        state.update({
            "escalate": result.get("escalate", False),
            "response_text": result.get("transition_message", state.get("response_text", "")),
            "agents_used": state.get("agents_used", []) + ["escalation_agent"]
        })
        
        return state
    
    async def _final_response_node(self, state: ChatState) -> ChatState:
        """Nœud de finalisation de la réponse"""
        # Ajouter des métadonnées finales
        state.update({
            "processing_complete": True,
            "agents_count": len(state.get("agents_used", [])),
            "final_intent": state.get("intent", "unknown")
        })
        
        # Log de la conversation
        await self._log_conversation(state)
        
        return state
    
    # Fonctions de routage conditionnel
    def _route_after_profiling(self, state: ChatState) -> str:
        """Router après le profilage utilisateur"""
        intent = state.get("intent", "")
        failed_attempts = state.get("failed_attempts", 0)
        
        # Vérifier si escalade nécessaire
        if failed_attempts >= 2:
            return "escalation_agent"
        
        # Router selon l'intention - utiliser les noms exacts des nœuds
        if intent in ["product_search", "product_info", "availability_check", "list_products"]:
            return "product_search_agent"
        elif intent in ["recommendation", "gift_suggestion", "bestsellers"]:
            return "recommendation_agent"
        elif intent in ["order_status", "track_delivery", "order_management"]:
            return "order_management_agent"
        elif intent in ["cart_management", "cart_view", "view_cart", "panier"]:
            return "cart_management_agent"
        elif intent in ["complaint", "refund_request", "escalation"]:
            return "escalation_agent"
        elif intent in ["greeting", "general_chat", "help"]:
            return "summarizer_agent"
        else:
            # Pour les intentions non reconnues, retourner vers conversation_agent (fallback personnalisé)
            return "conversation_agent"
    
    def _route_after_product_search(self, state: ChatState) -> str:
        """Router après la recherche de produits"""
        products = state.get("products", [])
        intent = state.get("intent", "")
        
        # Si pas de produits trouvés et intention de recommandation
        if not products and intent in ["gift_suggestion", "recommendation"]:
            return "recommendation_agent"
        else:
            return "summarizer_agent"
    
    def _route_after_summary(self, state: ChatState) -> str:
        """Router après la synthèse"""
        # Vérifier si on a une réponse satisfaisante
        response_text = state.get("response_text", "")
        confidence = state.get("confidence", 0.5)
        
        # N'escalader que si réponse vide ET confiance faible
        if (not response_text.strip()) and (confidence < 0.3):
            return "escalation_agent"
        else:
            return "final_response"
    
    # Fonctions utilitaires
    async def _extract_search_criteria(self, message: str) -> Dict[str, Any]:
        """Extraire les critères de recherche du message"""
        # Utiliser Gemini pour extraire les critères
        prompt = f"""
        Extrayez les critères de recherche de ce message:
        "{message}"
        
        Identifiez:
        - query: mots-clés de recherche
        - category: catégorie de produit (électronique, mode, maison, etc.)
        - max_price: prix maximum mentionné
        - brand: marque spécifique
        
        Répondez en JSON:
        {{
            "query": "mots-clés",
            "category": "catégorie",
            "max_price": null ou nombre,
            "brand": "marque"
        }}
        """
        
        response = await self.agents["conversation_agent"].generate_response(prompt)
        
        try:
            import json
            return json.loads(response)
        except:
            return {"query": message, "category": "", "max_price": None}
    
    def _determine_recommendation_type(self, intent: str) -> str:
        """Déterminer le type de recommandation"""
        rec_mapping = {
            "gift_suggestion": "gifts",
            "recommendation": "general",
            "product_search": "similar",
            "bestsellers": "bestsellers"
        }
        return rec_mapping.get(intent, "general")
    
    def _determine_order_action(self, intent: str, message: str) -> str:
        """Déterminer l'action pour la gestion des commandes"""
        if "statut" in message.lower() or "status" in message.lower():
            return "check_status"
        elif "suivi" in message.lower() or "track" in message.lower():
            return "track_delivery"
        elif "commandes" in message.lower() or "orders" in message.lower():
            return "list_orders"
        else:
            return "check_status"
    
    def _determine_cart_action(self, intent: str, message: str) -> str:
        """Déterminer l'action pour la gestion du panier"""
        message_lower = message.lower()
        if any(k in message_lower for k in ["vider le panier", "vider panier", "empty cart", "clear cart"]):
            return "clear"
        if any(k in message_lower for k in ["retirer", "supprimer du panier", "enlever du panier", "remove from cart", "supprimer"]):
            return "remove"
        if any(k in message_lower for k in ["modifier quantité", "changer quantité", "mettre", "quantité", "update quantity", "modifier"]):
            return "update"
        if any(k in message_lower for k in ["ajouter au panier", "ajouter", "add to cart", "mettre dans le panier"]):
            return "add"
        if any(k in message_lower for k in ["voir mon panier", "mon panier", "panier", "cart", "voir panier", "afficher panier"]):
            return "view"
        return "view"

    def _extract_cart_params(self, message: str) -> (int, int):
        """Extraire product_id et quantity à partir du message utilisateur."""
        import re
        message_lower = message.lower()
        product_id = None
        quantity = None
        
        # Chercher un id explicite: 'id 123', '#123', 'produit 123', 'article 123'
        id_patterns = [
            r"(?:id\s*|#\s*|produit\s*|article\s*)(\d+)",
            r"(\d+)(?:\s*$|\s+[xX]|\s+quantité|\s+fois)",
            r"produit\s+numéro\s+(\d+)",
            r"article\s+numéro\s+(\d+)"
        ]
        
        for pattern in id_patterns:
            id_match = re.search(pattern, message_lower)
            if id_match:
                try:
                    product_id = int(id_match.group(1))
                    break
                except Exception:
                    continue
        
        # Chercher quantité: 'x2', 'quantité 2', 'qty 2', 'fois 2', '2 fois'
        qty_patterns = [
            r"(?:x\s*|quantit[eé]\s*|qty\s*|fois\s*)(\d+)",
            r"(\d+)\s*(?:fois|unités?)",
            r"(\d+)\s*[xX]\s*\d+",  # Pour "2 x 3" (quantité = 2)
        ]
        
        for pattern in qty_patterns:
            qty_match = re.search(pattern, message_lower)
            if qty_match:
                try:
                    quantity = int(qty_match.group(1))
                    break
                except Exception:
                    continue
        
        # Défauts
        if quantity is None:
            quantity = 1
        
        return product_id, quantity
    
    def _determine_content_type(self, state: ChatState) -> str:
        """Déterminer le type de contenu à résumer"""
        if state.get("products"):
            return "product_summary"
        elif state.get("recommendations"):
            return "recommendations"
        elif state.get("order_info"):
            return "order_status"
        elif state.get("cart"):
            return "cart_summary"
        else:
            return "general"
    
    async def _log_conversation(self, state: ChatState):
        """Logger la conversation (bypass si DB indisponible)"""
        try:
            from SMA.models.database import SessionLocal, Message, Conversation
        except Exception:
            # Si les modèles ou la DB ne sont pas dispo, ne pas bloquer
            return
        
        db = SessionLocal()
        try:
            # Créer ou récupérer la conversation
            conversation = db.query(Conversation).filter(
                Conversation.session_id == state["session_id"]
            ).first()
            
            if not conversation:
                conversation = Conversation(
                    session_id=state["session_id"],
                    user_id=state.get("user_id")
                )
                db.add(conversation)
                db.flush()
            
            # Enregistrer le message utilisateur
            user_message = Message(
                conversation_id=conversation.id,
                sender_type="user",
                content=state["user_message"],
                intent=state.get("intent", ""),
                confidence=state.get("confidence", 0.0)
            )
            db.add(user_message)
            
            # Enregistrer la réponse du bot
            bot_message = Message(
                conversation_id=conversation.id,
                sender_type="bot",
                content=state.get("response_text", ""),
                intent=state.get("intent", ""),
                agent_used=",".join(state.get("agents_used", [])),
                metadata={
                    "agents_used": state.get("agents_used", []),
                    "escalated": state.get("escalate", False),
                    "processing_time": state.get("processing_time", 0)
                }
            )
            db.add(bot_message)
            
            db.commit()
            
        except Exception:
            # Ne pas bloquer le flux si la DB est indisponible
            try:
                db.rollback()
            except Exception:
                pass
        finally:
            try:
                db.close()
            except Exception:
                pass
    
    # Interface principale
    async def process_message(self, message: str, session_id: str, user_id: int = None) -> Dict[str, Any]:
        """Traiter un message utilisateur dynamiquement avec les agents"""
        import time
        import logging
        import traceback
        logger = logging.getLogger("chatbot.orchestrator")
        start_time = time.time()
        try:
            logger.info(f"[process_message] Début du traitement pour: {message}")
            
            # Initialiser l'état de la conversation
            state = {
                "user_message": message,
                "session_id": session_id,
                "user_id": (user_id if isinstance(user_id, int) and user_id is not None else 0),
                "conversation_history": [],
                "intent": "",
                "confidence": 0.0,
                "user_profile": {},
                "is_authenticated": user_id is not None,
                "agents_used": [],
                "failed_attempts": 0,
                "products": [],
                "recommendations": [],
                "order_info": {},
                "response_text": "",
                "response_type": "",
                "escalate": False,
                "processing_time": 0.0,
                "error_message": ""
            }
            logger.info(f"[process_message] État initialisé: {state}")
            
            # Vérifier que le graphe est disponible
            if not hasattr(self, 'graph') or self.graph is None:
                logger.error("[process_message] Le graphe LangGraph n'est pas initialisé")
                raise Exception("Graphe LangGraph non initialisé")
            
            logger.info(f"[process_message] Exécution du graphe LangGraph...")
            # Exécuter le workflow LangGraph (multi-agent)
            result_state = await self.graph.ainvoke(state)
            logger.info(f"[process_message] Résultat final: {result_state}")
            
            processing_time = time.time() - start_time
            return {
                "success": True,
                "response": result_state.get("response_text", "[Aucune réponse générée par les agents]"),
                "intent": result_state.get("intent", "unknown"),
                "escalate": result_state.get("escalate", False),
                "agents_used": result_state.get("agents_used", []),
                "processing_time": processing_time,
                "products": result_state.get("products", []),
                "recommendations": result_state.get("recommendations", [])
            }
        except Exception as e:
            logger.error(f"[process_message] Erreur détaillée: {str(e)}")
            logger.error(f"[process_message] Traceback: {traceback.format_exc()}")
            return {
                "success": False,
                "response": f"Erreur technique lors du traitement du message: {str(e)}",
                "intent": "error",
                "escalate": False,
                "agents_used": [],
                "processing_time": time.time() - start_time,
                "products": [],
                "recommendations": []
            }

# Instance globale de l'orchestrateur
chatbot_orchestrator = ChatBotOrchestrator()
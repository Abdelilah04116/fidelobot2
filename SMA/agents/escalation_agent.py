from .base_agent import BaseAgent
from typing import Dict, Any, List
import json
from datetime import datetime

class EscalationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="escalation_agent",
            description="Agent de gestion des escalades vers des conseillers humains"
        )
    
    def get_system_prompt(self) -> str:
        return """
        Vous êtes un agent de gestion des escalades.
        Votre rôle est de détecter quand une conversation doit être transférée à un humain.
        
        Critères d'escalade:
        - Incompréhension répétée
        - Demandes complexes hors scope
        - Plaintes importantes
        - Problèmes techniques
        - Demandes de remboursement
        - Situations émotionnelles
        
        Gérez les transitions en douceur et préparez le contexte pour l'agent humain.
        """
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        conversation_history = state.get("conversation_history", [])
        current_intent = state.get("intent", "")
        user_message = state.get("user_message", "")
        failed_attempts = state.get("failed_attempts", 0)
        
        # Analyser si une escalade est nécessaire
        escalation_needed = await self.should_escalate(
            conversation_history, current_intent, user_message, failed_attempts
        )
        
        if escalation_needed:
            # Préparer l'escalade
            escalation_context = await self.prepare_escalation_context(state)
            
            # Générer un message de transition
            transition_message = await self.generate_transition_message(
                escalation_context["reason"]
            )
            
            state["response_text"] = transition_message
            state["escalate"] = True
            return state
        else:
            state["response_text"] = "Votre demande nécessite l'intervention d'un conseiller humain. Un transfert est en cours."
            state["escalate"] = True
            return state
    
    async def should_escalate(self, conversation_history: List[Dict], 
                            intent: str, message: str, failed_attempts: int) -> bool:
        """Déterminer si une escalade est nécessaire"""
        
        # Escalade automatique après échecs répétés
        if failed_attempts >= 3:
            return True
        
        # Intentions nécessitant une escalade humaine
        escalation_intents = [
            "complaint",
            "refund_request", 
            "technical_problem",
            "complex_return",
            "billing_issue"
        ]
        
        if intent in escalation_intents:
            return True
        
        # Analyser le sentiment et la complexité du message
        escalation_analysis = await self.analyze_escalation_need(message)
        
        return escalation_analysis.get("needs_escalation", False)
    
    async def analyze_escalation_need(self, message: str) -> Dict[str, Any]:
        """Analyser si le message nécessite une escalade"""
        prompt = f"""
        Analysez ce message client pour déterminer s'il nécessite une escalade vers un agent humain:
        
        Message: "{message}"
        
        Critères d'escalade:
        - Plainte ou mécontentement fort
        - Demande de remboursement
        - Problème technique complexe
        - Situation urgente
        - Émotions négatives intenses
        - Demande sortant du scope du chatbot
        
        Répondez en JSON:
        {{
            "needs_escalation": true/false,
            "confidence": 0.0-1.0,
            "reason": "raison principale",
            "sentiment": "positive/negative/neutral",
            "urgency": "low/medium/high"
        }}
        """
        
        response = await self.generate_response(prompt)
        
        try:
            return json.loads(response)
        except:
            return {"needs_escalation": False, "confidence": 0.5}
    
    async def prepare_escalation_context(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Préparer le contexte pour l'agent humain"""
        return {
            "session_id": state.get("session_id"),
            "user_id": state.get("user_id"),
            "user_profile": state.get("user_profile", {}),
            "conversation_history": state.get("conversation_history", [])[-10:],  # 10 derniers messages
            "current_intent": state.get("intent"),
            "failed_attempts": state.get("failed_attempts", 0),
            "reason": "Complex issue requiring human assistance",
            "escalated_at": datetime.utcnow().isoformat(),
            "previous_agents": state.get("agents_used", [])
        }
    
    async def generate_transition_message(self, reason: str) -> str:
        """Générer un message de transition vers l'agent humain"""
        prompt = f"""
        Générez un message de transition poli et rassurant pour transférer la conversation 
        vers un conseiller humain.
        
        Raison du transfert: {reason}
        
        Le message doit:
        - Expliquer pourquoi un humain va prendre le relais
        - Rassurer le client
        - Indiquer le temps d'attente approximatif
        - Rester professionnel et empathique
        """
        
        return await self.generate_response(prompt)

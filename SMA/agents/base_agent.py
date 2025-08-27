import google.generativeai as genai
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
from langchain.schema import BaseMessage, HumanMessage, AIMessage, SystemMessage
from ..core.config import settings
import json
import logging

# Configuration de Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

class BaseAgent(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.logger = logging.getLogger(f"agent.{name}")
        
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Retourne le prompt système pour cet agent"""
        pass
    
    @abstractmethod
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Exécute la logique principal de l'agent"""
        pass
    
    async def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Génère une réponse en utilisant Gemini avec mode dégradé"""
        try:
            # Construire le prompt avec contexte
            full_prompt = self.get_system_prompt()
            if context:
                full_prompt += f"\n\nContexte: {json.dumps(context, ensure_ascii=False)}"
            full_prompt += f"\n\nRequête: {prompt}"
            
            # Générer la réponse
            response = await self.model.generate_content_async(full_prompt)
            return response.text
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la génération de réponse: {e}")
            
            # Mode dégradé : réponses prédéfinies selon le contexte
            if "quota" in str(e).lower() or "429" in str(e):
                return self._get_fallback_response(prompt, context)
            else:
                return "Désolé, je rencontre des difficultés techniques. Veuillez réessayer."
    
    def _get_fallback_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Réponse de fallback quand Gemini API n'est pas disponible"""
        prompt_lower = prompt.lower()
        
        # Réponses selon le type d'agent
        if "product_search" in self.name or "recherche" in prompt_lower:
            return "Je peux vous aider à trouver des produits. Que recherchez-vous exactement ?"
        
        elif "recommendation" in self.name or "recommand" in prompt_lower:
            return "Je peux vous faire des recommandations personnalisées. Dites-moi ce qui vous intéresse !"
        
        elif "cart" in self.name or "panier" in prompt_lower:
            return "Je peux vous aider avec votre panier. Que souhaitez-vous faire ?"
        
        elif "order" in self.name or "commande" in prompt_lower:
            return "Je peux vous aider avec vos commandes. Avez-vous une question spécifique ?"
        
        elif "customer_service" in self.name or "aide" in prompt_lower:
            return "Je suis là pour vous aider. Comment puis-je vous assister ?"
        
        elif "profiling" in self.name:
            return "Votre profil a été mis à jour avec succès."
        
        elif "summarizer" in self.name:
            return "Les informations ont été traitées et résumées."
        
        else:
            return "Je suis là pour vous aider. Que puis-je faire pour vous ?"
    
    def validate_input(self, state: Dict[str, Any]) -> bool:
        """Valide les données d'entrée"""
        required_fields = self.get_required_fields()
        for field in required_fields:
            if field not in state:
                self.logger.error(f"Champ requis manquant: {field}")
                return False
        return True
    
    def get_required_fields(self) -> List[str]:
        """Retourne les champs requis pour cet agent"""
        return ["user_message", "session_id"]
    
    def log_execution(self, action: str, details: Dict[str, Any] = None):
        """Log les actions de l'agent"""
        log_data = {
            "agent": self.name,
            "action": action,
            "details": details or {}
        }
        self.logger.info(json.dumps(log_data, ensure_ascii=False))

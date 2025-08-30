from .base_agent import BaseAgent
from typing import Dict, Any, List
import json

class ConversationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="conversation_agent",
            description="Agent orchestrateur central qui gère les conversations"
        )
        
    def get_system_prompt(self) -> str:
        return """
        Vous êtes l'agent de conversation principal d'un chatbot e-commerce.
        Votre rôle est d'orchestrer les autres agents et de fournir des réponses cohérentes.
        
        Capacités:
        - Analyser l'intention de l'utilisateur
        - Déterminer quels agents solliciter
        - Synthétiser les réponses des différents agents
        - Maintenir le contexte de conversation
        - Gérer les escalades vers des agents humains
        
        Règles:
        - Toujours être poli et professionnel
        - Personnaliser les réponses selon le profil utilisateur
        - Proposer des alternatives si la demande ne peut être satisfaite
        - Encourager l'achat de manière subtile
        """
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Orchestrer la conversation"""
        if not self.validate_input(state):
            state["response_text"] = "Données d'entrée invalides."
            return state
        
        user_message = state["user_message"]
        session_id = state["session_id"]
        user_profile = state.get("user_profile", {})
        
        # Analyser l'intention
        intent = await self.analyze_intent(user_message)
        state["intent"] = intent
        state["confidence"] = 0.8
        
        # Gestion spécifique pour l'intention 'bot_role'
        if intent == "bot_role":
            state["response_text"] = "Je suis un assistant virtuel conçu pour vous aider à trouver des produits, gérer vos commandes et répondre à vos questions sur notre boutique."
            return state
        
        # Déterminer les agents à solliciter
        agents = self.determine_agents(intent)

        # Vérification supplémentaire : si l'intention est 'product_search' mais que la requête ne contient pas de mots-clés produits, utiliser le fallback personnalisé
        if (
            agents == ["product_search_agent", "summarizer_agent"]
            and not self._contains_product_keywords(user_message)
        ) or agents == ["personalized_fallback"]:
            state["response_text"] = await self.generate_personalized_fallback_response(user_message, user_profile)
        else:
            # Laisser les agents spécialisés traiter
            state["response_text"] = ""  # Vide pour que l'agent spécialisé génère la réponse
        
        return state
    
    async def analyze_intent(self, message: str) -> str:
        """Analyser l'intention du message utilisateur"""
        message_lower = message.lower()
        
        # Détection directe pour les cas évidents - ORDRE IMPORTANT (plus spécifique en premier)
        if any(word in message_lower for word in ["rôle", "role", "mission", "qui es-tu", "ta fonction", "ta mission", "à quoi sers-tu", "présente-toi", "about you", "your role", "who are you"]):
            return "bot_role"
        if any(word in message_lower for word in ["bonjour", "salut", "hello", "hi", "hey"]):
            return "greeting"
        elif any(word in message_lower for word in ["panier", "cart", "voir mon panier", "mon panier", "afficher panier"]):
            return "cart_management"
        elif any(word in message_lower for word in ["ajouter au panier", "ajouter", "mettre dans le panier", "add to cart"]):
            return "cart_management"
        elif any(word in message_lower for word in ["supprimer du panier", "retirer", "enlever du panier", "remove from cart"]):
            return "cart_management"
        elif any(word in message_lower for word in ["modifier quantité", "changer quantité", "quantité"]):
            return "cart_management"
        elif any(word in message_lower for word in ["vider le panier", "vider panier", "clear cart"]):
            return "cart_management"
        elif any(word in message_lower for word in ["commande", "order", "statut", "status", "suivi"]):
            return "order_status"
        elif any(word in message_lower for word in ["recommand", "suggestion", "cadeau", "gift"]):
            return "recommendation"
        elif any(word in message_lower for word in ["aide", "help", "problème", "souci"]):
            return "customer_service"
        elif any(word in message_lower for word in ["liste", "produits", "catalogue"]):
            return "product_search"
        elif any(word in message_lower for word in ["avez", "disponible", "stock", "avoir", "est ce que"]):
            return "availability_check"
        elif any(word in message_lower for word in ["prix", "coût", "tarif", "combien"]):
            return "price_check"
        
        # Mode dégradé : détection basique sans IA
        # Recherche de mots-clés produits
        product_keywords = ["iphone", "samsung", "laptop", "ordinateur", "smartphone", "tablette", "écran", "clavier", "souris"]
        if any(keyword in message_lower for keyword in product_keywords):
            return "product_search"
        
        # Par défaut, considérer comme recherche de produit
        return "product_search"
    
    def determine_agents(self, intent: str) -> List[str]:
        """Déterminer quels agents solliciter selon l'intention"""
        agent_mapping = {
            "product_search": ["product_search_agent"],  # Sans summarizer pour éviter les conflits
            "product_info": ["product_search_agent"],
            "recommendation": ["personalized_fallback"],  # Désactivé - utilise fallback
            "order_status": ["order_management_agent"],
            "cart_management": ["product_search_agent"],
            "customer_service": ["escalation_agent"],
            "promotion_inquiry": ["product_search_agent"],
            "gift_suggestion": ["personalized_fallback"],  # Désactivé - utilise fallback
            "availability_check": ["product_search_agent"],  # Route vers product_search_agent
            "price_check": ["product_search_agent"],  # Route vers product_search_agent
            "return_policy": ["customer_service_agent"],
            "general_chat": ["summarizer_agent"]
        }
        
        # Si l'intention n'est pas reconnue, utiliser le fallback personnalisé
        return agent_mapping.get(intent, ["personalized_fallback"])

    async def generate_personalized_fallback_response(self, user_message: str, user_profile: dict) -> str:
        """Générer une réponse personnalisée selon le profil, l'historique d'achat et les services du site."""
        # Mode dégradé sans IA
        first_name = user_profile.get("first_name", "")
        segment = user_profile.get("segment", "client")
        
        # Réponses prédéfinies selon le contexte
        if "bonjour" in user_message.lower() or "salut" in user_message.lower():
            greeting = f"Bonjour {first_name} ! " if first_name else "Bonjour ! "
            return greeting + "Comment puis-je vous aider aujourd'hui ? Je peux vous aider à trouver des produits, vérifier la disponibilité, ou vous donner des recommandations."
        
        elif "merci" in user_message.lower():
            return "Je vous en prie ! N'hésitez pas si vous avez d'autres questions. Notre équipe est là pour vous accompagner."
        
        elif "au revoir" in user_message.lower() or "bye" in user_message.lower():
            return "Au revoir ! N'hésitez pas à revenir si vous avez besoin d'aide. Bonne journée !"
        
        else:
            # Réponse générique mais utile
            return f"Merci pour votre message ! Je suis là pour vous aider avec nos produits et services. Que souhaitez-vous faire aujourd'hui ?"

    def _contains_product_keywords(self, message: str) -> bool:
        """Détecte si le message contient des mots-clés produits ou catégories e-commerce."""
        keywords = [
            "produit", "produits", "article", "articles", "catalogue", "catégorie", "catégories",
            "modèle", "modèles", "marque", "prix", "acheter", "vente", "disponible", "stock",
            "référence", "bestseller", "nouveauté", "promotion", "offre", "panier", "commande"
        ]
        message_lower = message.lower()
        return any(kw in message_lower for kw in keywords)

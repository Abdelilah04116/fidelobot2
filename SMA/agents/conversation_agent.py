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
        
        # Pour les cas plus complexes, utiliser l'IA
        prompt = f"""
        Analysez l'intention de ce message utilisateur dans le contexte d'un site e-commerce:
        "{message}"
        
        Intentions possibles:
        - product_search: recherche de produits, demande de liste, catalogue
        - product_info: informations sur un produit spécifique
        - recommendation: demande de recommandations, suggestions
        - order_status: vérification de commande, suivi
        - cart_management: gestion du panier
        - customer_service: service client, aide, problèmes
        - promotion_inquiry: demande de promotions
        - gift_suggestion: suggestion de cadeau
        - availability_check: vérification de disponibilité
        - return_policy: politique de retour
        - greeting: salutations
        - general_chat: conversation générale
        
        Répondez uniquement par l'intention détectée.
        """
        
        intent = await self.generate_response(prompt)
        return intent.strip().lower()
    
    def determine_agents(self, intent: str) -> List[str]:
        """Déterminer quels agents solliciter selon l'intention"""
        agent_mapping = {
            "product_search": ["product_search_agent", "summarizer_agent"],
            "product_info": ["product_search_agent", "summarizer_agent"],
            "recommendation": ["recommendation_agent", "customer_profiling_agent"],
            "order_status": ["order_management_agent"],
            "cart_management": ["product_search_agent"],
            "customer_service": ["escalation_agent"],
            "promotion_inquiry": ["product_search_agent"],
            "gift_suggestion": ["recommendation_agent", "customer_profiling_agent"],
            "availability_check": ["product_search_agent"],
            "return_policy": ["customer_service_agent"],
            "general_chat": ["summarizer_agent"]
        }
        
        # Si l'intention n'est pas reconnue, utiliser le fallback personnalisé
        return agent_mapping.get(intent, ["personalized_fallback"])

    async def generate_personalized_fallback_response(self, user_message: str, user_profile: dict) -> str:
        """Générer une réponse personnalisée selon le profil, l'historique d'achat et les services du site."""
        # Récupérer l'historique d'achat et les services du site si disponibles
        purchase_history = user_profile.get("purchase_history", [])
        first_name = user_profile.get("first_name", "")
        segment = user_profile.get("segment", "client")
        # Exemple de services/produits (à adapter selon ton projet)
        services = user_profile.get("services", [
            "Livraison rapide",
            "Paiement sécurisé",
            "Support client 24/7",
            "Large choix de produits"
        ])
        # Construire un prompt personnalisé
        prompt = f"""
Vous êtes l'assistant principal d'un site e-commerce.
L'utilisateur a envoyé : '{user_message}'
Profil utilisateur : prénom = {first_name}, segment = {segment}
Historique d'achat : {purchase_history if purchase_history else 'aucun achat enregistré'}
Services proposés : {', '.join(services)}

Générez une réponse utile, personnalisée et engageante, en valorisant les services du site et en tenant compte du profil et de l'historique d'achat. Si possible, proposez un produit ou service pertinent.
"""
        response = await self.generate_response(prompt)
        return response.strip()

    def _contains_product_keywords(self, message: str) -> bool:
        """Détecte si le message contient des mots-clés produits ou catégories e-commerce."""
        keywords = [
            "produit", "produits", "article", "articles", "catalogue", "catégorie", "catégories",
            "modèle", "modèles", "marque", "prix", "acheter", "vente", "disponible", "stock",
            "référence", "bestseller", "nouveauté", "promotion", "offre", "panier", "commande"
        ]
        message_lower = message.lower()
        return any(kw in message_lower for kw in keywords)

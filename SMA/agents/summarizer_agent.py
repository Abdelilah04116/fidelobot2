from .base_agent import BaseAgent
from typing import Dict, Any, List

class SummarizerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="summarizer_agent",
            description="Agent de synthèse et structuration des informations"
        )
    
    def get_system_prompt(self) -> str:
        return """
        Vous êtes un expert en synthèse d'informations pour le e-commerce.
        Votre rôle est de condenser et structurer les informations complexes.
        
        Capacités:
        - Résumer les descriptions de produits
        - Synthétiser les avis clients
        - Structurer les réponses techniques
        - Adapter le niveau de détail selon le contexte
        
        Règles:
        - Soyez concis mais informatif
        - Utilisez un langage accessible
        - Mettez en avant les points clés
        - Adaptez le ton selon l'audience
        """
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        content_type = state.get("content_type", "general")
        raw_data = state.get("raw_data", {})
        user_profile = state.get("user_profile", {})
        user_message = state.get("user_message", "")
        intent = state.get("intent", "")
        
        # Enrichir les données brutes avec le contexte
        enriched_data = {
            **raw_data,
            "user_message": user_message,
            "intent": intent,
            "user_profile": user_profile
        }
        
        if content_type == "product_summary":
            summary = await self.summarize_products(raw_data.get("products", []))
        elif content_type == "recommendations":
            summary = await self.summarize_recommendations(raw_data.get("recommendations", []))
        elif content_type == "order_status":
            summary = await self.summarize_order_status(raw_data)
        elif content_type == "cart_summary":
            summary = await self.summarize_cart(raw_data.get("cart", {}))
        else:
            summary = await self.general_summary(enriched_data)
        
        # Adapter selon le profil utilisateur
        adapted_summary = await self.adapt_to_user(summary, user_profile)
        state["response_text"] = adapted_summary
        return state
    
    async def summarize_products(self, products: List[Dict]) -> str:
        """Résumer une liste de produits"""
        if not products:
            return "Aucun produit trouvé pour votre recherche."
        
        context = {
            "total_products": len(products),
            "products": products[:5]  # Limiter pour le contexte
        }
        
        prompt = f"""
        Résumez cette sélection de produits de manière engageante:
        
        {len(products)} produits trouvés
        
        Produits principaux:
        """
        for i, product in enumerate(products[:3], 1):
            prompt += f"\n{i}. {product['name']} - {product['price']}€"
            if product.get('average_rating'):
                prompt += f" (Note: {product['average_rating']:.1f}/5)"
        
        prompt += """
        
        Créez un résumé qui:
        - Présente les produits de manière attractive
        - Mentionne les gammes de prix
        - Souligne les points forts
        - Encourage à explorer davantage
        """
        
        return await self.generate_response(prompt, context)
    
    async def summarize_recommendations(self, recommendations: List[Dict]) -> str:
        """Résumer des recommandations personnalisées"""
        if not recommendations:
            return "Je n'ai pas pu générer de recommandations personnalisées pour le moment."
        
        context = {"recommendations": recommendations[:5]}
        
        prompt = f"""
        Présentez ces recommandations de manière personnalisée et engageante:
        
        Recommandations:
        """
        for rec in recommendations[:3]:
            prompt += f"\n• {rec['name']} - {rec['price']}€"
            if rec.get('reason'):
                prompt += f" ({rec['reason']})"
        
        prompt += """
        
        Créez une présentation qui:
        - Explique pourquoi ces produits sont recommandés
        - Met en avant les bénéfices pour l'utilisateur
        - Encourage à découvrir les produits
        - Reste naturel et conversationnel
        """
        
        return await self.generate_response(prompt, context)
    
    async def summarize_order_status(self, order_data: Dict) -> str:
        """Résumer le statut d'une commande"""
        context = {"order": order_data}
        
        prompt = f"""
        Résumez le statut de cette commande de manière claire:
        
        Commande: {order_data.get('order_id', 'N/A')}
        Statut: {order_data.get('status', 'N/A')}
        Total: {order_data.get('total_amount', 0)}€
        
        Créez un résumé qui:
        - Informe clairement sur le statut
        - Donne les prochaines étapes si applicable
        - Rassure le client
        - Propose de l'aide si nécessaire
        """
        
        return await self.generate_response(prompt, context)
    
    async def adapt_to_user(self, summary: str, user_profile: Dict) -> str:
        """Adapter le résumé selon le profil utilisateur"""
        if not user_profile:
            return summary
        
        segment = user_profile.get("segment", "")
        is_vip = user_profile.get("is_vip", False)
        
        if is_vip:
            # Ton plus personnalisé pour les VIP
            adaptation_prompt = f"""
            Adaptez ce texte pour un client VIP en:
            - Utilisant un ton plus personnalisé
            - Mentionnant des avantages exclusifs si pertinent
            - Montrant de la reconnaissance pour la fidélité
            
            Texte original: {summary}
            """
        elif segment == "new_customer":
            # Ton plus accueillant pour les nouveaux
            adaptation_prompt = f"""
            Adaptez ce texte pour un nouveau client en:
            - Utilisant un ton accueillant
            - Expliquant les services disponibles
            - Encourageant l'exploration
            
            Texte original: {summary}
            """
        else:
            return summary
        
        return await self.generate_response(adaptation_prompt)

    async def general_summary(self, raw_data: Dict[str, Any]) -> str:
        """Générer un résumé général à partir de données brutes"""
        intent = raw_data.get("intent", "")
        user_message = raw_data.get("user_message", "")
        
        # Réponses contextuelles selon l'intention
        if intent == "greeting":
            return "Bonjour ! Je suis votre assistant SMA spécialisé dans le e-commerce. Je peux vous aider à :\n\n• **Rechercher des produits** - Dites-moi ce que vous cherchez\n• **Vérifier vos commandes** - Suivi et statut de livraison\n• **Obtenir des recommandations** - Suggestions personnalisées\n• **Gérer votre panier** - Ajout, modification, validation\n\nQue souhaitez-vous faire aujourd'hui ?"
        
        elif intent == "product_search":
            return f"Je vais rechercher des produits pour vous. Votre demande était : '{user_message}'\n\n🔍 **Recherche en cours...**\n\nSi aucun produit n'est trouvé, je peux vous proposer des alternatives ou des recommandations similaires."
        
        elif intent == "order_status":
            return "Pour vérifier le statut de vos commandes, j'ai besoin de quelques informations :\n\n• Numéro de commande\n• Ou votre email et date de commande\n\nJe peux aussi vous aider à suivre vos livraisons en temps réel."
        
        elif intent == "recommendation":
            return "Excellente idée ! Je vais analyser vos préférences pour vous proposer des recommandations personnalisées.\n\n🎯 **Recommandations en cours de génération...**\n\nBasées sur vos achats précédents et les tendances actuelles."
        
        elif intent == "customer_service":
            return "Je suis là pour vous aider ! Pouvez-vous me décrire votre problème ou votre question ?\n\nJe peux vous assister pour :\n• Problèmes de commande\n• Questions sur les produits\n• Retours et remboursements\n• Informations générales"
        
        else:
            # Réponse générique mais dynamique
            return f"Merci pour votre message ! Je suis votre assistant SMA et je peux vous aider avec :\n\n🛍️ **Produits** - Recherche, informations, disponibilité\n📦 **Commandes** - Suivi, statut, historique\n💡 **Recommandations** - Suggestions personnalisées\n🛒 **Panier** - Gestion et validation\n❓ **Aide** - Service client et support\n\nDites-moi ce qui vous intéresse !"

    async def summarize_cart(self, cart: Dict[str, Any]) -> str:
        if not cart or cart.get("is_empty"):
            return "Votre panier est vide. Vous pouvez ajouter des articles à tout moment."
        items = cart.get("items", [])
        total_items = cart.get("total_items", 0)
        total_price = cart.get("total_price", 0.0)
        lines = [f"Votre panier contient {total_items} article(s) pour un total de {total_price}€:"]
        for it in items[:5]:
            lines.append(f"- {it['name']} x{it['quantity']} — {it['total']}€")
        if len(items) > 5:
            lines.append(f"... et {len(items)-5} autre(s) article(s)")
        lines.append("Souhaitez-vous finaliser votre commande ou continuer vos achats ?")
        return "\n".join(lines)

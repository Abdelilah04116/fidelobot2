"""
Agent de service client - gère les demandes de support et d'aide
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from .base_agent import BaseAgent
# Import des modèles (à adapter selon ta structure)
try:
    from catalogue.backend.database import SessionLocal
except ImportError:
    # Fallback si les modèles ne sont pas disponibles
    SessionLocal = None
# AGENT CONNECTÉ À POSTGRES (relationnel)
# Utilisez SessionLocal() pour accéder aux tickets, utilisateurs, commandes
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
import json

logger = logging.getLogger(__name__)

class CustomerServiceAgent(BaseAgent):
    """Agent de service client et support"""
    
    def __init__(self):
        super().__init__(
            name="customer_service_agent",
            description="Agent de service client et support"
        )
        self.logger = logging.getLogger(__name__)
        
        # Base de connaissances pour le support
        self.knowledge_base = {
            "livraison": {
                "délais": "Nos délais de livraison sont de 2-5 jours ouvrés en France métropolitaine.",
                "suivi": "Vous pouvez suivre votre commande dans votre espace client ou avec le numéro de suivi.",
                "retard": "En cas de retard, contactez-nous avec votre numéro de commande."
            },
            "retour": {
                "délai": "Vous avez 14 jours pour retourner un article.",
                "procédure": "Connectez-vous à votre espace client et sélectionnez 'Retourner un article'.",
                "remboursement": "Le remboursement est effectué sous 5-10 jours ouvrés."
            },
            "paiement": {
                "moyens": "Nous acceptons les cartes bancaires, PayPal et Apple Pay.",
                "sécurité": "Tous nos paiements sont sécurisés par cryptage SSL.",
                "problème": "En cas de problème de paiement, vérifiez vos informations bancaires."
            },
            "compte": {
                "création": "Cliquez sur 'Créer un compte' en haut à droite de la page.",
                "mot_de_passe": "Utilisez la fonction 'Mot de passe oublié' sur la page de connexion.",
                "modification": "Modifiez vos informations dans votre espace client."
            }
        }
        
        # Base de connaissances FAQ
        self.faq_categories = {
            "livraison": ["délais", "frais", "suivi", "retard", "adresse"],
            "paiement": ["moyens", "sécurité", "remboursement", "facture"],
            "retours": ["délai", "procédure", "remboursement", "échange"],
            "produits": ["garantie", "entretien", "utilisation", "spécifications"],
            "compte": ["création", "modification", "mot de passe", "profil"]
        }
    
    def get_system_prompt(self) -> str:
        return """
        Vous êtes un expert en service client e-commerce.
        Votre rôle est d'aider les clients avec leurs questions et problèmes.
        
        Capacités:
        - Répondre aux questions fréquentes (FAQ)
        - Gérer les retours et échanges
        - Traiter les réclamations
        - Fournir des informations sur la livraison et paiement
        - Guider vers l'escalade si nécessaire
        
        Soyez toujours empathique, professionnel et orienté solution.
        """
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            user_message = state.get("user_message", "").lower()
            
            # Détecter le type de demande
            if any(keyword in user_message for keyword in ["retourner", "retour", "remboursement", "échanger"]):
                if "produit" in user_message:
                    return await self.handle_return_request(state)
                else:
                    return await self.handle_general_return_info(state)
            
            elif any(keyword in user_message for keyword in ["aide", "support", "problème", "question"]):
                return await self.handle_general_help(state)
            
            elif any(keyword in user_message for keyword in ["livraison", "délai", "suivi"]):
                return await self.handle_delivery_info(state)
            
            elif any(keyword in user_message for keyword in ["paiement", "facture", "remboursement"]):
                return await self.handle_payment_info(state)
            
            else:
                # Demande générale de service client
                return await self.handle_general_help(state)
                
        except Exception as e:
            self.logger.error(f"Erreur critique dans CustomerServiceAgent: {str(e)}")
            return {"error": "Erreur technique de service client"}
    
    async def search_faq_safe(self, question: str) -> Dict[str, Any]:
        """Rechercher dans la FAQ de manière sécurisée"""
        try:
            if not question or len(question.strip()) < 3:
                return {"error": "Question trop courte pour la recherche"}
            
            question_lower = question.lower().strip()
            
            # Recherche par mots-clés dans les catégories
            matched_categories = []
            for category, keywords in self.faq_categories.items():
                for keyword in keywords:
                    if keyword in question_lower:
                        matched_categories.append(category)
                        break
            
            # Recherche dans la base de connaissances
            if SessionLocal:
                db = SessionLocal()
                try:
                    faq_results = []
                    # TODO: Implémenter la vraie recherche quand les modèles sont disponibles
                finally:
                    db.close()
            else:
                # Fallback : recherche dans la base locale
                faq_results = self._search_local_faq(question_lower, matched_categories)
            
            # Traiter les résultats de la recherche
            if faq_results:
                # Trier par pertinence si on a des scores
                if any("relevance_score" in faq for faq in faq_results):
                    faq_results.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
                    
                    return {
                        "faq_results": faq_results[:5],  # Top 5
                        "total_found": len(faq_results),
                        "matched_categories": matched_categories,
                        "search_query": question
                    }
            
            # Si pas de résultats ou erreur
            return {
                "faq_results": [],
                "total_found": 0,
                "matched_categories": matched_categories,
                "search_query": question
            }
            
        except Exception as e:
            self.logger.error(f"Erreur recherche FAQ: {str(e)}")
            return {"error": str(e)}
    
    def _calculate_relevance(self, question: str, faq_question: str, faq_keywords: List[str]) -> float:
        """Calculer la pertinence entre une question et une FAQ"""
        try:
            score = 0.0
            
            # Score par mots communs
            question_words = set(question.split())
            faq_words = set(faq_question.lower().split())
            common_words = question_words.intersection(faq_words)
            
            if common_words:
                score += len(common_words) / max(len(question_words), len(faq_words)) * 0.6
            
            # Score par mots-clés
            if faq_keywords:
                keyword_matches = sum(1 for keyword in faq_keywords if keyword.lower() in question)
                score += (keyword_matches / len(faq_keywords)) * 0.4
            
            return min(score, 1.0)
            
        except Exception:
            return 0.0
    
    def _search_local_faq(self, question: str, categories: List[str]) -> List[Dict[str, Any]]:
        """Recherche dans la base locale de connaissances"""
        results = []
        
        # Recherche par catégories
        for category in categories:
            if category in self.knowledge_base:
                for key, answer in self.knowledge_base[category].items():
                    if key.lower() in question or any(word in question for word in key.split()):
                        results.append({
                            "id": f"{category}_{key}",
                            "question": f"Question sur {key}",
                            "answer": answer,
                            "category": category,
                            "relevance_score": 0.8,
                            "keywords": [key]
                        })
        
        return results[:5]  # Limiter à 5 résultats
    
    async def handle_return_exchange_safe(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Gérer les retours et échanges de manière sécurisée"""
        db: Optional[Session] = None
        try:
            user_id = state.get("user_id")
            order_id = state.get("order_id")
            product_id = state.get("product_id")
            reason = state.get("reason", "")
            return_type = state.get("return_type", "return")  # return ou exchange
            
            if not all([user_id, order_id, product_id]):
                return {"error": "Informations de commande incomplètes"}
            
            db = SessionLocal()
            
            # Vérifier que la commande appartient à l'utilisateur
            order = db.query(Order).filter(
                Order.id == order_id,
                Order.user_id == user_id
            ).first()
            
            if not order:
                return {"error": "Commande non trouvée"}
            
            # Vérifier que le produit est dans la commande
            order_item = db.query(OrderItem).filter(
                OrderItem.order_id == order_id,
                OrderItem.product_id == product_id
            ).first()
            
            if not order_item:
                return {"error": "Produit non trouvé dans la commande"}
            
            # Vérifier la date de livraison pour le délai de retour
            delivery_date = getattr(order, 'delivery_date', order.created_at)
            days_since_delivery = (datetime.utcnow() - delivery_date).days
            
            if days_since_delivery > 30:
                return {"error": "Délai de retour dépassé (30 jours)"}
            
            # Informations de retour
            return_info = {
                "order_id": order_id,
                "product_id": product_id,
                "product_name": order_item.product.name if hasattr(order_item, 'product') else "Produit",
                "quantity": order_item.quantity,
                "return_type": return_type,
                "reason": reason,
                "days_since_delivery": days_since_delivery,
                "return_deadline": "30 jours après livraison",
                "status": "pending"
            }
            
            # Procédure selon le type
            if return_type == "return":
                return_info.update({
                    "procedure": "Retour par colis avec étiquette prépayée",
                    "refund_method": "Même moyen de paiement",
                    "refund_delay": "5-10 jours ouvrés",
                    "shipping_cost": "Gratuit"
                })
            else:  # exchange
                return_info.update({
                    "procedure": "Échange sur place ou par colis",
                    "exchange_options": "Même produit ou équivalent",
                    "processing_delay": "3-5 jours ouvrés",
                    "shipping_cost": "Gratuit"
                })
            
            return {
                "success": True,
                "return_info": return_info,
                "next_steps": [
                    "Confirmer le retour/échange",
                    "Imprimer l'étiquette de retour",
                    "Emballer le produit",
                    "Déposer en point relais ou bureau de poste"
                ],
                "contact_info": {
                    "email": "retours@fidelobot.com",
                    "phone": "01 23 45 67 89",
                    "hours": "Lun-Ven 9h-18h"
                }
            }
            
        except Exception as e:
            self.logger.error(f"Erreur gestion retour/échange: {str(e)}")
            return {"error": str(e)}
        finally:
            if db:
                db.close()
    
    async def handle_complaint_safe(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Gérer les réclamations de manière proactive"""
        try:
            user_id = state.get("user_id")
            complaint_type = state.get("complaint_type", "")
            description = state.get("description", "")
            urgency = state.get("urgency", "medium")
            
            if not description or len(description.strip()) < 10:
                return {"error": "Description de la réclamation trop courte"}
            
            # Catégoriser la réclamation
            complaint_categories = {
                "delivery": ["livraison", "retard", "dommage", "perdu"],
                "product": ["défaut", "qualité", "conformité", "description"],
                "service": ["attente", "réponse", "compétence", "politesse"],
                "billing": ["facturation", "paiement", "remboursement", "frais"],
                "website": ["bug", "erreur", "performance", "interface"]
            }
            
            detected_category = "general"
            for category, keywords in complaint_categories.items():
                if any(keyword in description.lower() for keyword in keywords):
                    detected_category = category
                    break
            
            # Niveau d'urgence
            urgency_levels = {
                "low": {"response_time": "48h", "priority": "normale"},
                "medium": {"response_time": "24h", "priority": "élevée"},
                "high": {"response_time": "4h", "priority": "critique"}
            }
            
            urgency_info = urgency_levels.get(urgency, urgency_levels["medium"])
            
            # Actions immédiates selon le type
            immediate_actions = []
            if detected_category == "delivery" and urgency == "high":
                immediate_actions.append("Contact immédiat du transporteur")
                immediate_actions.append("Recherche du colis")
            elif detected_category == "billing" and urgency == "high":
                immediate_actions.append("Vérification immédiate de la facturation")
                immediate_actions.append("Suspension des prélèvements si nécessaire")
            
            # Plan de résolution
            resolution_plan = {
                "immediate": immediate_actions,
                "short_term": [
                    "Analyse détaillée de la réclamation",
                    "Contact du client dans les délais",
                    "Proposition de solution"
                ],
                "long_term": [
                    "Mise en place de mesures préventives",
                    "Formation des équipes si nécessaire",
                    "Suivi de la satisfaction client"
                ]
            }
            
            return {
                "success": True,
                "complaint_info": {
                    "id": f"COMP-{user_id}-{datetime.utcnow().strftime('%Y%m%d%H%M')}",
                    "type": detected_category,
                    "urgency": urgency,
                    "response_time": urgency_info["response_time"],
                    "priority": urgency_info["priority"],
                    "status": "en_cours"
                },
                "resolution_plan": resolution_plan,
                "next_steps": [
                    f"Réponse dans les {urgency_info['response_time']}",
                    "Analyse approfondie de la situation",
                    "Proposition de solution personnalisée"
                ],
                "escalation_needed": urgency == "high" or detected_category in ["billing", "delivery"],
                "contact_info": {
                    "email": "reclamations@fidelobot.com",
                    "phone": "01 23 45 67 90",
                    "urgent_phone": "01 23 45 67 91"
                }
            }
            
        except Exception as e:
            self.logger.error(f"Erreur gestion réclamation: {str(e)}")
            return {"error": str(e)}
    
    async def get_delivery_info_safe(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Obtenir les informations de livraison"""
        try:
            user_id = state.get("user_id")
            order_id = state.get("order_id")
            
            delivery_info = {
                "standard_delivery": {
                    "name": "Livraison standard",
                    "delay": "3-5 jours ouvrés",
                    "cost": "5.99€",
                    "free_threshold": "50€",
                    "tracking": "Oui"
                },
                "express_delivery": {
                    "name": "Livraison express",
                    "delay": "1-2 jours ouvrés",
                    "cost": "12.99€",
                    "free_threshold": "100€",
                    "tracking": "Oui"
                },
                "same_day": {
                    "name": "Livraison le jour même",
                    "delay": "Le jour même",
                    "cost": "19.99€",
                    "free_threshold": "200€",
                    "tracking": "Oui",
                    "available_cities": ["Paris", "Lyon", "Marseille", "Bordeaux"]
                },
                "pickup": {
                    "name": "Point relais",
                    "delay": "2-3 jours ouvrés",
                    "cost": "2.99€",
                    "free_threshold": "30€",
                    "tracking": "Oui"
                }
            }
            
            # Informations spécifiques si une commande est fournie
            if order_id and user_id:
                db = SessionLocal()
                try:
                    order = db.query(Order).filter(
                        Order.id == order_id,
                        Order.user_id == user_id
                    ).first()
                    
                    if order:
                        delivery_info["current_order"] = {
                            "order_id": order_id,
                            "status": getattr(order, 'status', 'unknown'),
                            "estimated_delivery": getattr(order, 'estimated_delivery', 'Non disponible'),
                            "tracking_number": getattr(order, 'tracking_number', 'Non disponible')
                        }
                finally:
                    db.close()
            
            return {
                "delivery_options": delivery_info,
                "general_info": {
                    "delivery_zones": "France métropolitaine",
                    "excluded_areas": "DOM-TOM, Îles",
                    "special_instructions": "Livraison en étage possible sur demande",
                    "contact_delivery": "01 23 45 67 92"
                }
            }
            
        except Exception as e:
            self.logger.error(f"Erreur informations livraison: {str(e)}")
            return {"error": str(e)}
    
    async def get_payment_info_safe(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Obtenir les informations de paiement"""
        try:
            payment_info = {
                "accepted_methods": [
                    {
                        "type": "card",
                        "name": "Cartes bancaires",
                        "brands": ["Visa", "Mastercard", "American Express"],
                        "security": "3D Secure, cryptage SSL",
                        "processing_time": "immédiat"
                    },
                    {
                        "type": "digital_wallet",
                        "name": "Portefeuilles numériques",
                        "brands": ["Apple Pay", "Google Pay", "PayPal"],
                        "security": "Biométrie, tokenisation",
                        "processing_time": "immédiat"
                    },
                    {
                        "type": "bank_transfer",
                        "name": "Virement bancaire",
                        "description": "IBAN fourni après commande",
                        "security": "Vérification bancaire",
                        "processing_time": "2-3 jours ouvrés"
                    },
                    {
                        "type": "installments",
                        "name": "Paiement en plusieurs fois",
                        "description": "3x ou 4x sans frais",
                        "conditions": "Montant minimum 200€",
                        "processing_time": "immédiat"
                    }
                ],
                "security_features": [
                    "Cryptage SSL 256 bits",
                    "Certification PCI DSS",
                    "3D Secure obligatoire",
                    "Surveillance anti-fraude 24/7",
                    "Assurance transaction"
                ],
                "refund_policy": {
                    "delay": "5-10 jours ouvrés",
                    "method": "Même moyen de paiement",
                    "conditions": "Produit retourné dans l'état d'origine",
                    "exceptions": "Produits personnalisés, sous-vêtements"
                },
                "contact_billing": {
                    "email": "facturation@fidelobot.com",
                    "phone": "01 23 45 67 93",
                    "hours": "Lun-Ven 9h-18h"
                }
            }
            
            return payment_info
            
        except Exception as e:
            self.logger.error(f"Erreur informations paiement: {str(e)}")
            return {"error": str(e)}
    
    async def get_general_help_safe(self, question: str) -> Dict[str, Any]:
        """Obtenir de l'aide générale"""
        try:
            if not question:
                return {
                    "help_topics": [
                        "Comment passer une commande ?",
                        "Comment suivre ma livraison ?",
                        "Comment retourner un produit ?",
                        "Quels sont les moyens de paiement ?",
                        "Comment modifier mon profil ?"
                    ],
                    "contact_info": {
                        "email": "aide@fidelobot.com",
                        "phone": "01 23 45 67 89",
                        "chat": "Disponible 24/7",
                        "hours": "Support technique : 24h/24, 7j/7"
                    }
                }
            
            # Réponses automatiques simples
            question_lower = question.lower()
            
            if any(word in question_lower for word in ["commande", "acheter", "panier"]):
                return {
                    "answer": "Pour passer une commande, ajoutez des produits à votre panier puis suivez le processus de paiement. Notre assistant vous guide à chaque étape.",
                    "related_topics": ["Panier", "Paiement", "Livraison"],
                    "next_action": "Ajouter des produits à votre panier"
                }
            elif any(word in question_lower for word in ["livraison", "délai", "suivi"]):
                return {
                    "answer": "Les délais de livraison varient de 1 à 5 jours selon l'option choisie. Vous recevrez un numéro de suivi par email.",
                    "related_topics": ["Délais", "Suivi", "Options de livraison"],
                    "next_action": "Consulter les options de livraison"
                }
            elif any(word in question_lower for word in ["retour", "remboursement", "échange"]):
                return {
                    "answer": "Vous disposez de 30 jours pour retourner un produit. Les retours sont gratuits et le remboursement est effectué sous 5-10 jours.",
                    "related_topics": ["Procédure de retour", "Remboursement", "Échanges"],
                    "next_action": "Initier un retour"
                }
            else:
                return {
                    "answer": "Je ne comprends pas parfaitement votre question. Pouvez-vous la reformuler ou choisir un sujet dans la liste ci-dessous ?",
                    "suggested_topics": [
                        "Commandes et achats",
                        "Livraison et suivi",
                        "Retours et remboursements",
                        "Paiement et sécurité",
                        "Profil et compte"
                    ],
                    "contact_human": True
                }
                
        except Exception as e:
            self.logger.error(f"Erreur aide générale: {str(e)}")
            return {"error": str(e)}
    
    def can_handle(self, message: dict) -> bool:
        """Peut gérer les demandes de support et d'aide"""
        content_lower = message.get('content', '').lower()
        support_keywords = [
            "aide", "support", "problème", "difficulté", "question", "comment",
            "livraison", "retour", "paiement", "compte", "commande"
        ]
        return any(keyword in content_lower for keyword in support_keywords)
    
    async def process(self, message: dict, context: dict = None):
        """Traite une demande de support"""
        try:
            # 1. Analyser le type de demande de support
            content = message.get('content', '')
            support_type = self._analyze_support_request(content)
            
            # 2. Rechercher dans la base de connaissances
            knowledge_answer = await self._search_knowledge_base(content, support_type)
            
            # 3. Génère une réponse appropriée
            response_content = await self._generate_support_response(message, knowledge_answer, support_type, context)
            
            return {
                "success": True,
                "content": response_content,
                "support_type": support_type,
                "knowledge_used": knowledge_answer is not None
            }
            
        except Exception as e:
            self.logger.error(f"Error in customer service agent: {str(e)}")
            return {
                "success": False,
                "content": "Je n'ai pas pu traiter votre demande de support. Un conseiller va vous aider.",
                "error": str(e)
            }
    
    def _analyze_support_request(self, content: str) -> str:
        """Analyse le type de demande de support"""
        content_lower = content.lower()
        
        # Catégories de support
        support_categories = {
            "livraison": ["livraison", "livrer", "expédition", "suivi", "colis", "retard"],
            "retour": ["retour", "remboursement", "échanger", "récupérer", "annuler"],
            "paiement": ["paiement", "payer", "carte", "paypal", "erreur", "refusé"],
            "compte": ["compte", "connexion", "mot de passe", "inscription", "profil"],
            "commande": ["commande", "suivi", "annuler", "modifier", "statut"],
            "produit": ["produit", "défaut", "cassé", "ne fonctionne pas", "qualité"],
            "général": ["aide", "support", "question", "problème", "difficulté"]
        }
        
        for category, keywords in support_categories.items():
            if any(keyword in content_lower for keyword in keywords):
                return category
        
        return "général"
    
    async def _search_knowledge_base(self, content: str, support_type: str) -> Optional[str]:
        """Recherche dans la base de connaissances"""
        try:
            # Recherche simple basée sur les mots-clés
            content_lower = content.lower()
            
            if support_type in self.knowledge_base:
                category_knowledge = self.knowledge_base[support_type]
                
                # Chercher la réponse la plus pertinente
                for topic, answer in category_knowledge.items():
                    if topic in content_lower:
                        return answer
                
                # Si pas de correspondance exacte, retourner la première réponse
                if category_knowledge:
                    return list(category_knowledge.values())[0]
            
            # Recherche dans la base de données
            with self.db_manager.get_session() as session:
                knowledge_entries = session.query(KnowledgeBase).filter_by(category=support_type).all()
                
                for entry in knowledge_entries:
                    if any(keyword in content_lower for keyword in entry.keywords or []):
                        return entry.answer
            
            return None
            
        except Exception as e:
            logger.error(f"Error searching knowledge base: {e}")
            return None
    
    def _check_escalation_need(self, message: dict, context: dict = None, support_type: str = "") -> bool:
        """Vérifie si une escalade est nécessaire"""
        # Mots-clés qui indiquent un besoin d'escalade
        escalation_keywords = [
            "urgent", "grave", "insatisfait", "déçu", "fâché", "plainte",
            "réclamation", "responsable", "manager", "superviseur"
        ]
        
        content_lower = message.content.lower()
        
        # Escalade si mots-clés urgents
        if any(keyword in content_lower for keyword in escalation_keywords):
            return True
        
        # Escalade si sentiment très négatif
        if context.sentiment_score < -0.5:
            return True
        
        # Escalade si conversation longue sans résolution
        if len(context.conversation_history) > 15:
            return True
        
        # Escalade pour certains types de support complexes
        complex_support_types = ["produit", "paiement"]
        if support_type in complex_support_types and "problème" in content_lower:
            return True
        
        return False
    
    async def _generate_support_response(self, message: dict, knowledge_answer: Optional[str], support_type: str, context: dict = None) -> str:
        """Génère une réponse de support appropriée"""
        if knowledge_answer:
            response = f"🔧 **Support - {support_type.title()}**\n\n"
            response += f"{knowledge_answer}\n\n"
            
            # Ajouter des actions suggérées
            response += self._get_suggested_actions(support_type)
            
        else:
            response = f"🔧 **Support - {support_type.title()}**\n\n"
            response += self._get_generic_support_response(support_type)
        
        # Ajouter une note sur l'escalade si nécessaire
        if context.sentiment_score < -0.3:
            response += "\n\n💡 *Si vous avez besoin d'une assistance plus personnalisée, je peux vous transférer vers un conseiller.*"
        
        return response
    
    def _get_suggested_actions(self, support_type: str) -> str:
        """Retourne les actions suggérées selon le type de support"""
        actions = {
            "livraison": "📦 **Actions suggérées :**\n• Vérifiez le statut de votre commande\n• Consultez le numéro de suivi\n• Contactez-nous si le délai est dépassé",
            "retour": "📦 **Actions suggérées :**\n• Connectez-vous à votre espace client\n• Sélectionnez l'article à retourner\n• Imprimez l'étiquette de retour",
            "paiement": "💳 **Actions suggérées :**\n• Vérifiez vos informations bancaires\n• Essayez un autre moyen de paiement\n• Contactez votre banque si nécessaire",
            "compte": "👤 **Actions suggérées :**\n• Utilisez la fonction 'Mot de passe oublié'\n• Vérifiez votre adresse email\n• Créez un nouveau compte si nécessaire",
            "commande": "📋 **Actions suggérées :**\n• Consultez votre espace client\n• Vérifiez l'email de confirmation\n• Contactez-nous avec votre numéro de commande"
        }
        
        return actions.get(support_type, "💡 **Besoin d'aide supplémentaire ?**\nContactez notre équipe support.")
    
    def _get_generic_support_response(self, support_type: str) -> str:
        """Retourne une réponse générique de support"""
        generic_responses = {
            "livraison": "Pour toute question concernant la livraison, vous pouvez :\n• Consulter le suivi de votre commande\n• Vérifier les délais de livraison\n• Nous contacter en cas de problème",
            "retour": "Pour les retours et remboursements :\n• Vous avez 14 jours pour retourner un article\n• Utilisez votre espace client\n• Le remboursement est effectué sous 5-10 jours",
            "paiement": "Pour les questions de paiement :\n• Nous acceptons cartes bancaires, PayPal et Apple Pay\n• Tous les paiements sont sécurisés\n• Contactez-nous en cas de problème",
            "compte": "Pour la gestion de votre compte :\n• Créez un compte gratuitement\n• Modifiez vos informations personnelles\n• Gérez vos préférences de communication",
            "général": "Comment puis-je vous aider ? Je peux vous assister pour :\n• Les commandes et livraisons\n• Les retours et remboursements\n• Les questions de paiement\n• La gestion de votre compte"
        }
        
        return generic_responses.get(support_type, "Je suis là pour vous aider. Pouvez-vous me donner plus de détails sur votre demande ?")
    
    async def log_support_request(self, message: dict, context: dict = None, support_type: str = ""):
        """Enregistre la demande de support pour analyse"""
        try:
            support_log = {
                "timestamp": datetime.now(),
                "user_id": context.user_id,
                "session_id": context.session_id,
                "support_type": support_type,
                "message_content": message.content[:200],
                "sentiment_score": context.sentiment_score,
                "conversation_length": len(context.conversation_history)
            }
            
            # Sauvegarder dans MongoDB
            self.db_manager.mongo_db.support_requests.insert_one(support_log)
            
        except Exception as e:
            logger.error(f"Error logging support request: {e}")
    
    async def get_support_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques de support"""
        try:
            # Statistiques des dernières 24h
            yesterday = datetime.now() - timedelta(days=1)
            
            pipeline = [
                {"$match": {"timestamp": {"$gte": yesterday}}},
                {"$group": {
                    "_id": "$support_type",
                    "count": {"$sum": 1},
                    "avg_sentiment": {"$avg": "$sentiment_score"}
                }},
                {"$sort": {"count": -1}}
            ]
            
            stats = list(self.db_manager.mongo_db.support_requests.aggregate(pipeline))
            
            return {
                "last_24h": {
                    "total_requests": sum(stat["count"] for stat in stats),
                    "by_type": {stat["_id"]: stat["count"] for stat in stats},
                    "avg_sentiment": sum(stat["avg_sentiment"] for stat in stats) / len(stats) if stats else 0
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting support stats: {e}")
            return {}

    async def handle_return_request(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Gérer les demandes de retour de produits"""
        try:
            return {
                "response_text": """
## 🔄 **PROCÉDURE DE RETOUR DE PRODUIT**

### **1. Conditions de Retour**
- ✅ **30 jours** pour retourner un produit
- ✅ **Produit dans son état d'origine**
- ✅ **Emballage complet et accessoires inclus**

### **2. Étapes du Retour**
1. **Connectez-vous** à votre espace client
2. **Allez dans** "Mes Commandes"
3. **Sélectionnez** le produit à retourner
4. **Cliquez sur** "Demander un retour"
5. **Remplissez** le formulaire de retour
6. **Imprimez** l'étiquette de retour

### **3. Remboursement**
- 💳 **Carte bancaire** : 5-7 jours ouvrés
- 🏦 **Virement** : 3-5 jours ouvrés
- 📧 **Email de confirmation** envoyé automatiquement

### **4. Informations Importantes**
- 📦 **Frais de retour** : Gratuits pour les produits défectueux
- 🚚 **Transporteur** : Colis recommandé avec accusé de réception
- 📞 **Support** : Notre équipe est là pour vous aider

**Besoin d'aide supplémentaire ?** Contactez notre support client !
                """,
                "response_type": "return_procedure",
                "escalate": False
            }
        except Exception as e:
            self.logger.error(f"Erreur dans handle_return_request: {str(e)}")
            return {"error": "Erreur lors du traitement de la demande de retour"}

    async def handle_general_return_info(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Gérer les demandes générales sur les retours"""
        try:
            return {
                "response_text": """
## 🔄 **INFORMATIONS SUR LES RETOURS**

### **Politique de Retour**
- **Délai** : 30 jours à compter de la réception
- **Conditions** : Produit non utilisé, emballage intact
- **Frais** : Gratuits pour les produits défectueux

### **Types de Retour**
- **Remboursement** : Remboursement complet
- **Échange** : Remplacement par un produit similaire
- **Crédit boutique** : Bon d'achat valable 1 an

**Pour retourner un produit spécifique, dites-moi lequel !**
                """,
                "response_type": "return_info",
                "escalate": False
            }
        except Exception as e:
            self.logger.error(f"Erreur dans handle_general_return_info: {str(e)}")
            return {"error": "Erreur lors du traitement de la demande"}

    async def handle_general_help(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Gérer les demandes d'aide générales"""
        try:
            return {
                "response_text": """
## 🆘 **COMMENT PUIS-JE VOUS AIDER ?**

### **Services Disponibles**
- 🔍 **Recherche de produits** et recommandations
- 🛒 **Gestion du panier** et commandes
- 📦 **Suivi des livraisons** et retours
- 💳 **Questions de paiement** et facturation
- 👤 **Gestion de compte** et profil

### **Support Spécialisé**
- 📞 **Chat en direct** avec nos conseillers
- 📧 **Email support** : support@fidelobot.com
- 📱 **Téléphone** : 01 23 45 67 89

**Décrivez votre besoin et je vous orienterai vers la bonne solution !**
                """,
                "response_type": "general_help",
                "escalate": False
            }
        except Exception as e:
            self.logger.error(f"Erreur dans handle_general_help: {str(e)}")
            return {"error": "Erreur lors du traitement de la demande"}

    async def handle_delivery_info(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Gérer les demandes sur la livraison"""
        try:
            return {
                "response_text": """
## 📦 **INFORMATIONS SUR LA LIVRAISON**

### **Délais de Livraison**
- **Standard** : 3-5 jours ouvrés
- **Express** : 1-2 jours ouvrés (supplément 9.90€)
- **Point relais** : 2-4 jours ouvrés

### **Frais de Livraison**
- **Gratuit** : À partir de 49€ d'achat
- **Standard** : 4.90€
- **Express** : 9.90€

### **Suivi de Commande**
- **Email de confirmation** avec numéro de suivi
- **SMS** lors de la livraison
- **Espace client** : Suivi en temps réel

**Besoin du suivi d'une commande spécifique ?**
                """,
                "response_type": "delivery_info",
                "escalate": False
            }
        except Exception as e:
            self.logger.error(f"Erreur dans handle_delivery_info: {str(e)}")
            return {"error": "Erreur lors du traitement de la demande"}

    async def handle_payment_info(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Gérer les demandes sur le paiement"""
        try:
            return {
                "response_text": """
## 💳 **INFORMATIONS SUR LE PAIEMENT**

### **Moyens de Paiement Acceptés**
- **Cartes bancaires** : Visa, Mastercard, American Express
- **Paiements numériques** : PayPal, Apple Pay, Google Pay
- **Paiement en plusieurs fois** : 3x ou 4x sans frais

### **Sécurité des Paiements**
- **Chiffrement SSL** 256 bits
- **Certification PCI DSS** niveau 1
- **3D Secure** pour les cartes bancaires

### **Facturation**
- **Facture électronique** envoyée par email
- **TVA incluse** dans tous nos prix
- **Garantie** de remboursement sous 30 jours

**Question spécifique sur le paiement ?**
                """,
                "response_type": "payment_info",
                "escalate": False
            }
        except Exception as e:
            self.logger.error(f"Erreur dans handle_payment_info: {str(e)}")
            return {"error": "Erreur lors du traitement de la demande"} 

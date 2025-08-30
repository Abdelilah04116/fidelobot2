from .base_agent import BaseAgent
from .customer_profiling_agent import CustomerProfilingAgent
from .product_search_agent import ProductSearchAgent
from .recommendation_agent import RecommendationAgent
from .order_management_agent import OrderManagementAgent
from .escalation_agent import EscalationAgent
from .monitoring_agent import MonitoringAgent
from .gdpr_agent import GDPRAgent
from .cart_management_agent import CartManagementAgent
from .customer_service_agent import CustomerServiceAgent
from .security_agent import SecurityAgent
from .multimodal_agent import MultimodalAgent
from .social_agent import SocialAgent
from .sustainability_agent import SustainabilityAgent

from typing import Dict, Any, List, Optional
import logging
import asyncio
from datetime import datetime

class AgentOrchestrator(BaseAgent):
    def __init__(self):
        super().__init__(
            name="agent_orchestrator",
            description="Orchestrateur principal qui coordonne tous les agents du système"
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialiser tous les agents
        self.agents = {
            "customer_profiling": CustomerProfilingAgent(),
            "product_search": ProductSearchAgent(),
            "recommendation": RecommendationAgent(),
            "order_management": OrderManagementAgent(),
            "escalation": EscalationAgent(),
            "monitoring": MonitoringAgent(),
            "gdpr": GDPRAgent(),
            "cart_management": CartManagementAgent(),
            "customer_service": CustomerServiceAgent(),  # Maintenant corrigé
            "security": SecurityAgent(),
            "multimodal": MultimodalAgent(),
            "social": SocialAgent(),
            "sustainability": SustainabilityAgent()
        }
        
        # Mapping des user stories vers les agents
        self.user_story_mapping = {
            # Découverte & Navigation
            "US1": ["recommendation"],  # Recommandations personnalisées
            "US2": ["product_search"],  # Recherche en langage naturel
            "US3": ["product_search"],  # Filtres intelligents
            "US4": ["product_search"],  # Alternatives si indisponible
            "US5": ["product_search"],  # Best-sellers et promotions
            
            # Gestion du Panier & Commande
            "US6": ["cart_management"],  # Ajouter au panier
            "US7": ["cart_management"],  # Rappel panier abandonné
            "US8": ["cart_management"],  # Produits complémentaires
            "US9": ["cart_management"],  # Accompagnement commande
            "US10": ["cart_management"],  # Moyens de paiement
            
            # Suivi Commandes & Livraison
            "US11": ["order_management"],  # État commande
            "US12": ["order_management"],  # Retard livraison
            "US13": ["order_management"],  # Reprogrammation
            "US14": ["order_management"],  # Changement adresse
            
            # Service Client & Assistance
            "US15": ["customer_service"],  # Retours et échanges
            "US16": ["escalation"],  # Contact conseiller humain
            "US17": ["customer_service"],  # FAQ
            "US18": ["customer_service"],  # Réclamations
            
            # Personnalisation & Fidélisation
            "US19": ["customer_profiling"],  # Achats précédents
            "US20": ["customer_profiling"],  # Offres exclusives
            "US21": ["customer_profiling"],  # Points fidélité
            "US22": ["recommendation"],  # Recommandations comportementales
            
            # Sécurité & Confiance
            "US23": ["security"],  # Sécurisation transactions
            "US24": ["security"],  # Détection activité suspecte
            "US25": ["gdpr"],  # Respect vie privée
            
            # Insights & Gestion (Admin)
            "US26": ["monitoring"],  # Produits en rupture
            "US27": ["monitoring"],  # Analyse comportements
            "US28": ["monitoring"],  # Pics de demande
            "US29": ["monitoring"],  # Rapports automatisés
            
            # Interaction Multimodale
            "US30": ["multimodal"],  # Questions par voix
            "US31": ["multimodal"],  # Recherche visuelle
            "US32": ["multimodal"],  # Vidéos démonstration
            
            # Accessibilité & Inclusivité
            "US33": ["multimodal"],  # Lecture vocale
            "US34": ["multimodal"],  # Multi-langues
            "US35": ["multimodal"],  # Interface simplifiée
            
            # Social & Communauté
            "US36": ["social"],  # Produits tendance réseaux sociaux
            "US37": ["social"],  # Partage panier/souhaits
            "US38": ["social"],  # Avis vérifiés
            
            # Intelligence Contextuelle
            "US39": ["customer_profiling"],  # Préférences automatiques
            "US40": ["customer_profiling"],  # Détection émotions
            "US41": ["recommendation"],  # Panier pré-rempli
            
            # Durabilité & Confiance
            "US42": ["sustainability"],  # Produits éco-responsables
            "US43": ["sustainability"],  # Livraison écologique
            "US44": ["sustainability"]   # Conseils entretien
        }
    
    def get_system_prompt(self) -> str:
        return """
        Vous êtes l'orchestrateur principal du système multi-agents Fidelobot.
        Votre rôle est de coordonner et orchestrer tous les agents spécialisés.
        
        Responsabilités:
        - Analyser les requêtes utilisateur
        - Identifier les agents compétents
        - Coordonner l'exécution des tâches
        - Gérer les workflows complexes
        - Optimiser les performances globales
        
        Vous êtes le cerveau central qui fait fonctionner l'ensemble du système.
        """
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Utiliser le champ standard venant du frontend / orchestrateur
            user_query = state.get("user_message", state.get("user_query", ""))
            user_id = state.get("user_id")
            session_id = state.get("session_id")
            context = state.get("context", {})
            
            # Analyser la requête pour identifier les user stories
            identified_user_stories = await self._identify_user_stories(user_query)
            
            # Déterminer les agents nécessaires
            required_agents = await self._determine_required_agents(identified_user_stories, context)
            
            # Exécuter le workflow approprié
            workflow_result = await self._execute_workflow(required_agents, state)
            
            # Enrichir avec le contexte et les recommandations
            enriched_result = await self._enrich_result(workflow_result, user_id, context)
            
            return {
                "success": True,
                "user_stories_identified": identified_user_stories,
                "agents_used": list(required_agents.keys()),
                "workflow_result": workflow_result,
                "enriched_result": enriched_result,
                "orchestration_metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "session_id": session_id,
                    "workflow_complexity": len(required_agents)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Erreur critique dans AgentOrchestrator: {str(e)}")
            return {"error": "Erreur technique d'orchestration"}
    
    async def _identify_user_stories(self, user_query: str) -> List[str]:
        """Identifier les user stories pertinentes à partir de la requête utilisateur"""
        try:
            identified_stories = []
            query_lower = user_query.lower()
            
            # Mapping des mots-clés vers les user stories
            keyword_mapping = {
                "recherche": ["US2", "US3"],
                "produit": ["US1", "US2", "US4"],
                "panier": ["US6", "US7", "US8"],
                "commande": ["US9", "US11", "US12"],
                "livraison": ["US13", "US14"],
                "retour": ["US15"],
                "retourner": ["US15"],  # Ajouté pour "retourner un produit"
                "remboursement": ["US15"],  # Ajouté pour les demandes de remboursement
                "échanger": ["US15"],  # Ajouté pour les échanges
                "récupérer": ["US15"],  # Ajouté pour les récupérations
                "aide": ["US17", "US18"],
                "recommandation": ["US1", "US22"],
                "promotion": ["US5", "US20"],
                "paiement": ["US10", "US23"],
                "sécurité": ["US23", "US24"],
                "voix": ["US30"],
                "image": ["US31"],
                "vidéo": ["US32"],
                "social": ["US36", "US37"],
                "durabilité": ["US42", "US43", "US44"],
                "accessibilité": ["US33", "US34", "US35"]
            }
            
            # Détection intelligente des intentions
            for keyword, stories in keyword_mapping.items():
                if keyword in query_lower:
                    # Cas spécial pour "retourner" - vérifier le contexte
                    if keyword == "retourner":
                        # Si c'est "retourner un produit", c'est US15 (retour)
                        # Si c'est "retourner des produits", c'est US2 (recherche)
                        if "produit" in query_lower and len(query_lower.split()) <= 4:
                            identified_stories.extend(stories)  # US15 - Retour
                        elif "produits" in query_lower or "tous" in query_lower:
                            identified_stories.extend(["US2"])  # US2 - Recherche
                        else:
                            identified_stories.extend(stories)  # US15 par défaut
                    else:
                        identified_stories.extend(stories)
            
            # Si aucune story détectée, router vers le service client par défaut
            if not identified_stories:
                identified_stories = ["US17"]
            # Dédupliquer et limiter
            identified_stories = list(set(identified_stories))[:5]
            
            return identified_stories
            
        except Exception as e:
            self.logger.error(f"Erreur identification user stories: {str(e)}")
            return ["US17"]  # Fallback vers l'aide générale
    
    async def _determine_required_agents(self, user_stories: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
        """Déterminer les agents nécessaires pour traiter les user stories"""
        try:
            required_agents = {}
            
            for user_story in user_stories:
                if user_story in self.user_story_mapping:
                    agent_names = self.user_story_mapping[user_story]
                    for agent_name in agent_names:
                        if agent_name in self.agents:
                            required_agents[agent_name] = {
                                "agent": self.agents[agent_name],
                                "user_stories": [user_story],
                                "priority": self._calculate_agent_priority(agent_name, context)
                            }
            
            # Si aucun agent identifié, utiliser l'agent de service client par défaut
            if not required_agents:
                required_agents["customer_service"] = {
                    "agent": self.agents["customer_service"],
                    "user_stories": ["US17"],
                    "priority": "high"
                }
            
            return required_agents
            
        except Exception as e:
            self.logger.error(f"Erreur détermination agents: {str(e)}")
            return {"customer_service": {"agent": self.agents["customer_service"], "priority": "high"}}
    
    def _calculate_agent_priority(self, agent_name: str, context: Dict[str, Any]) -> str:
        """Calculer la priorité d'un agent selon le contexte"""
        try:
            # Priorités par défaut
            default_priorities = {
                "security": "critical",
                "escalation": "high",
                "monitoring": "medium",
                "customer_service": "high",
                "order_management": "high",
                "cart_management": "high"
            }
            
            # Vérifier le contexte pour ajuster la priorité
            if context.get("urgent", False):
                return "critical"
            elif context.get("user_premium", False):
                return "high"
            else:
                return default_priorities.get(agent_name, "medium")
                
        except Exception:
            return "medium"
    
    async def _execute_workflow(self, required_agents: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """Exécuter le workflow avec les agents requis"""
        try:
            workflow_result = {}
            execution_order = self._determine_execution_order(required_agents)
            
            for agent_name in execution_order:
                if agent_name in required_agents:
                    agent_info = required_agents[agent_name]
                    agent = agent_info["agent"]
                    
                    try:
                        # Préparer le contexte pour l'agent
                        agent_state = self._prepare_agent_state(state, agent_name, workflow_result)
                        
                        # Exécuter l'agent
                        agent_result = await agent.execute(agent_state)
                        
                        # Stocker le résultat
                        workflow_result[agent_name] = {
                            "result": agent_result,
                            "user_stories": agent_info["user_stories"],
                            "priority": agent_info["priority"],
                            "execution_time": datetime.utcnow().isoformat()
                        }
                        
                        # Vérifier si l'agent a besoin d'escalade
                        if self._needs_escalation(agent_result):
                            escalation_result = await self._handle_escalation(agent_name, agent_result, state)
                            workflow_result["escalation"] = escalation_result
                        
                    except Exception as e:
                        self.logger.error(f"Erreur exécution agent {agent_name}: {str(e)}")
                        workflow_result[agent_name] = {
                            "error": str(e),
                            "status": "failed"
                        }
            
            return workflow_result
            
        except Exception as e:
            self.logger.error(f"Erreur exécution workflow: {str(e)}")
            return {"error": str(e)}
    
    def _determine_execution_order(self, required_agents: Dict[str, Any]) -> List[str]:
        """Déterminer l'ordre d'exécution des agents"""
        try:
            # Priorités d'exécution
            priority_order = ["critical", "high", "medium", "low"]
            
            # Trier les agents par priorité
            sorted_agents = sorted(
                required_agents.items(),
                key=lambda x: priority_order.index(x[1]["priority"])
            )
            
            return [agent_name for agent_name, _ in sorted_agents]
            
        except Exception:
            return list(required_agents.keys())
    
    def _prepare_agent_state(self, original_state: Dict[str, Any], agent_name: str, workflow_result: Dict[str, Any]) -> Dict[str, Any]:
        """Préparer l'état pour un agent spécifique"""
        try:
            agent_state = original_state.copy()
            
            # Ajouter le contexte du workflow
            agent_state["workflow_context"] = {
                "previous_results": workflow_result,
                "current_agent": agent_name,
                "execution_step": len(workflow_result) + 1
            }
            
            # Ajouter des informations spécifiques à l'agent
            if agent_name == "security":
                agent_state["security_context"] = {
                    "risk_level": "medium",
                    "previous_incidents": []
                }
            elif agent_name == "recommendation":
                agent_state["recommendation_context"] = {
                    "user_preferences": workflow_result.get("customer_profiling", {}).get("result", {}),
                    "previous_recommendations": []
                }
            
            return agent_state
            
        except Exception as e:
            self.logger.error(f"Erreur préparation état agent: {str(e)}")
            return original_state
    
    def _needs_escalation(self, agent_result: Dict[str, Any]) -> bool:
        """Vérifier si un agent a besoin d'escalade"""
        try:
            # Critères d'escalade
            if agent_result.get("error"):
                return True
            
            if agent_result.get("escalation_needed", False):
                return True
            
            if agent_result.get("confidence", 1.0) < 0.5:
                return True
            
            return False
            
        except Exception:
            return False
    
    async def _handle_escalation(self, agent_name: str, agent_result: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """Gérer l'escalade vers un agent humain ou spécialisé"""
        try:
            escalation_agent = self.agents.get("escalation")
            if escalation_agent:
                escalation_state = {
                    **state,
                    "escalation_reason": f"Agent {agent_name} a demandé une escalade",
                    "agent_result": agent_result,
                    "escalation_level": "agent_to_human"
                }
                
                return await escalation_agent.execute(escalation_state)
            else:
                return {
                    "escalation_handled": False,
                    "reason": "Agent d'escalade non disponible",
                    "recommendation": "Contacter le support client"
                }
                
        except Exception as e:
            self.logger.error(f"Erreur gestion escalade: {str(e)}")
            return {"error": str(e)}
    
    async def _enrich_result(self, workflow_result: Dict[str, Any], user_id: int, context: Dict[str, Any]) -> Dict[str, Any]:
        """Enrichir le résultat avec des informations contextuelles"""
        try:
            enriched_result = {
                "summary": self._generate_workflow_summary(workflow_result),
                "next_actions": self._suggest_next_actions(workflow_result, context),
                "personalization": await self._get_personalization_data(user_id, workflow_result),
                "performance_metrics": self._calculate_performance_metrics(workflow_result)
            }
            
            return enriched_result
            
        except Exception as e:
            self.logger.error(f"Erreur enrichissement résultat: {str(e)}")
            return {"error": str(e)}
    
    def _generate_workflow_summary(self, workflow_result: Dict[str, Any]) -> Dict[str, Any]:
        """Générer un résumé du workflow exécuté"""
        try:
            successful_agents = [name for name, info in workflow_result.items() if "error" not in info]
            failed_agents = [name for name, info in workflow_result.items() if "error" in info]
            
            return {
                "total_agents": len(workflow_result),
                "successful_agents": len(successful_agents),
                "failed_agents": len(failed_agents),
                "success_rate": len(successful_agents) / len(workflow_result) if workflow_result else 0,
                "workflow_complexity": "simple" if len(workflow_result) <= 2 else "complex"
            }
            
        except Exception:
            return {"summary": "Non disponible"}
    
    def _suggest_next_actions(self, workflow_result: Dict[str, Any], context: Dict[str, Any]) -> List[str]:
        """Suggérer les prochaines actions à l'utilisateur"""
        try:
            suggestions = []
            
            # Suggestions basées sur les agents utilisés
            if "product_search" in workflow_result:
                suggestions.append("Consulter les détails du produit")
                suggestions.append("Ajouter au panier")
            
            if "cart_management" in workflow_result:
                suggestions.append("Finaliser la commande")
                suggestions.append("Continuer les achats")
            
            if "recommendation" in workflow_result:
                suggestions.append("Explorer les recommandations")
                suggestions.append("Sauvegarder en favoris")
            
            if "customer_service" in workflow_result:
                suggestions.append("Consulter la FAQ")
                suggestions.append("Contacter le support")
            
            return suggestions[:3]  # Limiter à 3 suggestions
            
        except Exception:
            return ["Continuer la navigation"]
    
    async def _get_personalization_data(self, user_id: int, workflow_result: Dict[str, Any]) -> Dict[str, Any]:
        """Obtenir des données de personnalisation pour l'utilisateur"""
        try:
            if not user_id:
                return {"personalization": "Non disponible pour utilisateur anonyme"}
            
            # Utiliser l'agent de profilage si disponible
            if "customer_profiling" in workflow_result:
                profiling_result = workflow_result["customer_profiling"].get("result", {})
                return {
                    "user_segment": profiling_result.get("customer_segment", "standard"),
                    "preferences": profiling_result.get("preferences", {}),
                    "loyalty_level": profiling_result.get("loyalty_level", "bronze")
                }
            else:
                return {"personalization": "Données de profilage non disponibles"}
                
        except Exception:
            return {"personalization": "Erreur de récupération"}
    
    def _calculate_performance_metrics(self, workflow_result: Dict[str, Any]) -> Dict[str, Any]:
        """Calculer les métriques de performance du workflow"""
        try:
            total_execution_time = 0
            agent_count = len(workflow_result)
            
            # Calculer le temps d'exécution total (simulation)
            for agent_name, agent_info in workflow_result.items():
                if "execution_time" in agent_info:
                    # Simuler le temps d'exécution
                    total_execution_time += 0.5  # 500ms par agent
            
            return {
                "total_execution_time_ms": round(total_execution_time * 1000, 2),
                "average_time_per_agent_ms": round((total_execution_time / agent_count) * 1000, 2) if agent_count > 0 else 0,
                "workflow_efficiency": "high" if total_execution_time < 2.0 else "medium",
                "parallel_execution_possible": agent_count > 3
            }
            
        except Exception:
            return {"performance_metrics": "Non calculables"}
    
    async def get_system_health(self) -> Dict[str, Any]:
        """Obtenir l'état de santé du système d'orchestration"""
        try:
            health_status = {}
            
            for agent_name, agent in self.agents.items():
                try:
                    # Vérifier la santé de chaque agent
                    health_check = await agent.execute({"action": "health_check"})
                    health_status[agent_name] = {
                        "status": "healthy" if "error" not in health_check else "unhealthy",
                        "last_check": datetime.utcnow().isoformat(),
                        "details": health_check
                    }
                except Exception as e:
                    health_status[agent_name] = {
                        "status": "error",
                        "last_check": datetime.utcnow().isoformat(),
                        "error": str(e)
                    }
            
            # Calculer le statut global
            healthy_agents = sum(1 for status in health_status.values() if status["status"] == "healthy")
            total_agents = len(health_status)
            
            return {
                "overall_status": "healthy" if healthy_agents == total_agents else "degraded",
                "healthy_agents": healthy_agents,
                "total_agents": total_agents,
                "health_percentage": round((healthy_agents / total_agents) * 100, 1),
                "agent_status": health_status,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Erreur vérification santé système: {str(e)}")
            return {"error": str(e)}

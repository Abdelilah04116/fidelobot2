from .base_agent import BaseAgent
from typing import Dict, Any, List, Optional
import asyncio
import time
import logging
from datetime import datetime, timedelta
from ..models.database import SessionLocal, Message, Conversation
from sqlalchemy import func
import json
import os

class MonitoringAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="monitoring_agent",
            description="Agent de surveillance et monitoring du système optimisé"
        )
        self.logger = logging.getLogger(__name__)
        self.metrics_cache = {}
        self.cache_ttl = 300  # 5 minutes
        
        # Configuration Redis avec fallback
        self.redis_client = None
        self._init_redis()
        
        # Vérifier les dépendances système
        self._check_system_dependencies()
    
    def _init_redis(self):
        """Initialiser la connexion Redis avec gestion d'erreur"""
        try:
            redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
            import redis
            self.redis_client = redis.Redis.from_url(redis_url, decode_responses=True)
            # Test de connexion
            self.redis_client.ping()
            self.logger.info("Connexion Redis établie avec succès")
        except Exception as e:
            self.logger.warning(f"Impossible de se connecter à Redis: {str(e)}. Monitoring limité.")
            self.redis_client = None
    
    def _check_system_dependencies(self):
        """Vérifier les dépendances système disponibles"""
        self.psutil_available = False
        try:
            import psutil
            self.psutil_available = True
        except ImportError:
            self.logger.warning("psutil non disponible. Métriques système limitées.")
    
    def get_system_prompt(self) -> str:
        return """
        Vous êtes un agent de surveillance système pour le chatbot e-commerce.
        Votre rôle est de monitorer les performances, détecter les anomalies et générer des alertes.
        
        Métriques surveillées:
        - Performance des agents
        - Temps de réponse
        - Taux d'erreur
        - Utilisation des ressources
        - Satisfaction utilisateur
        - Disponibilité du service
        """
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        # Exemple de réponse dynamique
        state["response_text"] = "Le système de monitoring est opérationnel. Toutes les métriques sont surveillées en temps réel."
        return state
    
    async def perform_health_check(self) -> Dict[str, Any]:
        """Vérification de l'état de santé du système"""
        try:
            health_status = {
                "timestamp": datetime.utcnow().isoformat(),
                "overall_status": "healthy",
                "components": {}
            }
            
            # Vérifier la base de données
            db_status = await self._check_database_health()
            health_status["components"]["database"] = db_status
            
            if db_status["status"] != "healthy":
                health_status["overall_status"] = "degraded"
            
            # Vérifier Redis
            redis_status = await self._check_redis_health()
            health_status["components"]["redis"] = redis_status
            
            if redis_status["status"] != "healthy":
                health_status["overall_status"] = "degraded"
            
            # Vérifier les ressources système
            system_status = await self._check_system_health()
            health_status["components"]["system"] = system_status
            
            # Déterminer le statut global
            if system_status.get("status") == "critical":
                health_status["overall_status"] = "critical"
            elif health_status["overall_status"] != "critical":
                health_status["overall_status"] = "healthy"
            
            return health_status
            
        except Exception as e:
            self.logger.error(f"Erreur vérification santé: {str(e)}")
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "overall_status": "unknown",
                "error": str(e)
            }
    
    async def _check_database_health(self) -> Dict[str, Any]:
        """Vérifier la santé de la base de données"""
        try:
            db = SessionLocal()
            start_time = time.time()
            db.execute("SELECT 1")
            response_time = (time.time() - start_time) * 1000  # en ms
            db.close()
            
            return {
                "status": "healthy",
                "response_time_ms": round(response_time, 2),
                "last_check": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "last_check": datetime.utcnow().isoformat()
            }
    
    async def _check_redis_health(self) -> Dict[str, Any]:
        """Vérifier la santé de Redis"""
        if not self.redis_client:
            return {
                "status": "unavailable",
                "error": "Client Redis non initialisé",
                "last_check": datetime.utcnow().isoformat()
            }
        
        try:
            start_time = time.time()
            self.redis_client.ping()
            response_time = (time.time() - start_time) * 1000
            
            return {
                "status": "healthy",
                "response_time_ms": round(response_time, 2),
                "last_check": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "last_check": datetime.utcnow().isoformat()
            }
    
    async def _check_system_health(self) -> Dict[str, Any]:
        """Vérifier la santé du système"""
        if not self.psutil_available:
            return {
                "status": "unavailable",
                "error": "psutil non disponible",
                "last_check": datetime.utcnow().isoformat()
            }
        
        try:
            import psutil
            
            # Métriques système non-bloquantes
            cpu_percent = psutil.cpu_percent(interval=0.1)  # Réduire l'intervalle
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Déterminer le statut
            status = "healthy"
            if cpu_percent > 90 or memory.percent > 90 or disk.percent > 95:
                status = "critical"
            elif cpu_percent > 80 or memory.percent > 80 or disk.percent > 90:
                status = "warning"
            
            return {
                "status": status,
                "cpu_percent": round(cpu_percent, 1),
                "memory_percent": round(memory.percent, 1),
                "disk_percent": round(disk.percent, 1),
                "load_average": round(psutil.getloadavg()[0], 2) if hasattr(psutil, 'getloadavg') else 0,
                "last_check": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "last_check": datetime.utcnow().isoformat()
            }
    
    async def get_performance_metrics(self) -> Dict[str, Any]:
        """Récupérer les métriques de performance"""
        # Vérifier le cache
        cache_key = f"performance_metrics_{datetime.utcnow().strftime('%Y%m%d_%H')}"
        if cache_key in self.metrics_cache:
            cache_time, cached_data = self.metrics_cache[cache_key]
            if time.time() - cache_time < self.cache_ttl:
                return cached_data
        
        db = SessionLocal()
        try:
            # Métriques des dernières 24h
            since = datetime.utcnow() - timedelta(hours=24)
            
            # Nombre total de conversations
            total_conversations = db.query(Conversation).filter(
                Conversation.started_at >= since
            ).count()
            
            # Nombre total de messages
            total_messages = db.query(Message).filter(
                Message.timestamp >= since
            ).count()
            
            # Temps de réponse moyen (avec gestion d'erreur)
            avg_response_time = 0
            try:
                avg_response_time = db.query(
                    func.avg(Message.metadata["processing_time"].astext.cast(float))
                ).filter(
                    Message.sender_type == "bot",
                    Message.timestamp >= since,
                    Message.metadata.has_key("processing_time")
                ).scalar() or 0
            except Exception as e:
                self.logger.warning(f"Erreur calcul temps de réponse: {str(e)}")
            
            # Taux d'escalade
            escalated_conversations = db.query(Conversation).filter(
                Conversation.started_at >= since,
                Conversation.status == "escalated"
            ).count()
            
            escalation_rate = (escalated_conversations / max(1, total_conversations)) * 100
            
            # Intents les plus fréquents
            intent_stats = []
            try:
                intent_stats = db.query(
                    Message.intent,
                    func.count(Message.intent)
                ).filter(
                    Message.timestamp >= since,
                    Message.sender_type == "user"
                ).group_by(Message.intent).all()
            except Exception as e:
                self.logger.warning(f"Erreur statistiques intents: {str(e)}")
            
            # Agents les plus utilisés
            agent_stats = {}
            try:
                messages_with_agents = db.query(Message).filter(
                    Message.timestamp >= since,
                    Message.sender_type == "bot",
                    Message.agent_used.isnot(None)
                ).all()
                
                for message in messages_with_agents:
                    if message.agent_used:
                        agents = message.agent_used.split(",")
                        for agent in agents:
                            agent = agent.strip()
                            agent_stats[agent] = agent_stats.get(agent, 0) + 1
            except Exception as e:
                self.logger.warning(f"Erreur statistiques agents: {str(e)}")
            
            metrics = {
                "period": "24h",
                "total_conversations": total_conversations,
                "total_messages": total_messages,
                "average_response_time": round(avg_response_time, 2),
                "escalation_rate": round(escalation_rate, 2),
                "top_intents": dict(intent_stats[:10]),
                "agent_usage": dict(sorted(agent_stats.items(), key=lambda x: x[1], reverse=True)[:10]),
                "messages_per_conversation": round(total_messages / max(1, total_conversations), 2),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Mettre en cache
            self.metrics_cache[cache_key] = (time.time(), metrics)
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Erreur métriques performance: {str(e)}")
            return {"error": str(e)}
        finally:
            db.close()
    
    async def check_alerts(self) -> Dict[str, Any]:
        """Vérifier les conditions d'alerte"""
        try:
            alerts = []
            
            # Récupérer les métriques actuelles
            health = await self.perform_health_check()
            performance = await self.get_performance_metrics()
            
            if performance.get("error"):
                alerts.append({
                    "level": "warning",
                    "type": "monitoring",
                    "message": "Impossible de récupérer les métriques de performance",
                    "details": performance["error"]
                })
            else:
                # Alerte temps de réponse élevé
                if performance["average_response_time"] > 5.0:
                    alerts.append({
                        "level": "warning",
                        "type": "performance",
                        "message": f"Temps de réponse élevé: {performance['average_response_time']}s",
                        "threshold": 5.0
                    })
                
                # Alerte taux d'escalade élevé
                if performance["escalation_rate"] > 20:
                    alerts.append({
                        "level": "warning",
                        "type": "escalation",
                        "message": f"Taux d'escalade élevé: {performance['escalation_rate']}%",
                        "threshold": 20
                    })
                
                # Alerte faible activité
                if performance["total_conversations"] < 10:
                    alerts.append({
                        "level": "info",
                        "type": "activity",
                        "message": "Faible activité détectée",
                        "conversations_24h": performance["total_conversations"]
                    })
            
            # Alertes de santé système
            if health.get("overall_status") == "critical":
                alerts.append({
                    "level": "critical",
                    "type": "system_health",
                    "message": "Ressources système critiques",
                    "details": health.get("components", {}).get("system", {})
                })
            
            return {
                "alert_count": len(alerts),
                "alerts": alerts,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Erreur vérification alertes: {str(e)}")
            return {"error": str(e), "alerts": []}
    
    async def analyze_user_satisfaction(self) -> Dict[str, Any]:
        """Analyser la satisfaction utilisateur"""
        db = SessionLocal()
        try:
            # Analyser les patterns de conversation
            since = datetime.utcnow() - timedelta(hours=24)
            
            # Conversations courtes (potentiellement insatisfaisantes)
            short_conversations = db.query(Conversation).filter(
                Conversation.started_at >= since
            ).all()
            
            short_conv_count = 0
            for conv in short_conversations:
                try:
                    message_count = len(conv.messages) if hasattr(conv, 'messages') else 0
                    if message_count <= 2:  # Très courte conversation
                        short_conv_count += 1
                except Exception as e:
                    self.logger.warning(f"Erreur analyse conversation {getattr(conv, 'id', 'unknown')}: {str(e)}")
                    continue
            
            short_conv_rate = (short_conv_count / max(1, len(short_conversations))) * 100
            
            # Messages d'erreur ou d'incompréhension
            error_messages = 0
            total_bot_messages = 0
            
            try:
                error_messages = db.query(Message).filter(
                    Message.timestamp >= since,
                    Message.sender_type == "bot",
                    Message.content.ilike("%désolé%") |
                    Message.content.ilike("%erreur%") |
                    Message.content.ilike("%ne comprends pas%")
                ).count()
                
                total_bot_messages = db.query(Message).filter(
                    Message.timestamp >= since,
                    Message.sender_type == "bot"
                ).count()
            except Exception as e:
                self.logger.warning(f"Erreur analyse messages: {str(e)}")
            
            error_rate = (error_messages / max(1, total_bot_messages)) * 100
            
            # Score de satisfaction estimé
            satisfaction_score = 100 - (short_conv_rate * 0.3) - (error_rate * 0.7)
            satisfaction_score = max(0, min(100, satisfaction_score))
            
            return {
                "satisfaction_score": round(satisfaction_score, 1),
                "short_conversation_rate": round(short_conv_rate, 1),
                "error_message_rate": round(error_rate, 1),
                "total_conversations_analyzed": len(short_conversations),
                "recommendations": await self._generate_satisfaction_recommendations(
                    satisfaction_score, short_conv_rate, error_rate
                ),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Erreur analyse satisfaction: {str(e)}")
            return {"error": str(e)}
        finally:
            db.close()
    
    async def _generate_satisfaction_recommendations(self, score: float, short_rate: float, error_rate: float) -> List[str]:
        """Générer des recommandations d'amélioration"""
        recommendations = []
        
        if score < 70:
            recommendations.append("Score de satisfaction faible - révision générale nécessaire")
        
        if short_rate > 30:
            recommendations.append("Taux élevé de conversations courtes - améliorer l'engagement initial")
        
        if error_rate > 15:
            recommendations.append("Taux d'erreur élevé - améliorer la compréhension NLP")
        
        if not recommendations:
            recommendations.append("Performances satisfaisantes - continuer le monitoring")
        
        return recommendations
    
    async def clear_cache(self) -> Dict[str, Any]:
        """Vider le cache des métriques"""
        try:
            cache_size = len(self.metrics_cache)
            self.metrics_cache.clear()
            return {
                "success": True,
                "cache_cleared": True,
                "items_removed": cache_size,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def get_cache_status(self) -> Dict[str, Any]:
        """Obtenir le statut du cache"""
        try:
            current_time = time.time()
            active_items = 0
            expired_items = 0
            
            for cache_time, _ in self.metrics_cache.values():
                if current_time - cache_time < self.cache_ttl:
                    active_items += 1
                else:
                    expired_items += 1
            
            return {
                "total_items": len(self.metrics_cache),
                "active_items": active_items,
                "expired_items": expired_items,
                "cache_ttl_seconds": self.cache_ttl,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}

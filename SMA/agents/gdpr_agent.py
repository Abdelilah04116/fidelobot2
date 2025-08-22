
from .base_agent import BaseAgent
from typing import Dict, Any, List
import hashlib
import json
from datetime import datetime, timedelta
from ..models.database import SessionLocal, User, Message, Conversation

class GDPRAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="gdpr_agent",
            description="Agent de conformité RGPD et protection des données"
        )
    
    def get_system_prompt(self) -> str:
        return """
        Vous êtes un agent spécialisé dans la conformité RGPD et la protection des données.
        Votre rôle est de garantir le respect de la vie privée et des droits des utilisateurs.
        
        Responsabilités:
        - Anonymisation des données sensibles
        - Gestion des demandes de suppression
        - Audit des données stockées
        - Filtrage des informations personnelles
        - Respect du droit à l'oubli
        - Chiffrement des communications
        """
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        # Exemple de réponse dynamique
        state["response_text"] = "Votre demande RGPD est prise en compte. Vous pouvez demander l'accès, la portabilité ou la suppression de vos données."
        return state
    
    async def anonymize_data(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Anonymiser les données utilisateur"""
        data_to_anonymize = state.get("data", {})
        anonymization_level = state.get("level", "partial")  # partial, full
        
        anonymized_data = {}
        
        for key, value in data_to_anonymize.items():
            if self._is_sensitive_field(key):
                if anonymization_level == "full":
                    anonymized_data[key] = self._full_anonymize(value)
                else:
                    anonymized_data[key] = self._partial_anonymize(value)
            else:
                anonymized_data[key] = value
        
        return {
            "anonymized_data": anonymized_data,
            "fields_anonymized": [k for k in data_to_anonymize.keys() if self._is_sensitive_field(k)],
            "anonymization_level": anonymization_level
        }
    
    async def delete_user_data(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Supprimer toutes les données d'un utilisateur (droit à l'oubli)"""
        user_id = state.get("user_id")
        
        if not user_id:
            return {"error": "ID utilisateur requis"}
        
        db = SessionLocal()
        try:
            # Compter les données avant suppression
            conversations_count = db.query(Conversation).filter(Conversation.user_id == user_id).count()
            messages_count = db.query(Message).join(Conversation).filter(Conversation.user_id == user_id).count()
            
            # Supprimer les messages
            messages_deleted = db.query(Message).join(Conversation).filter(
                Conversation.user_id == user_id
            ).delete(synchronize_session=False)
            
            # Supprimer les conversations
            conversations_deleted = db.query(Conversation).filter(
                Conversation.user_id == user_id
            ).delete()
            
            # Anonymiser l'utilisateur plutôt que le supprimer (pour préserver l'intégrité référentielle)
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                user.email = f"deleted_user_{user_id}@anonymized.com"
                user.username = f"deleted_user_{user_id}"
                user.hashed_password = "DELETED"
                user.is_active = False
                user.preferences = {}
            
            db.commit()
            
            return {
                "success": True,
                "user_anonymized": True,
                "conversations_deleted": conversations_deleted,
                "messages_deleted": messages_deleted,
                "deletion_timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            db.rollback()
            return {"error": f"Erreur lors de la suppression: {str(e)}"}
        finally:
            db.close()
    
    async def export_user_data(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Exporter toutes les données d'un utilisateur (droit d'accès)"""
        user_id = state.get("user_id")
        
        if not user_id:
            return {"error": "ID utilisateur requis"}
        
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return {"error": "Utilisateur non trouvé"}
            
            # Données utilisateur
            user_data = {
                "user_info": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "created_at": user.created_at.isoformat(),
                    "is_vip": user.is_vip,
                    "preferences": user.preferences
                }
            }
            
            # Conversations
            conversations = db.query(Conversation).filter(Conversation.user_id == user_id).all()
            user_data["conversations"] = []
            
            for conv in conversations:
                conv_data = {
                    "id": conv.id,
                    "session_id": conv.session_id,
                    "started_at": conv.started_at.isoformat(),
                    "ended_at": conv.ended_at.isoformat() if conv.ended_at else None,
                    "status": conv.status,
                    "messages": []
                }
                
                for message in conv.messages:
                    conv_data["messages"].append({
                        "id": message.id,
                        "sender_type": message.sender_type,
                        "content": message.content,
                        "intent": message.intent,
                        "timestamp": message.timestamp.isoformat(),
                        "agent_used": message.agent_used
                    })
                
                user_data["conversations"].append(conv_data)
            
            # Commandes (si applicable)
            from ..models.database import Order
            orders = db.query(Order).filter(Order.user_id == user_id).all()
            user_data["orders"] = []
            
            for order in orders:
                order_data = {
                    "id": order.id,
                    "total_amount": order.total_amount,
                    "status": order.status,
                    "created_at": order.created_at.isoformat(),
                    "items": []
                }
                
                for item in order.items:
                    order_data["items"].append({
                        "product_name": item.product.name,
                        "quantity": item.quantity,
                        "price": item.price
                    })
                
                user_data["orders"].append(order_data)
            
            return {
                "success": True,
                "user_data": user_data,
                "export_timestamp": datetime.utcnow().isoformat(),
                "total_conversations": len(user_data["conversations"]),
                "total_orders": len(user_data["orders"])
            }
            
        finally:
            db.close()
    
    async def audit_stored_data(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Auditer les données stockées pour la conformité RGPD"""
        db = SessionLocal()
        try:
            # Statistiques générales
            total_users = db.query(User).count()
            active_users = db.query(User).filter(User.is_active == True).count()
            total_conversations = db.query(Conversation).count()
            total_messages = db.query(Message).count()
            
            # Données anciennes (> 2 ans)
            cutoff_date = datetime.utcnow() - timedelta(days=730)
            old_conversations = db.query(Conversation).filter(
                Conversation.started_at < cutoff_date
            ).count()
            
            # Messages contenant potentiellement des données sensibles
            sensitive_patterns = ['email', 'telephone', 'adresse', 'carte', 'iban']
            potentially_sensitive_messages = 0
            
            messages = db.query(Message).filter(Message.sender_type == "user").all()
            for message in messages:
                content_lower = message.content.lower()
                if any(pattern in content_lower for pattern in sensitive_patterns):
                    potentially_sensitive_messages += 1
            
            # Utilisateurs inactifs depuis longtemps
            inactive_cutoff = datetime.utcnow() - timedelta(days=365)
            potentially_inactive_users = db.query(User).filter(
                User.created_at < inactive_cutoff,
                User.is_active == True
            ).count()
            
            # Recommandations de conformité
            recommendations = []
            
            if old_conversations > 0:
                recommendations.append(f"Examiner {old_conversations} conversations anciennes pour archivage/suppression")
            
            if potentially_sensitive_messages > total_messages * 0.1:
                recommendations.append("Taux élevé de messages potentiellement sensibles - réviser les filtres")
            
            if potentially_inactive_users > 0:
                recommendations.append(f"Contacter {potentially_inactive_users} utilisateurs inactifs pour confirmation")
            
            return {
                "audit_timestamp": datetime.utcnow().isoformat(),
                "statistics": {
                    "total_users": total_users,
                    "active_users": active_users,
                    "total_conversations": total_conversations,
                    "total_messages": total_messages,
                    "old_conversations": old_conversations,
                    "potentially_sensitive_messages": potentially_sensitive_messages,
                    "potentially_inactive_users": potentially_inactive_users
                },
                "compliance_score": self._calculate_compliance_score({
                    "old_data_ratio": old_conversations / max(1, total_conversations),
                    "sensitive_ratio": potentially_sensitive_messages / max(1, total_messages),
                    "inactive_ratio": potentially_inactive_users / max(1, total_users)
                }),
                "recommendations": recommendations
            }
            
        finally:
            db.close()
    
    async def filter_sensitive_content(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Filtrer et masquer le contenu sensible dans les messages"""
        content = state.get("content", "")
        filter_level = state.get("filter_level", "moderate")  # low, moderate, high
        
        filtered_content = content
        detected_patterns = []
        
        # Patterns de données sensibles
        sensitive_patterns = {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phone": r'\b(?:\+33|0)[1-9](?:[0-9]{8})\b',
            "credit_card": r'\b(?:[0-9]{4}[-\s]?){3}[0-9]{4}\b',
            "iban": r'\b[A-Z]{2}[0-9]{2}[A-Z0-9]{4}[0-9]{7}([A-Z0-9]?){0,16}\b'
        }
        
        import re
        
        for pattern_name, pattern in sensitive_patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                detected_patterns.append(pattern_name)
                
                # Remplacer selon le niveau de filtrage
                if filter_level == "high":
                    filtered_content = re.sub(pattern, "[DONNÉES SUPPRIMÉES]", filtered_content, flags=re.IGNORECASE)
                elif filter_level == "moderate":
                    filtered_content = re.sub(pattern, "[***]", filtered_content, flags=re.IGNORECASE)
                else:  # low
                    filtered_content = re.sub(pattern, lambda m: m.group()[:2] + "*" * (len(m.group()) - 4) + m.group()[-2:], filtered_content, flags=re.IGNORECASE)
        
        return {
            "original_content": content,
            "filtered_content": filtered_content,
            "detected_patterns": detected_patterns,
            "filter_level": filter_level,
            "content_modified": content != filtered_content
        }
    
    def _is_sensitive_field(self, field_name: str) -> bool:
        """Vérifier si un champ contient des données sensibles"""
        sensitive_fields = [
            'email', 'phone', 'address', 'credit_card', 'iban', 
            'password', 'ssn', 'birthdate', 'full_name'
        ]
        return field_name.lower() in sensitive_fields
    
    def _partial_anonymize(self, value: str) -> str:
        """Anonymisation partielle (masquer une partie)"""
        if len(value) <= 4:
            return "*" * len(value)
        return value[:2] + "*" * (len(value) - 4) + value[-2:]
    
    def _full_anonymize(self, value: str) -> str:
        """Anonymisation complète (hash)"""
        return hashlib.sha256(value.encode()).hexdigest()[:8]
    
    def _calculate_compliance_score(self, metrics: Dict[str, float]) -> float:
        """Calculer un score de conformité RGPD"""
        # Score basé sur les métriques de conformité
        score = 100
        
        # Pénaliser les données anciennes
        score -= metrics["old_data_ratio"] * 30
        
        # Pénaliser les données sensibles non filtrées
        score -= metrics["sensitive_ratio"] * 40
        
        # Pénaliser les utilisateurs inactifs
        score -= metrics["inactive_ratio"] * 20
        
        return max(0, min(100, round(score, 1)))

from .base_agent import BaseAgent
from typing import Dict, Any, List, Optional
from ..models.database import SessionLocal, User, Order, Message
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
import logging
from datetime import datetime, timedelta
import hashlib
import re

class SecurityAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="security_agent",
            description="Agent spécialisé dans la sécurité et la protection des données"
        )
        self.logger = logging.getLogger(__name__)
        
        # Patterns de détection d'activité suspecte
        self.suspicious_patterns = {
            "multiple_failed_logins": {"threshold": 5, "time_window": 300},  # 5 échecs en 5 min
            "unusual_payment_activity": {"threshold": 3, "time_window": 3600},  # 3 paiements en 1h
            "suspicious_ip": {"threshold": 2, "time_window": 86400},  # 2 connexions depuis IP suspecte en 24h
            "data_breach_attempt": {"keywords": ["password", "admin", "root", "hack"]},
            "unusual_order_patterns": {"threshold": 5, "time_window": 3600}  # 5 commandes en 1h
        }
    
    def get_system_prompt(self) -> str:
        return """
        Vous êtes un expert en sécurité e-commerce.
        Votre rôle est de protéger les utilisateurs et le système contre les menaces.
        
        Responsabilités:
        - Détecter les activités suspectes
        - Sécuriser les transactions
        - Protéger les données personnelles
        - Notifier les utilisateurs des risques
        - Bloquer les tentatives d'intrusion
        
        Soyez toujours vigilant et réactif aux menaces.
        """
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Exemple de réponse dynamique
            state["response_text"] = "Vos données sont protégées grâce à des protocoles de sécurité avancés et un chiffrement de bout en bout."
            return state
        except Exception as e:
            self.logger.error(f"Erreur critique dans SecurityAgent: {str(e)}")
            return {"error": "Erreur technique de sécurité"}
    
    async def perform_security_check_safe(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Effectuer une vérification de sécurité complète"""
        try:
            user_id = state.get("user_id")
            session_id = state.get("session_id")
            ip_address = state.get("ip_address", "")
            user_agent = state.get("user_agent", "")
            
            security_checks = {
                "session_validity": await self._check_session_validity(session_id),
                "ip_reputation": await self._check_ip_reputation(ip_address),
                "user_agent_analysis": await self._analyze_user_agent(user_agent),
                "account_activity": await self._check_account_activity(user_id),
                "transaction_history": await self._check_transaction_history(user_id)
            }
            
            # Calculer le score de sécurité global
            security_score = self._calculate_security_score(security_checks)
            
            # Déterminer le niveau de risque
            risk_level = "low"
            if security_score < 50:
                risk_level = "high"
            elif security_score < 75:
                risk_level = "medium"
            
            return {
                "security_score": security_score,
                "risk_level": risk_level,
                "checks": security_checks,
                "recommendations": self._generate_security_recommendations(security_checks),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Erreur vérification sécurité: {str(e)}")
            return {"error": str(e)}
    
    async def _check_session_validity(self, session_id: str) -> Dict[str, Any]:
        """Vérifier la validité de la session"""
        try:
            if not session_id:
                return {"valid": False, "reason": "Session ID manquant"}
            
            # Vérifier l'âge de la session (exemple: 24h max)
            # En production, cette logique serait dans la base de données
            return {
                "valid": True,
                "age_hours": 2,  # Exemple
                "max_age_hours": 24,
                "expires_at": (datetime.utcnow() + timedelta(hours=22)).isoformat()
            }
        except Exception:
            return {"valid": False, "reason": "Erreur de vérification"}
    
    async def _check_ip_reputation(self, ip_address: str) -> Dict[str, Any]:
        """Vérifier la réputation de l'IP"""
        try:
            if not ip_address:
                return {"reputation": "unknown", "risk": "medium"}
            
            # Liste d'IPs suspectes (en production, utiliser un service externe)
            suspicious_ips = [
                "192.168.1.100",  # Exemple d'IP locale suspecte
                "10.0.0.50"       # Exemple d'IP privée suspecte
            ]
            
            if ip_address in suspicious_ips:
                return {"reputation": "suspicious", "risk": "high", "reason": "IP dans liste noire"}
            
            # Vérifier si c'est une IP privée (normal pour développement)
            if ip_address.startswith(("192.168.", "10.", "172.")):
                return {"reputation": "private", "risk": "low", "note": "IP privée"}
            
            return {"reputation": "clean", "risk": "low"}
            
        except Exception:
            return {"reputation": "unknown", "risk": "medium"}
    
    async def _analyze_user_agent(self, user_agent: str) -> Dict[str, Any]:
        """Analyser l'user agent pour détecter les bots"""
        try:
            if not user_agent:
                return {"analysis": "unknown", "risk": "medium"}
            
            user_agent_lower = user_agent.lower()
            
            # Détecter les bots et outils automatisés
            bot_indicators = [
                "bot", "crawler", "spider", "scraper", "curl", "wget",
                "python", "java", "perl", "ruby", "php", "go"
            ]
            
            for indicator in bot_indicators:
                if indicator in user_agent_lower:
                    return {
                        "analysis": "bot_detected",
                        "risk": "high",
                        "indicator": indicator,
                        "recommendation": "Vérifier l'authenticité de la requête"
                    }
            
            # Détecter les navigateurs légitimes
            legitimate_browsers = [
                "chrome", "firefox", "safari", "edge", "opera"
            ]
            
            for browser in legitimate_browsers:
                if browser in user_agent_lower:
                    return {
                        "analysis": "legitimate_browser",
                        "risk": "low",
                        "browser": browser
                    }
            
            return {"analysis": "unknown", "risk": "medium"}
            
        except Exception:
            return {"analysis": "unknown", "risk": "medium"}
    
    async def _check_account_activity(self, user_id: int) -> Dict[str, Any]:
        """Vérifier l'activité du compte pour détecter des anomalies"""
        db: Optional[Session] = None
        try:
            if not user_id:
                return {"status": "unknown", "risk": "medium"}
            
            db = SessionLocal()
            
            # Vérifier les connexions récentes
            recent_logins = db.query(Message).filter(
                Message.user_id == user_id,
                Message.sender_type == "system",
                Message.content.like("%connexion%"),
                Message.timestamp >= datetime.utcnow() - timedelta(hours=24)
            ).count()
            
            # Vérifier les commandes récentes
            recent_orders = db.query(Order).filter(
                Order.user_id == user_id,
                Order.created_at >= datetime.utcnow() - timedelta(hours=24)
            ).count()
            
            # Analyser les patterns
            activity_score = 100
            
            if recent_logins > 10:
                activity_score -= 30
            if recent_orders > 5:
                activity_score -= 20
            
            risk_level = "low"
            if activity_score < 50:
                risk_level = "high"
            elif activity_score < 75:
                risk_level = "medium"
            
            return {
                "status": "active",
                "risk": risk_level,
                "recent_logins": recent_logins,
                "recent_orders": recent_orders,
                "activity_score": activity_score,
                "analysis": "Activité normale" if risk_level == "low" else "Activité suspecte détectée"
            }
            
        except Exception as e:
            self.logger.error(f"Erreur vérification activité compte: {str(e)}")
            return {"status": "error", "risk": "medium"}
        finally:
            if db:
                db.close()
    
    async def _check_transaction_history(self, user_id: int) -> Dict[str, Any]:
        """Vérifier l'historique des transactions pour détecter des anomalies"""
        db: Optional[Session] = None
        try:
            if not user_id:
                return {"status": "unknown", "risk": "medium"}
            
            db = SessionLocal()
            
            # Analyser les transactions des dernières 24h
            recent_transactions = db.query(Order).filter(
                Order.user_id == user_id,
                Order.created_at >= datetime.utcnow() - timedelta(hours=24)
            ).all()
            
            if not recent_transactions:
                return {"status": "no_recent_transactions", "risk": "low"}
            
            # Calculer les statistiques
            total_amount = sum(t.total_amount for t in recent_transactions)
            avg_amount = total_amount / len(recent_transactions)
            max_amount = max(t.total_amount for t in recent_transactions)
            
            # Détecter les anomalies
            anomalies = []
            risk_score = 0
            
            # Montant total élevé
            if total_amount > 1000:
                anomalies.append("Montant total élevé sur 24h")
                risk_score += 20
            
            # Nombre de transactions élevé
            if len(recent_transactions) > 10:
                anomalies.append("Nombre de transactions élevé")
                risk_score += 15
            
            # Variation importante des montants
            if max_amount > avg_amount * 5:
                anomalies.append("Variation importante des montants")
                risk_score += 10
            
            risk_level = "low"
            if risk_score > 30:
                risk_level = "high"
            elif risk_score > 15:
                risk_level = "medium"
            
            return {
                "status": "transactions_analyzed",
                "risk": risk_level,
                "total_transactions": len(recent_transactions),
                "total_amount": round(total_amount, 2),
                "average_amount": round(avg_amount, 2),
                "max_amount": round(max_amount, 2),
                "anomalies": anomalies,
                "risk_score": risk_score
            }
            
        except Exception as e:
            self.logger.error(f"Erreur vérification transactions: {str(e)}")
            return {"status": "error", "risk": "medium"}
        finally:
            if db:
                db.close()
    
    def _calculate_security_score(self, checks: Dict[str, Any]) -> int:
        """Calculer le score de sécurité global"""
        try:
            score = 100
            
            # Session
            if not checks.get("session_validity", {}).get("valid", False):
                score -= 30
            
            # IP
            ip_risk = checks.get("ip_reputation", {}).get("risk", "medium")
            if ip_risk == "high":
                score -= 25
            elif ip_risk == "medium":
                score -= 10
            
            # User Agent
            ua_risk = checks.get("user_agent_analysis", {}).get("risk", "medium")
            if ua_risk == "high":
                score -= 20
            elif ua_risk == "medium":
                score -= 5
            
            # Activité compte
            account_risk = checks.get("account_activity", {}).get("risk", "medium")
            if account_risk == "high":
                score -= 20
            elif account_risk == "medium":
                score -= 10
            
            # Transactions
            transaction_risk = checks.get("transaction_history", {}).get("risk", "medium")
            if transaction_risk == "high":
                score -= 15
            elif transaction_risk == "medium":
                score -= 5
            
            return max(0, score)
            
        except Exception:
            return 50
    
    def _generate_security_recommendations(self, checks: Dict[str, Any]) -> List[str]:
        """Générer des recommandations de sécurité"""
        recommendations = []
        
        try:
            # Session
            if not checks.get("session_validity", {}).get("valid", False):
                recommendations.append("Renouveler la session de connexion")
            
            # IP
            ip_risk = checks.get("ip_reputation", {}).get("risk", "medium")
            if ip_risk == "high":
                recommendations.append("Vérifier la sécurité de votre connexion réseau")
            
            # User Agent
            ua_risk = checks.get("user_agent_analysis", {}).get("risk", "medium")
            if ua_risk == "high":
                recommendations.append("Utiliser un navigateur web standard")
            
            # Activité compte
            account_risk = checks.get("account_activity", {}).get("risk", "medium")
            if account_risk == "high":
                recommendations.append("Vérifier l'activité de votre compte")
            
            # Transactions
            transaction_risk = checks.get("transaction_history", {}).get("risk", "medium")
            if transaction_risk == "high":
                recommendations.append("Vérifier vos transactions récentes")
            
            if not recommendations:
                recommendations.append("Aucune action de sécurité requise")
                
        except Exception:
            recommendations.append("Impossible de générer des recommandations")
        
        return recommendations
    
    async def detect_suspicious_activity_safe(self, user_id: int) -> Dict[str, Any]:
        """Détecter les activités suspectes pour un utilisateur"""
        try:
            if not user_id:
                return {"error": "ID utilisateur requis"}
            
            db = SessionLocal()
            
            # Vérifier les échecs de connexion
            failed_logins = db.query(Message).filter(
                Message.user_id == user_id,
                Message.content.like("%échec%connexion%"),
                Message.timestamp >= datetime.utcnow() - timedelta(minutes=5)
            ).count()
            
            # Vérifier les tentatives de paiement
            payment_attempts = db.query(Order).filter(
                Order.user_id == user_id,
                Order.status == "failed",
                Order.created_at >= datetime.utcnow() - timedelta(hours=1)
            ).count()
            
            # Détecter les anomalies
            suspicious_activities = []
            
            if failed_logins >= self.suspicious_patterns["multiple_failed_logins"]["threshold"]:
                suspicious_activities.append({
                    "type": "multiple_failed_logins",
                    "severity": "high",
                    "description": f"{failed_logins} échecs de connexion en 5 minutes",
                    "action_required": "Vérifier la sécurité du compte"
                })
            
            if payment_attempts >= self.suspicious_patterns["unusual_payment_activity"]["threshold"]:
                suspicious_activities.append({
                    "type": "unusual_payment_activity",
                    "severity": "medium",
                    "description": f"{payment_attempts} tentatives de paiement échouées en 1 heure",
                    "action_required": "Vérifier les informations de paiement"
                })
            
            return {
                "suspicious_activities": suspicious_activities,
                "total_detected": len(suspicious_activities),
                "account_status": "compromised" if suspicious_activities else "secure",
                "recommendations": [
                    "Changer le mot de passe si nécessaire",
                    "Vérifier l'historique des connexions",
                    "Contacter le support en cas de doute"
                ] if suspicious_activities else ["Aucune action requise"]
            }
            
        except Exception as e:
            self.logger.error(f"Erreur détection activité suspecte: {str(e)}")
            return {"error": str(e)}
        finally:
            if db:
                db.close()
    
    async def secure_transaction_safe(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Sécuriser une transaction"""
        try:
            user_id = state.get("user_id")
            amount = state.get("amount", 0.0)
            payment_method = state.get("payment_method", "")
            
            # Vérifications de sécurité
            security_checks = []
            
            # Montant élevé
            if amount > 500:
                security_checks.append({
                    "check": "high_amount",
                    "passed": True,
                    "description": "Montant élevé détecté, vérifications renforcées"
                })
            
            # Méthode de paiement
            if payment_method in ["card", "digital_wallet"]:
                security_checks.append({
                    "check": "secure_payment_method",
                    "passed": True,
                    "description": "Méthode de paiement sécurisée"
                })
            else:
                security_checks.append({
                    "check": "secure_payment_method",
                    "passed": False,
                    "description": "Méthode de paiement moins sécurisée"
                })
            
            # Validation 3D Secure si applicable
            if payment_method == "card" and amount > 100:
                security_checks.append({
                    "check": "3d_secure_required",
                    "passed": True,
                    "description": "3D Secure requis pour ce montant"
                })
            
            # Calculer le score de sécurité
            passed_checks = sum(1 for check in security_checks if check["passed"])
            security_score = (passed_checks / len(security_checks)) * 100 if security_checks else 0
            
            return {
                "transaction_secured": security_score >= 80,
                "security_score": round(security_score, 1),
                "security_checks": security_checks,
                "recommendations": [
                    "Utiliser une méthode de paiement sécurisée",
                    "Vérifier les informations de paiement",
                    "Activer l'authentification à deux facteurs"
                ] if security_score < 80 else ["Transaction sécurisée"]
            }
            
        except Exception as e:
            self.logger.error(f"Erreur sécurisation transaction: {str(e)}")
            return {"error": str(e)}
    
    async def validate_payment_safe(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Valider un paiement avec vérifications de sécurité"""
        try:
            payment_data = state.get("payment_data", {})
            user_id = state.get("user_id")
            
            # Vérifications de base
            required_fields = ["card_number", "expiry_date", "cvv", "cardholder_name"]
            missing_fields = [field for field in required_fields if not payment_data.get(field)]
            
            if missing_fields:
                return {
                    "valid": False,
                    "error": f"Champs manquants: {', '.join(missing_fields)}",
                    "security_risk": "high"
                }
            
            # Validation du format
            validation_results = []
            
            # Numéro de carte (format basique)
            card_number = payment_data.get("card_number", "")
            if not re.match(r'^\d{13,19}$', card_number.replace(" ", "")):
                validation_results.append({
                    "field": "card_number",
                    "valid": False,
                    "message": "Format de numéro de carte invalide"
                })
            else:
                validation_results.append({
                    "field": "card_number",
                    "valid": True,
                    "message": "Format valide"
                })
            
            # Date d'expiration
            expiry = payment_data.get("expiry_date", "")
            if not re.match(r'^\d{2}/\d{2}$', expiry):
                validation_results.append({
                    "field": "expiry_date",
                    "valid": False,
                    "message": "Format de date invalide (MM/YY)"
                })
            else:
                validation_results.append({
                    "field": "expiry_date",
                    "valid": True,
                    "message": "Format valide"
                })
            
            # CVV
            cvv = payment_data.get("cvv", "")
            if not re.match(r'^\d{3,4}$', cvv):
                validation_results.append({
                    "field": "cvv",
                    "valid": False,
                    "message": "CVV invalide"
                })
            else:
                validation_results.append({
                    "field": "cvv",
                    "valid": True,
                    "message": "Format valide"
                })
            
            # Calculer le score de validation
            valid_fields = sum(1 for result in validation_results if result["valid"])
            validation_score = (valid_fields / len(validation_results)) * 100
            
            return {
                "valid": validation_score == 100,
                "validation_score": round(validation_score, 1),
                "validation_results": validation_results,
                "security_checks": [
                    "Format des données validé",
                    "Chiffrement SSL requis",
                    "3D Secure recommandé"
                ],
                "next_steps": [
                    "Procéder au paiement sécurisé",
                    "Vérifier l'authentification 3D Secure"
                ] if validation_score == 100 else [
                    "Corriger les erreurs de format",
                    "Vérifier les informations saisies"
                ]
            }
            
        except Exception as e:
            self.logger.error(f"Erreur validation paiement: {str(e)}")
            return {"error": str(e)}
    
    async def check_account_security_safe(self, user_id: int) -> Dict[str, Any]:
        """Vérifier la sécurité du compte utilisateur"""
        try:
            if not user_id:
                return {"error": "ID utilisateur requis"}
            
            db = SessionLocal()
            
            # Vérifier la force du mot de passe (simulation)
            password_strength = "strong"  # En production, analyser le hash
            
            # Vérifier l'authentification à deux facteurs
            two_factor_enabled = True  # En production, vérifier en base
            
            # Vérifier la dernière modification du mot de passe
            last_password_change = datetime.utcnow() - timedelta(days=30)  # Simulation
            
            # Vérifier les connexions depuis des appareils inconnus
            unknown_devices = 0  # En production, analyser les sessions
            
            # Calculer le score de sécurité du compte
            security_score = 100
            
            if password_strength != "strong":
                security_score -= 20
            if not two_factor_enabled:
                security_score -= 30
            if (datetime.utcnow() - last_password_change).days > 90:
                security_score -= 15
            if unknown_devices > 0:
                security_score -= 10
            
            security_level = "excellent"
            if security_score < 60:
                security_level = "faible"
            elif security_score < 80:
                security_level = "moyen"
            elif security_score < 90:
                security_level = "bon"
            
            return {
                "account_security": {
                    "score": security_score,
                    "level": security_level,
                    "password_strength": password_strength,
                    "two_factor_enabled": two_factor_enabled,
                    "days_since_password_change": (datetime.utcnow() - last_password_change).days,
                    "unknown_devices": unknown_devices
                },
                "recommendations": self._generate_account_security_recommendations(security_score),
                "security_features": [
                    "Authentification à deux facteurs",
                    "Notifications de connexion",
                    "Historique des connexions",
                    "Gestion des appareils autorisés"
                ]
            }
            
        except Exception as e:
            self.logger.error(f"Erreur vérification sécurité compte: {str(e)}")
            return {"error": str(e)}
        finally:
            if db:
                db.close()
    
    def _generate_account_security_recommendations(self, security_score: int) -> List[str]:
        """Générer des recommandations de sécurité pour le compte"""
        recommendations = []
        
        if security_score < 60:
            recommendations.extend([
                "Changer immédiatement le mot de passe",
                "Activer l'authentification à deux facteurs",
                "Vérifier les appareils connectés",
                "Contacter le support sécurité"
            ])
        elif security_score < 80:
            recommendations.extend([
                "Renforcer le mot de passe",
                "Activer l'authentification à deux facteurs",
                "Vérifier régulièrement l'activité du compte"
            ])
        elif security_score < 90:
            recommendations.extend([
                "Changer le mot de passe (recommandé tous les 3 mois)",
                "Vérifier les paramètres de sécurité"
            ])
        else:
            recommendations.append("Maintenir les bonnes pratiques de sécurité")
        
        return recommendations
    
    async def generate_security_report_safe(self, user_id: int) -> Dict[str, Any]:
        """Générer un rapport de sécurité pour l'utilisateur"""
        try:
            if not user_id:
                return {"error": "ID utilisateur requis"}
            
            # Collecter toutes les informations de sécurité
            security_check = await self.perform_security_check_safe({"user_id": user_id})
            suspicious_activity = await self.detect_suspicious_activity_safe(user_id)
            account_security = await self.check_account_security_safe(user_id)
            
            # Générer le rapport
            report = {
                "user_id": user_id,
                "generated_at": datetime.utcnow().isoformat(),
                "overall_security_score": security_check.get("security_score", 0),
                "risk_assessment": {
                    "current_level": security_check.get("risk_level", "unknown"),
                    "threats_detected": len(suspicious_activity.get("suspicious_activities", [])),
                    "account_compromised": suspicious_activity.get("account_status") == "compromised"
                },
                "security_checks": security_check.get("checks", {}),
                "account_security": account_security.get("account_security", {}),
                "suspicious_activities": suspicious_activity.get("suspicious_activities", []),
                "recommendations": {
                    "immediate": [],
                    "short_term": [],
                    "long_term": []
                },
                "next_review": (datetime.utcnow() + timedelta(days=7)).isoformat()
            }
            
            # Catégoriser les recommandations
            if report["overall_security_score"] < 50:
                report["recommendations"]["immediate"].extend([
                    "Changer le mot de passe",
                    "Activer l'authentification à deux facteurs",
                    "Vérifier l'activité du compte"
                ])
            
            if suspicious_activity.get("account_status") == "compromised":
                report["recommendations"]["immediate"].extend([
                    "Contacter immédiatement le support",
                    "Bloquer temporairement le compte",
                    "Vérifier tous les appareils connectés"
                ])
            
            return report
            
        except Exception as e:
            self.logger.error(f"Erreur génération rapport sécurité: {str(e)}")
            return {"error": str(e)}

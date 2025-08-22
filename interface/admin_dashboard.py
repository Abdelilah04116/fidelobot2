
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from typing import Dict, Any
from agents.monitoring_agent import MonitoringAgent
from agents.gdpr_agent import GDPRAgent
from auth import get_current_active_user
from models.database import User

admin_router = APIRouter(prefix="/admin", tags=["admin"])
monitoring_agent = MonitoringAgent()
gdpr_agent = GDPRAgent()

@admin_router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(current_user: User = Depends(get_current_active_user)):
    """Interface d'administration"""
    if not current_user.is_vip:  # Simplifié - en prod, créer un rôle admin
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard Admin - Chatbot E-Commerce</title>
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .dashboard { max-width: 1200px; margin: 0 auto; }
            .card { background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
            .metric { text-align: center; padding: 15px; background: #f8f9fa; border-radius: 5px; }
            .metric-value { font-size: 2em; font-weight: bold; color: #007bff; }
            .metric-label { color: #666; margin-top: 5px; }
            .alert { padding: 10px; margin: 10px 0; border-radius: 4px; }
            .alert-critical { background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; }
            .alert-warning { background: #fff3cd; border: 1px solid #ffeaa7; color: #856404; }
            .alert-info { background: #d1ecf1; border: 1px solid #bee5eb; color: #0c5460; }
            .btn { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; margin: 5px; }
            .btn:hover { background: #0056b3; }
            .status-healthy { color: #28a745; }
            .status-warning { color: #ffc107; }
            .status-critical { color: #dc3545; }
            .loading { display: none; text-align: center; padding: 20px; }
        </style>
    </head>
    <body>
        <div class="dashboard">
            <h1>🔧 Dashboard Administrateur</h1>
            
            <div class="card">
                <h2>État du Système</h2>
                <div id="healthStatus" class="loading">Chargement...</div>
                <button onclick="refreshHealth()" class="btn">Actualiser</button>
            </div>
            
            <div class="card">
                <h2>Métriques de Performance</h2>
                <div id="performanceMetrics" class="loading">Chargement...</div>
                <button onclick="refreshMetrics()" class="btn">Actualiser</button>
            </div>
            
            <div class="card">
                <h2>Alertes Système</h2>
                <div id="systemAlerts" class="loading">Chargement...</div>
                <button onclick="refreshAlerts()" class="btn">Vérifier les Alertes</button>
            </div>
            
            <div class="card">
                <h2>Satisfaction Utilisateur</h2>
                <div id="userSatisfaction" class="loading">Chargement...</div>
                <button onclick="refreshSatisfaction()" class="btn">Analyser</button>
            </div>
            
            <div class="card">
                <h2>Conformité RGPD</h2>
                <div id="gdprCompliance" class="loading">Chargement...</div>
                <button onclick="refreshGDPR()" class="btn">Auditer</button>
            </div>
        </div>
        
        <script>
            async function makeAPICall(endpoint, data = {}) {
                try {
                    const response = await fetch(endpoint, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                        },
                        body: JSON.stringify(data)
                    });
                    return await response.json();
                } catch (error) {
                    console.error('Erreur API:', error);
                    return { error: 'Erreur de communication' };
                }
            }
            
            async function refreshHealth() {
                document.getElementById('healthStatus').innerHTML = 'Chargement...';
                const data = await makeAPICall('/admin/monitoring', { monitoring_type: 'health_check' });
                
                if (data.error) {
                    document.getElementById('healthStatus').innerHTML = `<div class="alert alert-critical">${data.error}</div>`;
                    return;
                }
                
                const statusClass = data.overall_status === 'healthy' ? 'status-healthy' : 
                                   data.overall_status === 'degraded' ? 'status-warning' : 'status-critical';
                
                let html = `<div class="metrics-grid">`;
                html += `<div class="metric">
                    <div class="metric-value ${statusClass}">${data.overall_status.toUpperCase()}</div>
                    <div class="metric-label">État Général</div>
                </div>`;
                
                for (const [component, status] of Object.entries(data.components)) {
                    const compClass = status.status === 'healthy' ? 'status-healthy' : 'status-critical';
                    html += `<div class="metric">
                        <div class="metric-value ${compClass}">${status.status}</div>
                        <div class="metric-label">${component}</div>
                    </div>`;
                }
                html += '</div>';
                
                document.getElementById('healthStatus').innerHTML = html;
            }
            
            async function refreshMetrics() {
                document.getElementById('performanceMetrics').innerHTML = 'Chargement...';
                const data = await makeAPICall('/admin/monitoring', { monitoring_type: 'performance_metrics' });
                
                if (data.error) {
                    document.getElementById('performanceMetrics').innerHTML = `<div class="alert alert-critical">${data.error}</div>`;
                    return;
                }
                
                let html = `<div class="metrics-grid">`;
                html += `<div class="metric">
                    <div class="metric-value">${data.total_conversations}</div>
                    <div class="metric-label">Conversations (24h)</div>
                </div>`;
                html += `<div class="metric">
                    <div class="metric-value">${data.average_response_time}s</div>
                    <div class="metric-label">Temps de Réponse Moyen</div>
                </div>`;
                html += `<div class="metric">
                    <div class="metric-value">${data.escalation_rate}%</div>
                    <div class="metric-label">Taux d'Escalade</div>
                </div>`;
                html += `<div class="metric">
                    <div class="metric-value">${data.messages_per_conversation}</div>
                    <div class="metric-label">Messages par Conversation</div>
                </div>`;
                html += '</div>';
                
                // Top intents
                if (data.top_intents && Object.keys(data.top_intents).length > 0) {
                    html += '<h3>Intentions les Plus Fréquentes</h3><ul>';
                    for (const [intent, count] of Object.entries(data.top_intents)) {
                        html += `<li><strong>${intent}:</strong> ${count}</li>`;
                    }
                    html += '</ul>';
                }
                
                document.getElementById('performanceMetrics').innerHTML = html;
            }
            
            async function refreshAlerts() {
                document.getElementById('systemAlerts').innerHTML = 'Chargement...';
                const data = await makeAPICall('/admin/monitoring', { monitoring_type: 'alert_check' });
                
                if (data.error) {
                    document.getElementById('systemAlerts').innerHTML = `<div class="alert alert-critical">${data.error}</div>`;
                    return;
                }
                
                let html = `<p><strong>Nombre d'alertes:</strong> ${data.alert_count}</p>`;
                
                if (data.alerts.length === 0) {
                    html += '<div class="alert alert-info">Aucune alerte active</div>';
                } else {
                    for (const alert of data.alerts) {
                        const alertClass = alert.level === 'critical' ? 'alert-critical' : 
                                         alert.level === 'warning' ? 'alert-warning' : 'alert-info';
                        html += `<div class="alert ${alertClass}">
                            <strong>${alert.level.toUpperCase()}:</strong> ${alert.message}
                        </div>`;
                    }
                }
                
                document.getElementById('systemAlerts').innerHTML = html;
            }
            
            async function refreshSatisfaction() {
                document.getElementById('userSatisfaction').innerHTML = 'Chargement...';
                const data = await makeAPICall('/admin/monitoring', { monitoring_type: 'user_satisfaction' });
                
                if (data.error) {
                    document.getElementById('userSatisfaction').innerHTML = `<div class="alert alert-critical">${data.error}</div>`;
                    return;
                }
                
                const scoreClass = data.satisfaction_score >= 80 ? 'status-healthy' : 
                                  data.satisfaction_score >= 60 ? 'status-warning' : 'status-critical';
                
                let html = `<div class="metrics-grid">`;
                html += `<div class="metric">
                    <div class="metric-value ${scoreClass}">${data.satisfaction_score}</div>
                    <div class="metric-label">Score de Satisfaction</div>
                </div>`;
                html += `<div class="metric">
                    <div class="metric-value">${data.short_conversation_rate}%</div>
                    <div class="metric-label">Conversations Courtes</div>
                </div>`;
                html += `<div class="metric">
                    <div class="metric-value">${data.error_message_rate}%</div>
                    <div class="metric-label">Messages d'Erreur</div>
                </div>`;
                html += '</div>';
                
                if (data.recommendations.length > 0) {
                    html += '<h3>Recommandations</h3><ul>';
                    for (const rec of data.recommendations) {
                        html += `<li>${rec}</li>`;
                    }
                    html += '</ul>';
                }
                
                document.getElementById('userSatisfaction').innerHTML = html;
            }
            
            async function refreshGDPR() {
                document.getElementById('gdprCompliance').innerHTML = 'Chargement...';
                const data = await makeAPICall('/admin/gdpr', { action: 'audit_data' });
                
                if (data.error) {
                    document.getElementById('gdprCompliance').innerHTML = `<div class="alert alert-critical">${data.error}</div>`;
                    return;
                }
                
                const scoreClass = data.compliance_score >= 80 ? 'status-healthy' : 
                                  data.compliance_score >= 60 ? 'status-warning' : 'status-critical';
                
                let html = `<div class="metrics-grid">`;
                html += `<div class="metric">
                    <div class="metric-value ${scoreClass}">${data.compliance_score}</div>
                    <div class="metric-label">Score de Conformité</div>
                </div>`;
                html += `<div class="metric">
                    <div class="metric-value">${data.statistics.total_users}</div>
                    <div class="metric-label">Total Utilisateurs</div>
                </div>`;
                html += `<div class="metric">
                    <div class="metric-value">${data.statistics.old_conversations}</div>
                    <div class="metric-label">Conversations Anciennes</div>
                </div>`;
                html += `<div class="metric">
                    <div class="metric-value">${data.statistics.potentially_sensitive_messages}</div>
                    <div class="metric-label">Messages Sensibles</div>
                </div>`;
                html += '</div>';
                
                if (data.recommendations.length > 0) {
                    html += '<h3>Actions Recommandées</h3><ul>';
                    for (const rec of data.recommendations) {
                        html += `<li>${rec}</li>`;
                    }
                    html += '</ul>';
                }
                
                document.getElementById('gdprCompliance').innerHTML = html;
            }
            
            // Charger les données au démarrage
            window.onload = function() {
                refreshHealth();
                refreshMetrics();
                refreshAlerts();
                refreshSatisfaction();
                refreshGDPR();
            };
            
            // Actualisation automatique toutes les 5 minutes
            setInterval(() => {
                refreshHealth();
                refreshMetrics();
                refreshAlerts();
            }, 300000);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@admin_router.post("/monitoring")
async def monitoring_endpoint(
    request: Dict[str, Any],
    current_user: User = Depends(get_current_active_user)
):
    """Endpoint pour le monitoring"""
    if not current_user.is_vip:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    return await monitoring_agent.execute(request)

@admin_router.post("/gdpr")
async def gdpr_endpoint(
    request: Dict[str, Any],
    current_user: User = Depends(get_current_active_user)
):
    """Endpoint pour les opérations RGPD"""
    if not current_user.is_vip:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    return await gdpr_agent.execute(request)
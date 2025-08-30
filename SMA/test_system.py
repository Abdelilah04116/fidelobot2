#!/usr/bin/env python3
"""
Script de test pour vérifier le bon fonctionnement du SMA
Teste tous les agents corrigés et l'orchestrateur
"""

import asyncio
import sys
import os
from pathlib import Path

# Ajouter le répertoire SMA au path
sys.path.append(str(Path(__file__).parent))

from agents.agent_orchestrator import AgentOrchestrator
from agents.product_search_agent import ProductSearchAgent
from agents.customer_service_agent import CustomerServiceAgent
from agents.recommendation_agent import RecommendationAgent
from agents.cart_management_agent import CartManagementAgent
from agents.voice_agent import VoiceAgent
from agents.multimodal_agent import MultimodalAgent

async def test_individual_agents():
    """Teste chaque agent individuellement"""
    print("🔍 **TEST DES AGENTS INDIVIDUELS**\n")
    
    # Test ProductSearchAgent
    print("1. Test ProductSearchAgent...")
    try:
        agent = ProductSearchAgent()
        result = await agent.execute({
            "search_query": "tablette",
            "user_message": "Je cherche une tablette",
            "session_id": "test-123"
        })
        print(f"   ✅ Succès: {result.get('response_text', 'Pas de réponse')[:50]}...")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test CustomerServiceAgent
    print("2. Test CustomerServiceAgent...")
    try:
        agent = CustomerServiceAgent()
        result = await agent.execute({
            "user_message": "Comment retourner un produit ?",
            "session_id": "test-123"
        })
        print(f"   ✅ Succès: {result.get('response_text', 'Pas de réponse')[:50]}...")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test RecommendationAgent
    print("3. Test RecommendationAgent...")
    try:
        agent = RecommendationAgent()
        result = await agent.execute({
            "user_message": "Donnez-moi des recommandations",
            "session_id": "test-123"
        })
        print(f"   ✅ Succès: {result.get('response_text', 'Pas de réponse')[:50]}...")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test CartManagementAgent
    print("4. Test CartManagementAgent...")
    try:
        agent = CartManagementAgent()
        result = await agent.execute({
            "user_message": "Voir mon panier",
            "session_id": "test-123"
        })
        print(f"   ✅ Succès: {result.get('response_text', 'Pas de réponse')[:50]}...")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test VoiceAgent
    print("5. Test VoiceAgent...")
    try:
        agent = VoiceAgent()
        result = await agent.execute({
            "user_message": "Test agent vocal",
            "session_id": "test-123"
        })
        print(f"   ✅ Succès: {result.get('response_text', 'Pas de réponse')[:50]}...")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test MultimodalAgent
    print("6. Test MultimodalAgent...")
    try:
        agent = MultimodalAgent()
        result = await agent.execute({
            "user_message": "Analyser cette image",
            "session_id": "test-123"
        })
        print(f"   ✅ Succès: {result.get('response_text', 'Pas de réponse')[:50]}...")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")

async def test_orchestrator():
    """Teste l'orchestrateur principal"""
    print("\n🎯 **TEST DE L'ORCHESTRATEUR**\n")
    
    try:
        orchestrator = AgentOrchestrator()
        print("✅ Orchestrateur initialisé avec succès")
        
        # Test d'exécution simple
        result = await orchestrator.execute({
            "user_query": "Je cherche une tablette et veux des recommandations",
            "user_id": 1,
            "session_id": "test-orchestrator-123",
            "context": {"urgent": False}
        })
        
        if result.get("success"):
            print("✅ Orchestrateur fonctionne correctement")
            print(f"   Agents utilisés: {result.get('agents_used', [])}")
            print(f"   User stories identifiées: {result.get('user_stories_identified', [])}")
        else:
            print(f"⚠️ Orchestrateur a rencontré des problèmes: {result.get('error', 'Erreur inconnue')}")
            
    except Exception as e:
        print(f"❌ Erreur critique dans l'orchestrateur: {e}")

async def test_system_health():
    """Teste la santé globale du système"""
    print("\n🏥 **TEST DE SANTÉ DU SYSTÈME**\n")
    
    try:
        orchestrator = AgentOrchestrator()
        health = await orchestrator.get_system_health()
        
        if "error" not in health:
            print(f"✅ Statut global: {health.get('overall_status', 'inconnu')}")
            print(f"   Agents sains: {health.get('healthy_agents', 0)}/{health.get('total_agents', 0)}")
            print(f"   Pourcentage de santé: {health.get('health_percentage', 0)}%")
            
            # Détails par agent
            print("\n   Détails par agent:")
            for agent_name, status in health.get('agent_status', {}).items():
                emoji = "✅" if status.get('status') == 'healthy' else "❌"
                print(f"     {emoji} {agent_name}: {status.get('status', 'inconnu')}")
        else:
            print(f"❌ Erreur lors du test de santé: {health.get('error')}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test de santé: {e}")

async def main():
    """Fonction principale de test"""
    print("🚀 **DÉMARRAGE DES TESTS DU SMA**\n")
    print("=" * 50)
    
    # Test des agents individuels
    await test_individual_agents()
    
    # Test de l'orchestrateur
    await test_orchestrator()
    
    # Test de santé du système
    await test_system_health()
    
    print("\n" + "=" * 50)
    print("🎉 **TESTS TERMINÉS**")
    print("\nSi tu vois des ✅, ton SMA fonctionne bien !")
    print("Si tu vois des ❌, il y a encore des corrections à faire.")

if __name__ == "__main__":
    asyncio.run(main())

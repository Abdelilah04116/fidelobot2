#!/usr/bin/env python3
"""
Test rapide de l'agent multimodal
"""

import asyncio
import sys
import os

# Ajouter le chemin du projet
sys.path.append('.')

async def quick_test():
    """Test rapide de l'agent multimodal"""
    print("🚀 Test rapide de l'agent multimodal...")
    
    try:
        # Test 1: Import de l'agent
        print("1️⃣ Test d'import...")
        from SMA.agents.multimodal_agent import MultimodalAgent
        print("   ✅ MultimodalAgent importé")
        
        # Test 2: Initialisation
        print("2️⃣ Test d'initialisation...")
        agent = MultimodalAgent()
        print("   ✅ Agent initialisé")
        
        # Test 3: Prompt système
        print("3️⃣ Test du prompt système...")
        prompt = agent.get_system_prompt()
        print(f"   ✅ Prompt système: {len(prompt)} caractères")
        
        # Test 4: Test d'exécution basique
        print("4️⃣ Test d'exécution...")
        test_state = {
            "user_message": "Test d'image",
            "audio_data": "fake_data",
            "audio_format": "png",
            "session_id": "test",
            "user_id": 1,
            "conversation_history": [],
            "intent": "image_analysis",
            "confidence": 0.8,
            "user_profile": {},
            "is_authenticated": True,
            "agents_used": [],
            "failed_attempts": 0,
            "products": [],
            "recommendations": [],
            "order_info": {},
            "cart": {},
            "response_text": "",
            "response_type": "",
            "escalate": False,
            "processing_time": 0.0,
            "error_message": ""
        }
        
        result = await agent.execute(test_state)
        print(f"   ✅ Exécution réussie: {result.get('response_text', 'Pas de réponse')}")
        
        # Test 5: Test de l'orchestrateur
        print("5️⃣ Test de l'orchestrateur...")
        from SMA.core.orchestrator import ChatbotOrchestrator
        orchestrator = ChatbotOrchestrator()
        print("   ✅ Orchestrateur initialisé")
        
        # Vérifier que l'agent multimodal est dans la liste
        agent_names = [agent.__class__.__name__ for agent in orchestrator.agents.values()]
        if 'MultimodalAgent' in agent_names:
            print("   ✅ Agent multimodal trouvé dans l'orchestrateur")
        else:
            print("   ❌ Agent multimodal non trouvé dans l'orchestrateur")
            return False
        
        print("\n🎉 Tous les tests sont passés!")
        print("\n📋 Pour tester avec une vraie image:")
        print("1. Démarrez le serveur: uvicorn catalogue.backend.main:app --reload")
        print("2. Ouvrez l'interface: http://localhost:5173/")
        print("3. Envoyez une image dans le chat")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("💡 Solution: Installez les dépendances avec pip install -r SMA/requirements_multimodal.txt")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(quick_test())
    if success:
        print("\n✅ L'agent multimodal est prêt à être testé!")
    else:
        print("\n❌ Des problèmes ont été détectés. Consultez le guide de dépannage.")

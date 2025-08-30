#!/usr/bin/env python3
"""
Test simple du SMA - Vérification des agents de base
Version corrigée pour éviter les problèmes d'import
"""

import asyncio
import sys
import os
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))
sys.path.insert(0, str(current_dir))

async def test_simple():
    """Test simple des agents essentiels"""
    print("🚀 **TEST SIMPLE DU SMA**\n")
    
    # Test 1: BaseAgent
    print("1. Test BaseAgent...")
    try:
        from SMA.agents.base_agent import BaseAgent
        print("   ✅ BaseAgent importé avec succès")
    except Exception as e:
        print(f"   ❌ Erreur BaseAgent: {e}")
        return
    
    # Test 2: ProductSearchAgent
    print("2. Test ProductSearchAgent...")
    try:
        from SMA.agents.product_search_agent import ProductSearchAgent
        agent = ProductSearchAgent()
        print("   ✅ ProductSearchAgent créé avec succès")
    except Exception as e:
        print(f"   ❌ Erreur ProductSearchAgent: {e}")
    
    # Test 3: CustomerServiceAgent
    print("3. Test CustomerServiceAgent...")
    try:
        from SMA.agents.customer_service_agent import CustomerServiceAgent
        agent = CustomerServiceAgent()
        print("   ✅ CustomerServiceAgent créé avec succès")
    except Exception as e:
        print(f"   ❌ Erreur CustomerServiceAgent: {e}")
    
    # Test 4: AgentOrchestrator
    print("4. Test AgentOrchestrator...")
    try:
        from SMA.agents.agent_orchestrator import AgentOrchestrator
        orchestrator = AgentOrchestrator()
        print("   ✅ AgentOrchestrator créé avec succès")
        print(f"   ✅ Nombre d'agents: {len(orchestrator.agents)}")
    except Exception as e:
        print(f"   ❌ Erreur AgentOrchestrator: {e}")
    
    print("\n🎯 **RÉSUMÉ**")
    print("Si tu vois des ✅, ton SMA est prêt !")
    print("Si tu vois des ❌, il y a encore des corrections à faire.")

if __name__ == "__main__":
    asyncio.run(test_simple())

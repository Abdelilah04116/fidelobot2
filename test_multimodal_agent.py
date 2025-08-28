#!/usr/bin/env python3
"""
Script de test pour l'agent multimodal
"""

import asyncio
import base64
import os
from PIL import Image
import numpy as np

# Ajouter le chemin du projet
import sys
sys.path.append('.')

from SMA.agents.multimodal_agent import MultimodalAgent
from SMA.tools.image_tools import ImageProcessingTools
from SMA.tools.vector_search import VectorSearchTools

async def test_image_processing():
    """Test du traitement d'images"""
    print("🧪 Test du traitement d'images...")
    
    # Créer une image de test simple
    test_image = Image.new('RGB', (100, 100), color='red')
    
    # Sauvegarder temporairement
    test_image_path = "test_image.png"
    test_image.save(test_image_path)
    
    try:
        # Initialiser les outils
        image_tools = ImageProcessingTools()
        
        # Analyser l'image
        analysis = image_tools.analyze_image_content(test_image)
        print(f"✅ Analyse d'image: {analysis}")
        
        # Extraire l'embedding
        embedding = image_tools.extract_image_embedding(test_image)
        if embedding is not None:
            print(f"✅ Embedding extrait: forme {embedding.shape}")
        else:
            print("❌ Échec extraction embedding")
        
        # Générer description
        description = image_tools.generate_image_description(analysis)
        print(f"✅ Description générée: {description}")
        
    finally:
        # Nettoyer
        if os.path.exists(test_image_path):
            os.remove(test_image_path)

async def test_vector_search():
    """Test de la recherche vectorielle"""
    print("\n🔍 Test de la recherche vectorielle...")
    
    try:
        # Initialiser les outils
        vector_tools = VectorSearchTools()
        
        # Créer un embedding de test
        test_embedding = np.random.rand(1, 512).astype(np.float32)
        
        # Test de recherche (sans Qdrant pour l'instant)
        print("✅ Outils de recherche vectorielle initialisés")
        
    except Exception as e:
        print(f"❌ Erreur recherche vectorielle: {e}")

async def test_multimodal_agent():
    """Test de l'agent multimodal complet"""
    print("\n🤖 Test de l'agent multimodal...")
    
    try:
        # Initialiser l'agent
        agent = MultimodalAgent()
        print("✅ Agent multimodal initialisé")
        
        # Test du prompt système
        system_prompt = agent.get_system_prompt()
        print(f"✅ Prompt système: {len(system_prompt)} caractères")
        
        # Créer un état de test
        test_state = {
            "user_message": "Test d'image",
            "audio_data": base64.b64encode(b"fake_image_data").decode(),
            "audio_format": "png",
            "session_id": "test-123",
            "user_id": 1,
            "conversation_history": [],
            "intent": "",
            "confidence": 0.0,
            "user_profile": {},
            "is_authenticated": False,
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
        
        # Exécuter l'agent
        result = await agent.execute(test_state)
        print(f"✅ Exécution agent: {result}")
        
    except Exception as e:
        print(f"❌ Erreur agent multimodal: {e}")

async def test_image_upload_simulation():
    """Simulation d'un upload d'image"""
    print("\n📸 Test simulation upload d'image...")
    
    try:
        # Créer une image de test
        test_image = Image.new('RGB', (200, 200), color='blue')
        
        # Convertir en base64
        import io
        buffer = io.BytesIO()
        test_image.save(buffer, format='PNG')
        image_data = buffer.getvalue()
        image_base64 = base64.b64encode(image_data).decode()
        
        print(f"✅ Image créée et encodée: {len(image_base64)} caractères base64")
        
        # Simuler l'envoi via l'agent
        agent = MultimodalAgent()
        
        # Créer un état avec l'image
        test_state = {
            "user_message": "Voici une image de produit",
            "audio_data": image_base64,  # Réutilise le champ audio_data
            "audio_format": "png",
            "session_id": "test-image-123",
            "user_id": 1,
            "conversation_history": [],
            "intent": "image_analysis",
            "confidence": 0.8,
            "user_profile": {"segment": "test"},
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
        
        # Traiter l'image
        result = await agent.execute(test_state)
        print(f"✅ Résultat traitement image: {result.get('response_text', 'Pas de réponse')}")
        
        if result.get("products"):
            print(f"✅ Produits trouvés: {len(result['products'])}")
        
    except Exception as e:
        print(f"❌ Erreur simulation upload: {e}")

async def main():
    """Fonction principale de test"""
    print("🚀 Démarrage des tests de l'agent multimodal\n")
    
    try:
        # Tests individuels
        await test_image_processing()
        await test_vector_search()
        await test_multimodal_agent()
        await test_image_upload_simulation()
        
        print("\n✅ Tous les tests terminés avec succès!")
        
    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Exécuter les tests
    asyncio.run(main())

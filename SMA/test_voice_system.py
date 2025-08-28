"""
Script de test pour le système de traitement vocal
Teste la transcription, la synthèse vocale et l'extraction d'intention
"""

import asyncio
import base64
import json
import logging
from pathlib import Path

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import du système vocal
from core.voice_processing_system import VoiceProcessingSystem

async def test_voice_system():
    """Test complet du système de traitement vocal"""
    
    print("🎤 Test du système de traitement vocal Fidelo")
    print("=" * 50)
    
    # Initialiser le système
    voice_system = VoiceProcessingSystem()
    
    # Test 1: Vérifier les capacités
    print("\n1. Vérification des capacités:")
    capabilities = voice_system.get_capabilities()
    print(f"   - Système: {capabilities['system']}")
    print(f"   - Capacités: {', '.join(capabilities['capabilities'])}")
    print(f"   - FFmpeg disponible: {capabilities['ffmpeg_available']}")
    print(f"   - Langues supportées: {capabilities['languages']}")
    
    # Test 2: Extraction d'intention
    print("\n2. Test d'extraction d'intention:")
    test_texts = [
        ("Cherche des téléphones", "fr"),
        ("Ajoute ce produit au panier", "fr"),
        ("Show me laptops", "en"),
        ("أريد البحث عن هاتف", "ar")
    ]
    
    for text, lang in test_texts:
        intent_result = voice_system._extract_intent(text, lang)
        print(f"   - Texte: '{text}' ({lang})")
        print(f"     Intention: {intent_result['intent']}")
        print(f"     Confiance: {intent_result['confidence']}")
        if intent_result['entities']:
            print(f"     Entités: {intent_result['entities']}")
    
    # Test 3: Synthèse vocale
    print("\n3. Test de synthèse vocale:")
    test_synthesis = [
        ("Bonjour, je suis Fidelo votre assistant shopping", "fr"),
        ("Hello, I am Fidelo your shopping assistant", "en")
    ]
    
    for text, lang in test_synthesis:
        print(f"   - Génération: '{text}' ({lang})")
        try:
            result = await voice_system.generate_speech(text, lang, "wav")
            if result["success"]:
                print(f"     ✅ Succès - Taille audio: {len(result['audio_data'])} caractères")
            else:
                print(f"     ❌ Échec: {result['error']}")
        except Exception as e:
            print(f"     ❌ Erreur: {e}")
    
    # Test 4: Validation de fichiers audio
    print("\n4. Test de validation de fichiers audio:")
    
    # Créer un fichier audio de test simple (simulation)
    test_audio_data = b'\x1a\x45\xdf\xa3' + b'\x00' * 100  # Header WebM + données
    
    formats_to_test = ['webm', 'mp3', 'wav', 'invalid']
    for fmt in formats_to_test:
        is_valid = voice_system.validate_audio_file(test_audio_data, fmt)
        print(f"   - Format {fmt}: {'✅ Valide' if is_valid else '❌ Invalide'}")
    
    # Test 5: Conversion audio (si ffmpeg disponible)
    if voice_system.ffmpeg_available:
        print("\n5. Test de conversion audio:")
        try:
            # Créer un fichier audio de test plus réaliste
            test_wav_data = b'RIFF' + b'\x00' * 100  # Header WAV
            
            converted = await voice_system._convert_to_wav(test_wav_data, "wav")
            if converted:
                print("   ✅ Conversion WAV réussie")
            else:
                print("   ❌ Échec de conversion WAV")
        except Exception as e:
            print(f"   ❌ Erreur conversion: {e}")
    else:
        print("\n5. Test de conversion audio: FFmpeg non disponible")
    
    print("\n" + "=" * 50)
    print("✅ Tests terminés!")

async def test_voice_endpoints():
    """Test des endpoints vocaux via HTTP"""
    
    print("\n🌐 Test des endpoints vocaux")
    print("=" * 50)
    
    import httpx
    
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        # Test 1: Health check
        print("\n1. Test health check:")
        try:
            response = await client.get(f"{base_url}/voice/health")
            if response.status_code == 200:
                health_data = response.json()
                print(f"   ✅ Statut: {health_data['status']}")
                print(f"   FFmpeg: {health_data['ffmpeg_available']}")
            else:
                print(f"   ❌ Erreur: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Erreur connexion: {e}")
        
        # Test 2: Capacités
        print("\n2. Test capacités:")
        try:
            response = await client.get(f"{base_url}/voice/capabilities")
            if response.status_code == 200:
                caps_data = response.json()
                print(f"   ✅ Système: {caps_data['system']}")
                print(f"   Capacités: {', '.join(caps_data['capabilities'])}")
            else:
                print(f"   ❌ Erreur: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
        
        # Test 3: Extraction d'intention
        print("\n3. Test extraction d'intention:")
        try:
            intent_data = {
                "text": "Cherche des téléphones",
                "language": "fr"
            }
            response = await client.post(f"{base_url}/voice/intent", json=intent_data)
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Intention: {result['intent']}")
                print(f"   Confiance: {result['confidence']}")
            else:
                print(f"   ❌ Erreur: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
        
        # Test 4: Synthèse vocale
        print("\n4. Test synthèse vocale:")
        try:
            synthesis_data = {
                "text": "Bonjour, je suis Fidelo",
                "language": "fr",
                "output_format": "wav"
            }
            response = await client.post(f"{base_url}/voice/synthesize", json=synthesis_data)
            if response.status_code == 200:
                result = response.json()
                if result['success']:
                    print(f"   ✅ Audio généré - Taille: {len(result['audio_data'])} caractères")
                else:
                    print(f"   ❌ Échec: {result['error']}")
            else:
                print(f"   ❌ Erreur: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Erreur: {e}")

def main():
    """Fonction principale"""
    print("🚀 Démarrage des tests du système vocal")
    
    # Test du système local
    asyncio.run(test_voice_system())
    
    # Test des endpoints (si le serveur est en cours d'exécution)
    print("\n" + "=" * 60)
    print("Note: Pour tester les endpoints, assurez-vous que le serveur FastAPI est en cours d'exécution")
    print("Commande: cd SMA && python -m uvicorn core.main:app --reload")
    
    # Demander si l'utilisateur veut tester les endpoints
    try:
        response = input("\nVoulez-vous tester les endpoints vocaux? (y/n): ").lower()
        if response in ['y', 'yes', 'o', 'oui']:
            asyncio.run(test_voice_endpoints())
    except KeyboardInterrupt:
        print("\n\nTests interrompus par l'utilisateur")
    
    print("\n🎉 Tests terminés!")

if __name__ == "__main__":
    main()











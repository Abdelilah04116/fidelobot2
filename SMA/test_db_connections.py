"""
Script de test pour vérifier les connexions aux bases de données
PostgreSQL et Qdrant
"""

import asyncio
import logging
from core.db_connection import health_check, get_postgres_session, get_qdrant_client

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_postgres_connection():
    """Test de la connexion PostgreSQL"""
    print("🔍 Test de la connexion PostgreSQL...")
    
    try:
        with get_postgres_session() as session:
            # Test simple
            result = session.execute("SELECT 1 as test")
            row = result.fetchone()
            print(f"✅ PostgreSQL OK - Test query: {row[0]}")
            
            # Test des tables
            tables_result = session.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
            tables = [row[0] for row in tables_result.fetchall()]
            print(f"📋 Tables disponibles: {', '.join(tables)}")
            
            # Test de la table produits
            if 'produits' in tables:
                count_result = session.execute("SELECT COUNT(*) FROM produits")
                count = count_result.fetchone()[0]
                print(f"📦 Nombre de produits: {count}")
            
            return True
            
    except Exception as e:
        print(f"❌ Erreur PostgreSQL: {str(e)}")
        return False

async def test_qdrant_connection():
    """Test de la connexion Qdrant"""
    print("\n🔍 Test de la connexion Qdrant...")
    
    try:
        client = get_qdrant_client()
        
        # Test des collections
        collections = client.get_collections()
        print(f"✅ Qdrant OK - Collections trouvées: {len(collections.collections)}")
        
        for collection in collections.collections:
            print(f"📁 Collection: {collection.name}")
            
            # Test de recherche dans chaque collection
            try:
                # Recherche simple (avec un vecteur factice pour test)
                test_vector = [0.1] * 384  # Vecteur de test
                search_result = client.search(
                    collection_name=collection.name,
                    query_vector=test_vector,
                    limit=1
                )
                print(f"   🔍 Recherche OK - {len(search_result)} résultats")
                
            except Exception as search_error:
                print(f"   ⚠️ Erreur recherche: {str(search_error)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur Qdrant: {str(e)}")
        return False

async def test_health_check():
    """Test de la fonction health_check"""
    print("\n🔍 Test de la fonction health_check...")
    
    try:
        status = health_check()
        print("📊 État des connexions:")
        
        for db_name, db_status in status.items():
            status_emoji = "✅" if db_status["status"] == "healthy" else "❌"
            print(f"   {status_emoji} {db_name.upper()}: {db_status['status']}")
            if db_status.get("error"):
                print(f"      Erreur: {db_status['error']}")
        
        return all(db_status["status"] == "healthy" for db_status in status.values())
        
    except Exception as e:
        print(f"❌ Erreur health_check: {str(e)}")
        return False

async def test_agent_integration():
    """Test d'intégration avec un agent"""
    print("\n🔍 Test d'intégration avec ProductSearchAgent...")
    
    try:
        from agents.product_search_agent import ProductSearchAgent
        
        agent = ProductSearchAgent()
        
        # Test avec un état simple
        test_state = {
            "user_message": "smartphone",
            "session_id": "test-session",
            "limit": 5
        }
        
        result = await agent.execute(test_state)
        
        print(f"✅ Agent test OK")
        print(f"   Produits trouvés: {len(result.get('products', []))}")
        print(f"   Réponse: {result.get('response_text', '')[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test agent: {str(e)}")
        return False

async def main():
    """Fonction principale de test"""
    print("🚀 Démarrage des tests de connexion aux bases de données\n")
    
    tests = [
        ("Health Check", test_health_check),
        ("PostgreSQL", test_postgres_connection),
        ("Qdrant", test_qdrant_connection),
        ("Intégration Agent", test_agent_integration)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = await test_func()
        except Exception as e:
            print(f"❌ Erreur dans {test_name}: {str(e)}")
            results[test_name] = False
    
    # Résumé
    print("\n" + "="*50)
    print("📋 RÉSUMÉ DES TESTS")
    print("="*50)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 TOUS LES TESTS SONT PASSÉS !")
        print("✅ Votre couche d'abstraction des bases de données fonctionne correctement.")
    else:
        print("⚠️ CERTAINS TESTS ONT ÉCHOUÉ")
        print("🔧 Vérifiez votre configuration et vos connexions.")
    print("="*50)

if __name__ == "__main__":
    asyncio.run(main())

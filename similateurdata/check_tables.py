#!/usr/bin/env python3
"""
Script de vérification des tables dans Postgres
"""

import sys
import os

# Ajouter le dossier parent au PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from catalogue.backend.database import engine
from sqlalchemy import text

def check_tables():
    """Vérifier que toutes les tables nécessaires existent"""
    
    # Liste des tables attendues
    expected_tables = [
        "categories",
        "produits", 
        "utilisateurs",
        "commandes",
        "commande_produits",
        "paniers",
        "panier_produits",
        "tickets_service_client",
        "durabilite"
    ]
    
    print("🔍 Vérification des tables dans Postgres...")
    print("=" * 50)
    
    try:
        with engine.connect() as conn:
            # Récupérer la liste des tables existantes
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            
            existing_tables = [row[0] for row in result]
            
            print(f"Tables trouvées ({len(existing_tables)}):")
            for table in existing_tables:
                print(f"  ✓ {table}")
            
            print(f"\nTables attendues ({len(expected_tables)}):")
            missing_tables = []
            for table in expected_tables:
                if table in existing_tables:
                    print(f"  ✅ {table}")
                else:
                    print(f"  ❌ {table} - MANQUANTE")
                    missing_tables.append(table)
            
            # Vérifier le nombre de lignes dans chaque table
            print(f"\n📊 Nombre de lignes par table:")
            for table in existing_tables:
                try:
                    count_result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = count_result.scalar()
                    print(f"  {table}: {count} lignes")
                except Exception as e:
                    print(f"  {table}: Erreur - {e}")
            
            if missing_tables:
                print(f"\n❌ {len(missing_tables)} table(s) manquante(s): {', '.join(missing_tables)}")
                print("\n💡 Solution: Créer les tables avec:")
                print("   uvicorn catalogue.backend.main:app --reload")
                return False
            else:
                print(f"\n✅ Toutes les {len(expected_tables)} tables sont présentes!")
                return True
                
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        print("\n💡 Vérifiez que:")
        print("   1. Postgres est démarré (docker-compose up -d)")
        print("   2. Les variables d'environnement sont correctes")
        return False

def check_connection():
    """Vérifier la connexion à la base"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Connexion à Postgres réussie")
            return True
    except Exception as e:
        print(f"❌ Impossible de se connecter à Postgres: {e}")
        return False

if __name__ == "__main__":
    print("🎯 VÉRIFICATEUR DE TABLES POSTGRES")
    print("=" * 50)
    
    if check_connection():
        check_tables()
    else:
        print("\n🔧 Actions recommandées:")
        print("   1. Démarrer Postgres: docker-compose -f catalogue/docker-compose.yml up -d")
        print("   2. Attendre que le service soit prêt")
        print("   3. Relancer ce script")

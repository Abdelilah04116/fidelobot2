#!/usr/bin/env python3
"""
Script simple pour créer les tables dans Postgres
"""

import sys
import os

# Ajouter le dossier parent au PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from catalogue.backend.database import Base, engine

def create_tables():
    """Créer toutes les tables définies dans les modèles"""
    print("🚀 Création des tables dans Postgres...")
    
    try:
        # Créer toutes les tables
        Base.metadata.create_all(bind=engine)
        print("✅ Toutes les tables ont été créées avec succès!")
        
        # Vérifier que les tables existent
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            
            tables = [row[0] for row in result]
            print(f"\n📋 Tables créées ({len(tables)}):")
            for table in tables:
                print(f"  ✓ {table}")
                
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🎯 CRÉATEUR DE TABLES POSTGRES")
    print("=" * 50)
    
    if create_tables():
        print("\n🎉 Tables créées! Tu peux maintenant lancer la simulation.")
        print("💡 Commande: python similateurdata/run_all.py")
    else:
        print("\n❌ Échec de la création des tables.")
        print("💡 Vérifiez que Postgres est démarré et accessible.")

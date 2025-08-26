#!/usr/bin/env python3
"""
Script de debug pour vérifier la connexion et les modèles
"""

import sys
import os

# Ajouter le dossier parent au PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from catalogue.backend.database import engine, Base
from catalogue.backend.models import Category, Product, Utilisateur

def debug_connection():
    """Debug de la connexion et des modèles"""
    print("🔍 DEBUG CONNEXION ET MODÈLES")
    print("=" * 50)
    
    # Test de connexion
    try:
        with engine.connect() as conn:
            print("✅ Connexion à Postgres réussie")
            
            # Test simple
            from sqlalchemy import text
            result = conn.execute(text("SELECT 1"))
            print("✅ Requête simple réussie")
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False
    
    # Vérifier les modèles
    print(f"\n📋 Modèles disponibles:")
    print(f"  - Base: {Base}")
    print(f"  - Category: {Category}")
    print(f"  - Product: {Product}")
    print(f"  - Utilisateur: {Utilisateur}")
    
    # Vérifier les métadonnées
    print(f"\n🔧 Métadonnées des modèles:")
    print(f"  - Tables dans Base.metadata: {list(Base.metadata.tables.keys())}")
    
    return True

def try_create_tables():
    """Essayer de créer les tables avec plus de détails"""
    print(f"\n🚀 TENTATIVE DE CRÉATION DES TABLES")
    print("=" * 50)
    
    try:
        # Créer les tables
        Base.metadata.create_all(bind=engine)
        print("✅ Base.metadata.create_all() exécuté sans erreur")
        
        # Vérifier immédiatement
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            
            tables = [row[0] for row in result]
            print(f"\n📋 Tables trouvées après création ({len(tables)}):")
            for table in tables:
                print(f"  ✓ {table}")
                
            if len(tables) == 0:
                print("⚠️  Aucune table créée - problème avec les modèles")
                return False
                
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    if debug_connection():
        try_create_tables()
    else:
        print("\n❌ Impossible de continuer sans connexion")

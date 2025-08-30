#!/usr/bin/env python3
"""
Script de test simple pour vérifier la connexion à PostgreSQL
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Configuration PostgreSQL
postgres_host = 'localhost'
postgres_port = '5432'
postgres_user = 'catalogue_user'
postgres_password = 'catalogue_pass'
postgres_db = 'catalogue'

# URL de connexion PostgreSQL
postgres_url = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"

print(f"🔍 Test de connexion à PostgreSQL...")
print(f"URL: {postgres_url}")

try:
    # Créer l'engine PostgreSQL
    engine = create_engine(postgres_url, echo=True)
    
    # Créer une session
    SessionLocal = sessionmaker(bind=engine)
    
    with SessionLocal() as session:
        # Test 1: Connexion simple
        print("\n✅ Test 1: Connexion simple")
        result = session.execute(text("SELECT 1 as test"))
        print(f"Résultat: {result.fetchone()[0]}")
        
        # Test 2: Lister les tables
        print("\n✅ Test 2: Lister les tables")
        result = session.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))
        tables = [row[0] for row in result.fetchall()]
        print(f"Tables trouvées: {tables}")
        
        # Test 3: Compter les produits
        if 'produits' in tables:
            print("\n✅ Test 3: Compter les produits")
            result = session.execute(text("SELECT COUNT(*) FROM produits"))
            count = result.fetchone()[0]
            print(f"Nombre de produits: {count}")
            
            # Test 4: Lister quelques produits
            print("\n✅ Test 4: Lister quelques produits")
            result = session.execute(text("SELECT id, nom, prix FROM produits LIMIT 5"))
            products = result.fetchall()
            for product in products:
                print(f"  - ID: {product[0]}, Nom: {product[1]}, Prix: {product[2]}")
        
        # Test 5: Compter les catégories
        if 'categories' in tables:
            print("\n✅ Test 5: Compter les catégories")
            result = session.execute(text("SELECT COUNT(*) FROM categories"))
            count = result.fetchone()[0]
            print(f"Nombre de catégories: {count}")
    
    print("\n🎉 Tous les tests sont passés !")
    
except Exception as e:
    print(f"\n❌ Erreur: {str(e)}")
    import traceback
    traceback.print_exc()



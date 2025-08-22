import sys
import os

# Ajouter le chemin du projet pour l'import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from catalogue.database.catalog_database import catalog_db
    from catalogue.database.catalog_models import Product, Category
    
    print("🔍 Test de la base de données...")
    
    # Créer une session
    session = catalog_db.get_session_direct()
    
    # Compter les produits
    total_products = session.query(Product).count()
    print(f"✅ Total produits: {total_products}")
    
    # Compter les catégories
    total_categories = session.query(Category).count()
    print(f"✅ Total catégories: {total_categories}")
    
    # Afficher quelques produits
    if total_products > 0:
        print("\n📦 Exemples de produits:")
        products = session.query(Product).limit(3).all()
        for i, prod in enumerate(products, 1):
            print(f"  {i}. {prod.name} - {prod.base_price}€")
    
    session.close()
    print("\n🎉 Test réussi !")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()







import sys
import os

# Ajoute la racine du projet au PYTHONPATH pour l'import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from catalogue.database.catalog_database import catalog_db
from catalogue.database.catalog_models import Product, Category

def verify_import():
    """Vérifie que les produits ont bien été importés"""
    
    try:
        session = catalog_db.get_session_direct()
        
        # Compter les produits
        total_products = session.query(Product).count()
        print(f"✅ Total produits dans la base: {total_products}")
        
        # Compter les catégories
        total_categories = session.query(Category).count()
        print(f"✅ Total catégories dans la base: {total_categories}")
        
        # Afficher les catégories disponibles
        print("\n📂 Catégories disponibles:")
        categories = session.query(Category).all()
        for cat in categories:
            product_count = session.query(Product).filter(Product.category_id == cat.id).count()
            print(f"  - {cat.name}: {product_count} produits")
        
        # Afficher quelques exemples de produits
        print(f"\n📦 Exemples de produits (premiers 5):")
        products = session.query(Product).limit(5).all()
        for i, prod in enumerate(products, 1):
            category = session.query(Category).filter(Category.id == prod.category_id).first()
            print(f"  {i}. {prod.name}")
            print(f"     Prix: {prod.base_price}€")
            print(f"     Stock: {prod.stock_quantity}")
            print(f"     Catégorie: {category.name if category else 'Inconnue'}")
            print()
        
        # Rechercher par catégorie (exemple)
        print("🔍 Test de recherche par catégorie:")
        category_name = "Électronique"
        category = session.query(Category).filter(Category.name == category_name).first()
        if category:
            products_in_category = session.query(Product).filter(Product.category_id == category.id).count()
            print(f"  Produits dans la catégorie '{category_name}': {products_in_category}")
        else:
            print(f"  Catégorie '{category_name}' non trouvée")
        
        session.close()
        
        if total_products > 0:
            print(f"\n🎉 Import réussi ! {total_products} produits sont maintenant disponibles dans la base de données.")
            print("L'agent product_search_agent peut maintenant rechercher ces produits.")
        else:
            print("\n❌ Aucun produit trouvé dans la base de données.")
            
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")

if __name__ == "__main__":
    print("🔍 Vérification de l'import des produits...")
    verify_import()







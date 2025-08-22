import json
import csv
import sys
import os
import pandas as pd
import shutil
from pathlib import Path
from datetime import datetime

# Ajoute la racine du projet au PYTHONPATH pour l'import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from catalogue.database.catalog_database import catalog_db
from catalogue.database.catalog_models import Product, Category, Brand, User, ProductStatus

def import_from_excel(excel_file, table_name):
    """Importe des données depuis un fichier Excel"""
    
    try:
        print(f"📁 Lecture du fichier Excel: {excel_file}")
        
        # Lire le fichier Excel avec pandas
        df = pd.read_excel(excel_file, engine='openpyxl')
        print(f"✅ {len(df)} lignes lues depuis {excel_file}")
        
        # Créer une session de base de données
        session = catalog_db.get_session_direct()
        
        if table_name.lower() == "products":
            import_products_from_dataframe(df, session)
        elif table_name.lower() == "categories":
            import_categories_from_dataframe(df, session)
        elif table_name.lower() == "brands":
            import_brands_from_dataframe(df, session)
        elif table_name.lower() == "users":
            import_users_from_dataframe(df, session)
        else:
            print(f"❌ Table '{table_name}' non supportée. Tables supportées: products, categories, brands, users")
            return
        
        session.close()
        print(f"🎉 Import terminé pour la table {table_name}!")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'import Excel: {e}")

def import_from_csv(csv_file, table_name):
    """Importe des données depuis un fichier CSV"""
    
    try:
        print(f"📁 Lecture du fichier CSV: {csv_file}")
        
        # Lire le fichier CSV avec pandas
        df = pd.read_csv(csv_file, encoding='utf-8')
        print(f"✅ {len(df)} lignes lues depuis {csv_file}")
        
        # Créer une session de base de données
        session = catalog_db.get_session_direct()
        
        if table_name.lower() == "products":
            import_products_from_dataframe(df, session)
        elif table_name.lower() == "categories":
            import_categories_from_dataframe(df, session)
        elif table_name.lower() == "brands":
            import_brands_from_dataframe(df, session)
        elif table_name.lower() == "users":
            import_users_from_dataframe(df, session)
        else:
            print(f"❌ Table '{table_name}' non supportée. Tables supportées: products, categories, brands, users")
            return
        
        session.close()
        print(f"🎉 Import terminé pour la table {table_name}!")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'import CSV: {e}")

def import_users_from_dataframe(df, session):
    """Importe les utilisateurs depuis un DataFrame"""
    
    for index, row in df.iterrows():
        try:
            # Traiter l'avatar si il existe
            avatar_url = process_image(row.get('avatar_url', row.get('avatar', '')), row.get('username', row.get('email', '')))
            
            # Traiter la date de naissance si elle existe
            date_of_birth = None
            if row.get('date_of_birth') and pd.notna(row.get('date_of_birth')):
                try:
                    if isinstance(row.get('date_of_birth'), str):
                        date_of_birth = pd.to_datetime(row.get('date_of_birth')).to_pydatetime()
                    else:
                        date_of_birth = row.get('date_of_birth').to_pydatetime()
                except:
                    date_of_birth = None
            
            user = User(
                email=row.get('email', f"user{index+1}@example.com"),
                username=row.get('username', row.get('nom_utilisateur', f"user{index+1}")),
                is_active=bool(row.get('is_active', True))
            )
            
            session.add(user)
            
            if (index + 1) % 50 == 0:
                session.commit()
                print(f"👤 Importé {index + 1} utilisateurs...")
                
        except Exception as e:
            print(f"⚠️ Erreur utilisateur {index+1}: {e}")
            session.rollback()
            continue
    
    session.commit()

def import_products_from_dataframe(df, session):
    """Importe les produits depuis un DataFrame (CSV ou Excel)"""
    
    # Dictionnaire pour stocker les catégories existantes
    categories = {}
    
    for index, row in df.iterrows():
        try:
            # Gérer la catégorie
            category_name = row.get('catégorie', row.get('category', 'Général'))
            if category_name not in categories:
                category = session.query(Category).filter(Category.name == category_name).first()
                if not category:
                    category = Category(
                        name=category_name,
                        slug=category_name.lower().replace(" ", "-"),
                        description=f"Catégorie {category_name}",
                        is_active=True
                    )
                    session.add(category)
                    session.flush()
                categories[category_name] = category.id
            
            # Traiter l'image si elle existe
            image_url = process_image(row.get('image_url', row.get('image', '')), row.get('nom', row.get('name', '')))
            
            # Créer le produit
            product = Product(
                sku=str(row.get('sku', row.get('id_produit', f"SKU-{index+1}"))),
                name=row.get('nom', row.get('name', 'Produit sans nom')),
                slug=str(row.get('nom', row.get('name', 'produit-sans-nom'))).lower().replace(" ", "-"),
                description=row.get('description', ''),
                short_description=str(row.get('description', ''))[:200] + "..." if len(str(row.get('description', ''))) > 200 else str(row.get('description', '')),
                base_price=float(row.get('prix', row.get('price', 0))),
                stock_quantity=int(row.get('stock', row.get('quantity', 0))),
                category_id=categories[category_name],
                main_image_url=image_url,
                status=ProductStatus.ACTIVE
            )
            
            session.add(product)
            
            # Commit tous les 100 produits
            if (index + 1) % 100 == 0:
                session.commit()
                print(f"📦 Importé {index + 1} produits...")
                
        except Exception as e:
            print(f"⚠️ Erreur produit {index+1}: {e}")
            session.rollback()
            continue
    
    session.commit()

def import_categories_from_dataframe(df, session):
    """Importe les catégories depuis un DataFrame"""
    
    for index, row in df.iterrows():
        try:
            # Traiter l'image de catégorie si elle existe
            image_url = process_image(row.get('image_url', row.get('image', '')), row.get('nom', row.get('name', '')))
            
            category = Category(
                name=row.get('nom', row.get('name', 'Catégorie sans nom')),
                slug=str(row.get('nom', row.get('name', 'categorie-sans-nom'))).lower().replace(" ", "-"),
                description=row.get('description', ''),
                image_url=image_url,
                is_active=bool(row.get('is_active', True))
            )
            
            session.add(category)
            
            if (index + 1) % 50 == 0:
                session.commit()
                print(f"📂 Importé {index + 1} catégories...")
                
        except Exception as e:
            print(f"⚠️ Erreur catégorie {index+1}: {e}")
            session.rollback()
            continue
    
    session.commit()

def import_brands_from_dataframe(df, session):
    """Importe les marques depuis un DataFrame"""
    
    for index, row in df.iterrows():
        try:
            # Traiter le logo si il existe
            logo_url = process_image(row.get('logo_url', row.get('logo', '')), row.get('nom', row.get('name', '')))
            
            brand = Brand(
                name=row.get('nom', row.get('name', 'Marque sans nom')),
                slug=str(row.get('nom', row.get('name', 'marque-sans-nom'))).lower().replace(" ", "-"),
                description=row.get('description', ''),
                logo_url=logo_url,
                website=row.get('website', ''),
                is_active=bool(row.get('is_active', True))
            )
            
            session.add(brand)
            
            if (index + 1) % 50 == 0:
                session.commit()
                print(f"🏷️ Importé {index + 1} marques...")
                
        except Exception as e:
            print(f"⚠️ Erreur marque {index+1}: {e}")
            session.rollback()
            continue
    
    session.commit()

def process_image(image_path, item_name):
    """Traite et copie les images dans le dossier approprié"""
    
    if not image_path or pd.isna(image_path):
        return ""
    
    try:
        # Créer le dossier images s'il n'existe pas
        images_dir = Path("images")
        images_dir.mkdir(exist_ok=True)
        
        # Si c'est une URL, la retourner telle quelle
        if image_path.startswith(('http://', 'https://')):
            return image_path
        
        # Si c'est un chemin local, copier l'image
        source_path = Path(image_path)
        if source_path.exists():
            # Générer un nom de fichier unique
            extension = source_path.suffix
            safe_name = "".join(c for c in item_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_')
            new_filename = f"{safe_name}_{hash(image_path) % 10000}{extension}"
            dest_path = images_dir / new_filename
            
            # Copier l'image
            shutil.copy2(source_path, dest_path)
            print(f"🖼️ Image copiée: {source_path} -> {dest_path}")
            
            return str(dest_path)
        else:
            print(f"⚠️ Image non trouvée: {image_path}")
            return ""
            
    except Exception as e:
        print(f"⚠️ Erreur traitement image {image_path}: {e}")
        return ""

def import_from_json(json_file, table_name):
    """Importe des données depuis un fichier JSON"""
    
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        print(f"📁 Lecture de {len(data)} éléments depuis {json_file}")
        
        session = catalog_db.get_session_direct()
        
        if table_name.lower() == "products":
            import_products_from_json(data, session)
        elif table_name.lower() == "users":
            import_users_from_json(data, session)
        else:
            print(f"❌ Table '{table_name}' non supportée pour JSON")
            return
        
        session.close()
        print(f"🎉 Import JSON terminé pour {table_name}!")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'import JSON: {e}")

def import_users_from_json(data, session):
    """Importe les utilisateurs depuis une liste JSON"""
    
    for i, user_data in enumerate(data):
        try:
            # Traiter l'avatar
            avatar_url = process_image(user_data.get("avatar_url"), user_data.get("username", user_data.get("email", "")))
            
            # Traiter la date de naissance
            date_of_birth = None
            if user_data.get('date_of_birth'):
                try:
                    date_of_birth = pd.to_datetime(user_data.get('date_of_birth')).to_pydatetime()
                except:
                    date_of_birth = None
            
            user = User(
                email=user_data.get("email", f"user{i+1}@example.com"),
                username=user_data.get("username", user_data.get("nom_utilisateur", f"user{i+1}")),
                is_active=bool(user_data.get("is_active", True))
            )
            
            session.add(user)
            
            if (i + 1) % 50 == 0:
                session.commit()
                print(f"👤 Importé {i + 1} utilisateurs...")
                
        except Exception as e:
            print(f"⚠️ Erreur utilisateur {i+1}: {e}")
            session.rollback()
            continue
    
    session.commit()

def import_products_from_json(data, session):
    """Importe les produits depuis une liste JSON"""
    
    categories = {}
    
    for i, prod in enumerate(data):
        try:
            category_name = prod.get("catégorie", "Général")
            if category_name not in categories:
                category = session.query(Category).filter(Category.name == category_name).first()
                if not category:
                    category = Category(
                        name=category_name,
                        slug=category_name.lower().replace(" ", "-"),
                        description=f"Catégorie {category_name}",
                        is_active=True
                    )
                    session.add(category)
                    session.flush()
                categories[category_name] = category.id
            
            # Traiter l'image
            image_url = process_image(prod.get("image_url"), prod.get("nom", ""))
            
            product = Product(
                sku=f"SKU-{prod.get('id_produit', i+1)}",
                name=prod.get("nom", "Produit sans nom"),
                slug=prod.get("nom", "produit-sans-nom").lower().replace(" ", "-"),
                description=prod.get("description", ""),
                short_description=prod.get("description", "")[:200] + "..." if len(prod.get("description", "")) > 200 else prod.get("description", ""),
                base_price=float(prod.get("prix", 0)),
                stock_quantity=int(prod.get("stock", 0)),
                category_id=categories[category_name],
                main_image_url=image_url,
                status=ProductStatus.ACTIVE
            )
            
            session.add(product)
            
            if (i + 1) % 100 == 0:
                session.commit()
                print(f"📦 Importé {i + 1} produits...")
                
        except Exception as e:
            print(f"⚠️ Erreur produit {i+1}: {e}")
            session.rollback()
            continue
    
    session.commit()

def main():
    """Fonction principale pour l'import"""
    
    print("🚀 Script d'import universel pour le catalogue")
    print("=" * 50)
    
    # Vérifier les arguments
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python import_data.py <fichier> <table>")
        print("")
        print("Exemples:")
        print("  python import_data.py produits.csv products")
        print("  python import_data.py produits.xlsx products")
        print("  python import_data.py categories.csv categories")
        print("  python import_data.py marques.xlsx brands")
        print("  python import_data.py utilisateurs.csv users")
        print("  python import_data.py produits.json products")
        print("  python import_data.py utilisateurs.json users")
        print("")
        print("Formats supportés:")
        print("  📊 CSV (.csv)")
        print("  📈 Excel (.xlsx, .xls)")
        print("  📄 JSON (.json)")
        print("")
        print("Tables supportées: products, categories, brands, users")
        print("")
        print("Fonctionnalités:")
        print("  🖼️ Traitement automatique des images")
        print("  👤 Support des utilisateurs avec avatars")
        print("  🔄 Support des noms de colonnes en français et anglais")
        print("  ⚡ Import par lots pour optimiser les performances")
        print("  📅 Traitement automatique des dates")
        return
    
    file_path = sys.argv[1]
    table_name = sys.argv[2]
    
    # Vérifier que le fichier existe
    if not os.path.exists(file_path):
        print(f"❌ Fichier '{file_path}' non trouvé!")
        return
    
    # Détecter le type de fichier et importer
    file_extension = file_path.lower()
    
    if file_extension.endswith('.csv'):
        import_from_csv(file_path, table_name)
    elif file_extension.endswith(('.xlsx', '.xls')):
        import_from_excel(file_path, table_name)
    elif file_extension.endswith('.json'):
        import_from_json(file_path, table_name)
    else:
        print(f"❌ Format de fichier non supporté: {file_path}")
        print("Formats supportés: .csv, .xlsx, .xls, .json")

if __name__ == "__main__":
    main()

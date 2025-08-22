
"""Script pour initialiser la base de données avec des données de test"""

from models.database import SessionLocal, User, Product, Order, OrderItem, Rating
from auth import get_password_hash
import random

def setup_test_data():
    """Initialiser la base avec des données de test"""
    db = SessionLocal()
    
    try:
        # Créer des utilisateurs de test
        test_users = [
            {
                "email": "alice@example.com",
                "username": "alice",
                "password": "password123",
                "is_vip": True,
                "preferences": {
                    "preferred_brands": ["Apple", "Samsung"],
                    "favorite_categories": ["électronique", "mode"]
                }
            },
            {
                "email": "bob@example.com",
                "username": "bob",
                "password": "password123",
                "is_vip": False,
                "preferences": {
                    "preferred_brands": ["Nike", "Adidas"],
                    "favorite_categories": ["sport", "mode"]
                }
            },
            {
                "email": "charlie@example.com",
                "username": "charlie",
                "password": "password123",
                "is_vip": False,
                "preferences": {}
            }
        ]
        
        created_users = []
        for user_data in test_users:
            existing_user = db.query(User).filter(User.email == user_data["email"]).first()
            if not existing_user:
                user = User(
                    email=user_data["email"],
                    username=user_data["username"],
                    hashed_password=get_password_hash(user_data["password"]),
                    is_vip=user_data["is_vip"],
                    preferences=user_data["preferences"]
                )
                db.add(user)
                created_users.append(user)
        
        db.commit()
        
        # Récupérer tous les utilisateurs pour les IDs
        all_users = db.query(User).all()
        
        # Créer des produits de test
        test_products = [
            {
                "name": "iPhone 15 Pro",
                "description": "Le dernier smartphone Apple avec puce A17 Pro",
                "price": 1229.00,
                "category": "électronique",
                "brand": "Apple",
                "stock_quantity": 25,
                "image_url": "/images/iphone15pro.jpg",
                "specifications": {
                    "écran": "6.1 pouces",
                    "stockage": "128GB",
                    "couleur": "Titane naturel"
                }
            },
            {
                "name": "Samsung Galaxy S24",
                "description": "Smartphone Android premium avec intelligence artificielle",
                "price": 899.00,
                "category": "électronique",
                "brand": "Samsung",
                "stock_quantity": 30,
                "image_url": "/images/galaxys24.jpg",
                "specifications": {
                    "écran": "6.2 pouces",
                    "stockage": "256GB",
                    "couleur": "Violet"
                }
            },
            {
                "name": "MacBook Air M3",
                "description": "Ordinateur portable ultra-fin avec puce M3",
                "price": 1599.00,
                "category": "électronique",
                "brand": "Apple",
                "stock_quantity": 15,
                "image_url": "/images/macbookair.jpg",
                "specifications": {
                    "processeur": "Apple M3",
                    "mémoire": "16GB",
                    "stockage": "512GB SSD"
                }
            },
            {
                "name": "Nike Air Max 270",
                "description": "Chaussures de sport confortables avec amorti Air",
                "price": 149.99,
                "category": "sport",
                "brand": "Nike",
                "stock_quantity": 50,
                "image_url": "/images/airmax270.jpg",
                "specifications": {
                    "type": "Running",
                    "matière": "Mesh et cuir synthétique",
                    "couleur": "Noir/Blanc"
                }
            },
            {
                "name": "Adidas Ultraboost 22",
                "description": "Chaussures de running haute performance",
                "price": 189.99,
                "category": "sport", 
                "brand": "Adidas",
                "stock_quantity": 40,
                "image_url": "/images/ultraboost.jpg",
                "specifications": {
                    "type": "Running",
                    "technologie": "Boost",
                    "couleur": "Blanc/Noir"
                }
            },
            {
                "name": "Canapé Scandinave 3 places",
                "description": "Canapé design en tissu gris clair",
                "price": 899.00,
                "category": "maison",
                "brand": "IKEA",
                "stock_quantity": 8,
                "image_url": "/images/canape.jpg",
                "specifications": {
                    "dimensions": "200x85x90 cm",
                    "matière": "Tissu polyester",
                    "couleur": "Gris clair"
                }
            },
            {
                "name": "T-shirt Bio Homme",
                "description": "T-shirt en coton biologique certifié",
                "price": 29.99,
                "category": "mode",
                "brand": "Patagonia",
                "stock_quantity": 100,
                "image_url": "/images/tshirt.jpg",
                "specifications": {
                    "matière": "100% coton bio",
                    "tailles": "S, M, L, XL",
                    "couleur": "Bleu marine"
                }
            },
            {
                "name": "Casque Sony WH-1000XM5",
                "description": "Casque à réduction de bruit active premium",
                "price": 399.99,
                "category": "électronique",
                "brand": "Sony",
                "stock_quantity": 20,
                "image_url": "/images/casque_sony.jpg",
                "specifications": {
                    "type": "Over-ear",
                    "autonomie": "30 heures",
                    "réduction_bruit": "Oui"
                }
            }
        ]
        
        created_products = []
        for product_data in test_products:
            existing_product = db.query(Product).filter(Product.name == product_data["name"]).first()
            if not existing_product:
                product = Product(**product_data)
                db.add(product)
                created_products.append(product)
        
        db.commit()
        
        # Récupérer tous les produits pour les IDs
        all_products = db.query(Product).all()
        
        # Créer des commandes de test
        for user in all_users[:2]:  # Seulement pour Alice et Bob
            # Créer 2-3 commandes par utilisateur
            for order_num in range(random.randint(2, 3)):
                order = Order(
                    user_id=user.id,
                    total_amount=0,
                    status=random.choice(["pending", "confirmed", "shipped", "delivered"])
                )
                db.add(order)
                db.flush()  # Pour obtenir l'ID
                
                # Ajouter 1-3 articles par commande
                total_amount = 0
                for _ in range(random.randint(1, 3)):
                    product = random.choice(all_products)
                    quantity = random.randint(1, 2)
                    
                    order_item = OrderItem(
                        order_id=order.id,
                        product_id=product.id,
                        quantity=quantity,
                        price=product.price
                    )
                    db.add(order_item)
                    total_amount += product.price * quantity
                
                order.total_amount = total_amount
        
        # Créer des évaluations de test
        for user in all_users:
            # Chaque utilisateur évalue 3-5 produits
            products_to_rate = random.sample(all_products, random.randint(3, 5))
            for product in products_to_rate:
                rating = Rating(
                    user_id=user.id,
                    product_id=product.id,
                    rating=random.randint(3, 5),
                    comment=random.choice([
                        "Excellent produit, je recommande !",
                        "Très satisfait de mon achat",
                        "Bonne qualité, livraison rapide",
                        "Conforme à mes attentes",
                        "Parfait pour mes besoins"
                    ])
                )
                db.add(rating)
        
        db.commit()
        
        print("✅ Données de test créées avec succès !")
        print(f"👥 Utilisateurs créés: {len(all_users)}")
        print(f"📦 Produits créés: {len(all_products)}")
        print("🔐 Comptes de test:")
        print("   - alice@example.com / password123 (VIP)")
        print("   - bob@example.com / password123")
        print("   - charlie@example.com / password123")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erreur lors de la création des données: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    setup_test_data()
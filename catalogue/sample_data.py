"""
Données d'exemple pour le catalogue des produits
Permet de tester le système avec des produits, catégories et marques
"""

from typing import Dict, Any, List
from .database.catalog_models import ProductStatus, ProductType

# ==================== DONNÉES D'EXEMPLE ====================

# Catégories principales
SAMPLE_CATEGORIES = [
    {
        "name": "Électronique",
        "slug": "electronique",
        "description": "Produits électroniques et technologiques",
        "image_url": "https://example.com/images/electronics.jpg",
        "sort_order": 1
    },
    {
        "name": "Vêtements",
        "slug": "vetements",
        "description": "Mode et accessoires vestimentaires",
        "image_url": "https://example.com/images/clothing.jpg",
        "sort_order": 2
    },
    {
        "name": "Livres",
        "slug": "livres",
        "description": "Livres, magazines et publications",
        "image_url": "https://example.com/images/books.jpg",
        "sort_order": 3
    },
    {
        "name": "Maison & Jardin",
        "slug": "maison-jardin",
        "description": "Décoration et aménagement",
        "image_url": "https://example.com/images/home-garden.jpg",
        "sort_order": 4
    }
]

# Sous-catégories
SAMPLE_SUBCATEGORIES = [
    {
        "name": "Smartphones",
        "slug": "smartphones",
        "description": "Téléphones intelligents et mobiles",
        "parent_name": "Électronique",
        "image_url": "https://example.com/images/smartphones.jpg",
        "sort_order": 1
    },
    {
        "name": "Ordinateurs",
        "slug": "ordinateurs",
        "description": "PC, laptops et accessoires",
        "parent_name": "Électronique",
        "image_url": "https://example.com/images/computers.jpg",
        "sort_order": 2
    },
    {
        "name": "Homme",
        "slug": "vetements-homme",
        "description": "Vêtements pour hommes",
        "parent_name": "Vêtements",
        "image_url": "https://example.com/images/mens-clothing.jpg",
        "sort_order": 1
    },
    {
        "name": "Femme",
        "slug": "vetements-femme",
        "description": "Vêtements pour femmes",
        "parent_name": "Vêtements",
        "image_url": "https://example.com/images/womens-clothing.jpg",
        "sort_order": 2
    }
]

# Marques
SAMPLE_BRANDS = [
    {
        "name": "Apple",
        "slug": "apple",
        "description": "Technologie et innovation",
        "logo_url": "https://example.com/logos/apple.png",
        "website": "https://www.apple.com"
    },
    {
        "name": "Samsung",
        "slug": "samsung",
        "description": "Électronique grand public",
        "logo_url": "https://example.com/logos/samsung.png",
        "website": "https://www.samsung.com"
    },
    {
        "name": "Nike",
        "slug": "nike",
        "description": "Sport et mode",
        "logo_url": "https://example.com/logos/nike.png",
        "website": "https://www.nike.com"
    },
    {
        "name": "Adidas",
        "slug": "adidas",
        "description": "Sport et lifestyle",
        "logo_url": "https://example.com/logos/adidas.png",
        "website": "https://www.adidas.com"
    }
]

# Produits d'exemple
SAMPLE_PRODUCTS = [
    {
        "sku": "IPHONE-15-PRO",
        "name": "iPhone 15 Pro",
        "slug": "iphone-15-pro",
        "description": "Le dernier iPhone avec puce A17 Pro, appareil photo professionnel et design en titane",
        "short_description": "iPhone 15 Pro - Innovation et performance",
        "product_type": ProductType.PHYSICAL,
        "status": ProductStatus.ACTIVE,
        "base_price": 1199.99,
        "sale_price": 1099.99,
        "cost_price": 800.00,
        "weight": 187.0,
        "dimensions": {"length": 147.6, "width": 71.6, "height": 8.25},
        "stock_quantity": 50,
        "low_stock_threshold": 5,
        "track_stock": True,
        "meta_title": "iPhone 15 Pro - Apple Store",
        "meta_description": "Découvrez l'iPhone 15 Pro avec puce A17 Pro et appareil photo professionnel",
        "meta_keywords": "iPhone, smartphone, Apple, A17 Pro, photo",
        "main_image_url": "https://example.com/products/iphone-15-pro-main.jpg",
        "image_urls": [
            "https://example.com/products/iphone-15-pro-1.jpg",
            "https://example.com/products/iphone-15-pro-2.jpg",
            "https://example.com/products/iphone-15-pro-3.jpg"
        ],
        "category_name": "Smartphones",
        "brand_name": "Apple"
    },
    {
        "sku": "MACBOOK-AIR-M2",
        "name": "MacBook Air M2",
        "slug": "macbook-air-m2",
        "description": "Ordinateur portable ultra-léger avec puce M2, jusqu'à 18h d'autonomie",
        "short_description": "MacBook Air M2 - Performance et mobilité",
        "product_type": ProductType.PHYSICAL,
        "status": ProductStatus.ACTIVE,
        "base_price": 1299.99,
        "sale_price": None,
        "cost_price": 900.00,
        "weight": 1240.0,
        "dimensions": {"length": 304.1, "width": 215.0, "height": 11.3},
        "stock_quantity": 25,
        "low_stock_threshold": 3,
        "track_stock": True,
        "meta_title": "MacBook Air M2 - Apple Store",
        "meta_description": "MacBook Air avec puce M2, ultra-léger et performant",
        "meta_keywords": "MacBook, Air, M2, Apple, ordinateur portable",
        "main_image_url": "https://example.com/products/macbook-air-m2-main.jpg",
        "image_urls": [
            "https://example.com/products/macbook-air-m2-1.jpg",
            "https://example.com/products/macbook-air-m2-2.jpg"
        ],
        "category_name": "Ordinateurs",
        "brand_name": "Apple"
    },
    {
        "sku": "NIKE-AIR-MAX",
        "name": "Nike Air Max 270",
        "slug": "nike-air-max-270",
        "description": "Chaussures de sport avec amorti Air Max visible, confort maximal",
        "short_description": "Nike Air Max 270 - Confort et style",
        "product_type": ProductType.PHYSICAL,
        "status": ProductStatus.ACTIVE,
        "base_price": 149.99,
        "sale_price": 129.99,
        "cost_price": 80.00,
        "weight": 350.0,
        "dimensions": {"length": 30.0, "width": 12.0, "height": 10.0},
        "stock_quantity": 100,
        "low_stock_threshold": 10,
        "track_stock": True,
        "meta_title": "Nike Air Max 270 - Chaussures de sport",
        "meta_description": "Chaussures Nike Air Max 270 avec amorti visible",
        "meta_keywords": "Nike, Air Max, chaussures, sport, confort",
        "main_image_url": "https://example.com/products/nike-air-max-270-main.jpg",
        "image_urls": [
            "https://example.com/products/nike-air-max-270-1.jpg",
            "https://example.com/products/nike-air-max-270-2.jpg"
        ],
        "category_name": "Homme",
        "brand_name": "Nike"
    }
]

# Variantes de produits
SAMPLE_VARIANTS = [
    {
        "sku": "IPHONE-15-PRO-128GB",
        "name": "128GB",
        "attributes": {"storage": "128GB", "color": "Natural Titanium"},
        "price_adjustment": 0.0,
        "stock_quantity": 20,
        "image_url": "https://example.com/products/iphone-15-pro-128gb.jpg"
    },
    {
        "sku": "IPHONE-15-PRO-256GB",
        "name": "256GB",
        "attributes": {"storage": "256GB", "color": "Natural Titanium"},
        "price_adjustment": 100.0,
        "stock_quantity": 15,
        "image_url": "https://example.com/products/iphone-15-pro-256gb.jpg"
    },
    {
        "sku": "MACBOOK-AIR-M2-8GB",
        "name": "8GB RAM",
        "attributes": {"ram": "8GB", "storage": "256GB"},
        "price_adjustment": 0.0,
        "stock_quantity": 15,
        "image_url": "https://example.com/products/macbook-air-m2-8gb.jpg"
    },
    {
        "sku": "MACBOOK-AIR-M2-16GB",
        "name": "16GB RAM",
        "attributes": {"ram": "16GB", "storage": "512GB"},
        "price_adjustment": 300.0,
        "stock_quantity": 10,
        "image_url": "https://example.com/products/macbook-air-m2-16gb.jpg"
    }
]

# Tags de produits
SAMPLE_TAGS = [
    {
        "name": "Nouveau",
        "slug": "nouveau",
        "color": "#28a745",
        "description": "Produits récemment ajoutés"
    },
    {
        "name": "Promotion",
        "slug": "promotion",
        "color": "#ffc107",
        "description": "Produits en promotion"
    },
    {
        "name": "Bestseller",
        "slug": "bestseller",
        "color": "#dc3545",
        "description": "Produits les plus populaires"
    },
    {
        "name": "Éco-responsable",
        "slug": "eco-responsable",
        "color": "#20c997",
        "description": "Produits respectueux de l'environnement"
    }
]

# Avis de produits
SAMPLE_REVIEWS = [
    {
        "rating": 5,
        "title": "Excellent produit !",
        "comment": "L'iPhone 15 Pro dépasse toutes mes attentes. La qualité photo est exceptionnelle.",
        "is_verified_purchase": True,
        "is_approved": True,
        "is_helpful": 12
    },
    {
        "rating": 4,
        "title": "Très satisfait",
        "comment": "Le MacBook Air M2 est rapide et l'autonomie est impressionnante.",
        "is_verified_purchase": True,
        "is_approved": True,
        "is_helpful": 8
    },
    {
        "rating": 5,
        "title": "Chaussures parfaites",
        "comment": "Les Nike Air Max 270 sont très confortables pour la course.",
        "is_verified_purchase": True,
        "is_approved": True,
        "is_helpful": 15
    }
]

def get_sample_data() -> Dict[str, List[Dict[str, Any]]]:
    """
    Retourne toutes les données d'exemple organisées par type
    
    Returns:
        Dict contenant toutes les données d'exemple
    """
    return {
        "categories": SAMPLE_CATEGORIES,
        "subcategories": SAMPLE_SUBCATEGORIES,
        "brands": SAMPLE_BRANDS,
        "products": SAMPLE_PRODUCTS,
        "variants": SAMPLE_VARIANTS,
        "tags": SAMPLE_TAGS,
        "reviews": SAMPLE_REVIEWS
    }

def get_product_with_variants() -> Dict[str, Any]:
    """
    Retourne un produit avec ses variantes pour les tests
    
    Returns:
        Dict contenant un produit et ses variantes
    """
    return {
        "product": SAMPLE_PRODUCTS[0],  # iPhone 15 Pro
        "variants": [
            SAMPLE_VARIANTS[0],  # 128GB
            SAMPLE_VARIANTS[1]   # 256GB
        ]
    }

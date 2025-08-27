#!/usr/bin/env python3
"""
Générateur de données de test pour le domaine de l'électronique
Génère des données pour PostgreSQL (fichiers .sql) et Qdrant (fichiers JSON)
"""

import os
import json
import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any
import hashlib
import numpy as np
from faker import Faker

# Configuration
fake = Faker('fr_FR')
np.random.seed(42)
random.seed(42)
fake.seed_instance(42)

# Constantes
NB_RECORDS = 100
VECTOR_DIMENSION = 384

# Données de référence
CATEGORIES = [
    "Smartphones",
    "Laptops", 
    "Tablettes",
    "Composants PC",
    "Périphériques",
    "Audio",
    "Gaming",
    "Accessoires"
]

PRODUITS_DATA = {
    "Smartphones": [
        ("iPhone 15 Pro", "Smartphone haut de gamme avec puce A17 Pro, écran Super Retina XDR 6.1 pouces, triple caméra 48MP", 1199, {"ecran": "6.1 pouces", "stockage": "128GB", "appareil_photo": "48MP"}),
        ("Samsung Galaxy S24", "Smartphone Android avec écran Dynamic AMOLED 6.2 pouces, processeur Snapdragon 8 Gen 3", 899, {"ecran": "6.2 pouces", "stockage": "256GB", "appareil_photo": "50MP"}),
        ("Google Pixel 8", "Smartphone avec intelligence artificielle avancée, appareil photo exceptionnel", 699, {"ecran": "6.2 pouces", "stockage": "128GB", "appareil_photo": "50MP"}),
        ("OnePlus 12", "Smartphone haute performance avec charge rapide 100W", 799, {"ecran": "6.82 pouces", "stockage": "256GB", "appareil_photo": "50MP"}),
        ("Xiaomi 14", "Smartphone avec caméra Leica, écran LTPO OLED", 649, {"ecran": "6.36 pouces", "stockage": "256GB", "appareil_photo": "50MP"})
    ],
    "Laptops": [
        ("MacBook Pro 14\"", "Ordinateur portable professionnel avec puce M3 Pro, écran Liquid Retina XDR", 2499, {"processeur": "M3 Pro", "ram": "18GB", "stockage": "512GB SSD"}),
        ("Dell XPS 13", "Ultrabook premium avec processeur Intel Core i7, écran InfinityEdge", 1299, {"processeur": "Intel i7", "ram": "16GB", "stockage": "1TB SSD"}),
        ("ThinkPad X1 Carbon", "Laptop professionnel ultra-léger, certifié MIL-STD", 1599, {"processeur": "Intel i7", "ram": "16GB", "stockage": "512GB SSD"}),
        ("ASUS ROG Strix", "Laptop gaming avec RTX 4070, écran 144Hz", 1799, {"processeur": "AMD Ryzen 7", "ram": "32GB", "stockage": "1TB SSD"}),
        ("HP Spectre x360", "Laptop convertible 2-en-1 avec écran tactile OLED", 1399, {"processeur": "Intel i7", "ram": "16GB", "stockage": "512GB SSD"})
    ],
    "Tablettes": [
        ("iPad Pro 12.9\"", "Tablette professionnelle avec puce M2, écran Liquid Retina XDR", 1199, {"ecran": "12.9 pouces", "stockage": "256GB", "connectivite": "Wi-Fi + 5G"}),
        ("Samsung Galaxy Tab S9", "Tablette Android premium avec S Pen inclus", 849, {"ecran": "11 pouces", "stockage": "256GB", "connectivite": "Wi-Fi"}),
        ("Surface Pro 9", "Tablette Windows 2-en-1 avec clavier détachable", 1099, {"ecran": "13 pouces", "stockage": "256GB", "connectivite": "Wi-Fi"})
    ],
    "Composants PC": [
        ("NVIDIA RTX 4080", "Carte graphique haut de gamme pour gaming et création", 1199, {"memoire": "16GB GDDR6X", "architecture": "Ada Lovelace"}),
        ("AMD Ryzen 9 7950X", "Processeur 16 cœurs haute performance", 699, {"coeurs": "16", "frequence": "4.5 GHz"}),
        ("Corsair Vengeance DDR5", "Mémoire RAM haute performance 32GB", 299, {"capacite": "32GB", "frequence": "5600MHz"}),
        ("Samsung 990 PRO", "SSD NVMe ultra-rapide 2TB", 199, {"capacite": "2TB", "interface": "PCIe 4.0"})
    ],
    "Périphériques": [
        ("Logitech MX Master 3S", "Souris ergonomique sans fil pour professionnels", 109, {"connectivite": "Bluetooth + USB", "autonomie": "70 jours"}),
        ("Keychron K8", "Clavier mécanique sans fil compact", 89, {"switches": "Cherry MX", "connectivite": "Bluetooth + USB"}),
        ("Dell UltraSharp U2723QE", "Moniteur 4K 27 pouces pour professionnels", 599, {"resolution": "4K", "taille": "27 pouces"})
    ]
}

STATUTS_COMMANDE = ["en_cours", "expedie", "livre", "annule"]
STATUTS_TICKET = ["ouvert", "en_cours", "resolu", "ferme"]
LABELS_ECO = ["Energy Star", "EPEAT Gold", "EPEAT Silver", "RoHS", "FSC", "TCO Certified"]

class DataGenerator:
    def __init__(self):
        self.categories_map = {}
        self.produits_ids = []
        self.utilisateurs_ids = []
        self.commandes_ids = []
        
    def create_directories(self):
        """Crée les dossiers nécessaires"""
        os.makedirs("data/sql", exist_ok=True)
        os.makedirs("data/json", exist_ok=True)
        
    def generate_hash_password(self, password: str) -> str:
        """Génère un hash fictif pour un mot de passe"""
        return hashlib.sha256(password.encode()).hexdigest()
        
    def generate_vector(self) -> List[float]:
        """Génère un vecteur aléatoire normalisé"""
        vector = np.random.randn(VECTOR_DIMENSION)
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        return vector.tolist()
    
    def generate_categories_sql(self):
        """Génère le fichier SQL pour la table categories"""
        sql_content = """-- Table categories
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL UNIQUE
);

"""
        
        # INSERT statements
        for i, category in enumerate(CATEGORIES, 1):
            self.categories_map[category] = i
            sql_content += f"INSERT INTO categories (id, nom) VALUES ({i}, '{category}');\n"
            
        self.save_sql_file("categories.sql", sql_content)
    
    def generate_produits_sql(self):
        """Génère le fichier SQL pour la table produits"""
        sql_content = """-- Table produits
CREATE TABLE IF NOT EXISTS produits (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(200) NOT NULL,
    prix DECIMAL(10,2) NOT NULL,
    stock INTEGER DEFAULT 0,
    categorie_id INTEGER REFERENCES categories(id),
    description_courte TEXT,
    caracteristiques_structurees JSONB
);

"""
        
        for i in range(1, NB_RECORDS + 1):
            self.produits_ids.append(i)
            
            # Choisir une catégorie aléatoire
            category = random.choice(CATEGORIES)
            categorie_id = self.categories_map[category]
            
            # Générer ou choisir un produit
            if category in PRODUITS_DATA and random.random() < 0.7:
                # Utiliser un produit prédéfini avec variation
                base_produit = random.choice(PRODUITS_DATA[category])
                nom = base_produit[0]
                description = base_produit[1]
                prix_base = base_produit[2]
                caracteristiques = json.dumps(base_produit[3])
                
                # Ajouter de la variation
                prix = prix_base + random.randint(-200, 300)
                if random.random() < 0.3:
                    nom += f" - {fake.color_name()}"
            else:
                # Générer un produit fictif
                nom = f"{fake.company()} {category[:-1]} {fake.random_element(['Pro', 'Max', 'Plus', 'Ultra', 'Elite'])}"
                description = f"{fake.text(max_nb_chars=200)}"
                prix = random.randint(50, 3000)
                caracteristiques = json.dumps({
                    "couleur": fake.color_name(),
                    "poids": f"{random.randint(100, 2000)}g",
                    "garantie": f"{random.randint(1, 3)} ans"
                })
            
            stock = random.randint(0, 500)
            
            # Échapper les apostrophes
            nom_escaped = nom.replace("'", "''")
            description_escaped = description.replace("'", "''")
            caracteristiques_escaped = caracteristiques.replace("'", "''")
            
            sql_content += f"""INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES ({i}, '{nom_escaped}', {prix}, {stock}, {categorie_id}, '{description_escaped}', '{caracteristiques_escaped}');\n"""
        
        self.save_sql_file("produits.sql", sql_content)
    
    def generate_utilisateurs_sql(self):
        """Génère le fichier SQL pour la table utilisateurs"""
        sql_content = """-- Table utilisateurs
CREATE TABLE IF NOT EXISTS utilisateurs (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    consentement_rgpd BOOLEAN DEFAULT FALSE
);

"""
        
        for i in range(1, NB_RECORDS + 1):
            self.utilisateurs_ids.append(i)
            nom = fake.name()
            email = fake.email()
            password = fake.password()
            mot_de_passe_hash = self.generate_hash_password(password)
            consentement_rgpd = random.choice([True, False])
            
            nom_escaped = nom.replace("'", "''")
            
            sql_content += f"""INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES ({i}, '{nom_escaped}', '{email}', '{mot_de_passe_hash}', {consentement_rgpd});\n"""
        
        self.save_sql_file("utilisateurs.sql", sql_content)
    
    def generate_commandes_sql(self):
        """Génère le fichier SQL pour la table commandes"""
        sql_content = """-- Table commandes
CREATE TABLE IF NOT EXISTS commandes (
    id SERIAL PRIMARY KEY,
    utilisateur_id INTEGER REFERENCES utilisateurs(id),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    statut VARCHAR(50) DEFAULT 'en_cours',
    total DECIMAL(10,2) NOT NULL
);

"""
        
        for i in range(1, NB_RECORDS + 1):
            self.commandes_ids.append(i)
            utilisateur_id = random.choice(self.utilisateurs_ids)
            date = fake.date_time_between(start_date='-1y', end_date='now')
            statut = random.choice(STATUTS_COMMANDE)
            total = random.uniform(50, 2000)
            
            sql_content += f"""INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES ({i}, {utilisateur_id}, '{date.isoformat()}', '{statut}', {total:.2f});\n"""
        
        self.save_sql_file("commandes.sql", sql_content)
    
    def generate_commande_produits_sql(self):
        """Génère le fichier SQL pour la table commande_produits"""
        sql_content = """-- Table commande_produits
CREATE TABLE IF NOT EXISTS commande_produits (
    id SERIAL PRIMARY KEY,
    commande_id INTEGER REFERENCES commandes(id),
    produit_id INTEGER REFERENCES produits(id),
    quantite INTEGER DEFAULT 1,
    prix_unitaire DECIMAL(10,2) NOT NULL
);

"""
        
        for i in range(1, NB_RECORDS + 1):
            commande_id = random.choice(self.commandes_ids)
            produit_id = random.choice(self.produits_ids)
            quantite = random.randint(1, 5)
            prix_unitaire = random.uniform(50, 1500)
            
            sql_content += f"""INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES ({i}, {commande_id}, {produit_id}, {quantite}, {prix_unitaire:.2f});\n"""
        
        self.save_sql_file("commande_produits.sql", sql_content)
    
    def generate_paniers_sql(self):
        """Génère le fichier SQL pour la table paniers"""
        sql_content = """-- Table paniers
CREATE TABLE IF NOT EXISTS paniers (
    id SERIAL PRIMARY KEY,
    utilisateur_id INTEGER REFERENCES utilisateurs(id),
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

"""
        
        for i in range(1, NB_RECORDS + 1):
            utilisateur_id = random.choice(self.utilisateurs_ids)
            date_creation = fake.date_time_between(start_date='-30d', end_date='now')
            
            sql_content += f"""INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES ({i}, {utilisateur_id}, '{date_creation.isoformat()}');\n"""
        
        self.save_sql_file("paniers.sql", sql_content)
    
    def generate_panier_produits_sql(self):
        """Génère le fichier SQL pour la table panier_produits"""
        sql_content = """-- Table panier_produits
CREATE TABLE IF NOT EXISTS panier_produits (
    id SERIAL PRIMARY KEY,
    panier_id INTEGER REFERENCES paniers(id),
    produit_id INTEGER REFERENCES produits(id),
    quantite INTEGER DEFAULT 1
);

"""
        
        for i in range(1, NB_RECORDS + 1):
            panier_id = random.randint(1, NB_RECORDS)
            produit_id = random.choice(self.produits_ids)
            quantite = random.randint(1, 3)
            
            sql_content += f"""INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES ({i}, {panier_id}, {produit_id}, {quantite});\n"""
        
        self.save_sql_file("panier_produits.sql", sql_content)
    
    def generate_tickets_service_client_sql(self):
        """Génère le fichier SQL pour la table tickets_service_client"""
        sql_content = """-- Table tickets_service_client
CREATE TABLE IF NOT EXISTS tickets_service_client (
    id SERIAL PRIMARY KEY,
    utilisateur_id INTEGER REFERENCES utilisateurs(id),
    sujet VARCHAR(200) NOT NULL,
    description TEXT,
    statut VARCHAR(50) DEFAULT 'ouvert'
);

"""
        
        sujets_possibles = [
            "Problème de livraison",
            "Produit défectueux",
            "Question sur la garantie",
            "Demande de remboursement",
            "Support technique",
            "Modification de commande",
            "Problème de paiement"
        ]
        
        for i in range(1, NB_RECORDS + 1):
            utilisateur_id = random.choice(self.utilisateurs_ids)
            sujet = random.choice(sujets_possibles)
            description = fake.text(max_nb_chars=300)
            statut = random.choice(STATUTS_TICKET)
            
            description_escaped = description.replace("'", "''")
            
            sql_content += f"""INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES ({i}, {utilisateur_id}, '{sujet}', '{description_escaped}', '{statut}');\n"""
        
        self.save_sql_file("tickets_service_client.sql", sql_content)
    
    def generate_durabilite_sql(self):
        """Génère le fichier SQL pour la table durabilite"""
        sql_content = """-- Table durabilite
CREATE TABLE IF NOT EXISTS durabilite (
    id SERIAL PRIMARY KEY,
    produit_id INTEGER REFERENCES produits(id),
    label_ecologique VARCHAR(100),
    certification VARCHAR(100)
);

"""
        
        for i in range(1, NB_RECORDS + 1):
            produit_id = random.choice(self.produits_ids)
            label_ecologique = random.choice(LABELS_ECO)
            certification = f"Cert-{random.randint(1000, 9999)}"
            
            sql_content += f"""INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES ({i}, {produit_id}, '{label_ecologique}', '{certification}');\n"""
        
        self.save_sql_file("durabilite.sql", sql_content)
    
    def generate_produits_embeddings_json(self):
        """Génère le fichier JSON pour les embeddings de produits"""
        data = []
        
        for i in range(1, NB_RECORDS + 1):
            category = random.choice(CATEGORIES)
            
            if category in PRODUITS_DATA and random.random() < 0.7:
                base_produit = random.choice(PRODUITS_DATA[category])
                nom = base_produit[0]
                description = base_produit[1]
            else:
                nom = f"{fake.company()} {category[:-1]} {fake.random_element(['Pro', 'Max', 'Plus', 'Ultra'])}"
                description = fake.text(max_nb_chars=200)
            
            image_url = f"https://example.com/images/produit_{i}.jpg"
            vector = self.generate_vector()
            
            data.append({
                "id_produit": i,
                "nom": nom,
                "description": description,
                "image_url": image_url,
                "vector": vector
            })
        
        self.save_json_file("produits_embeddings.json", data)
    
    def generate_utilisateurs_embeddings_json(self):
        """Génère le fichier JSON pour les embeddings d'utilisateurs"""
        data = []
        
        preferences_possibles = [
            "Gaming haute performance, RGB, overclocking",
            "Productivité bureautique, silence, efficacité énergétique",
            "Création de contenu, écrans haute résolution, stockage rapide",
            "Mobilité, autonomie, légèreté",
            "Budget serré, rapport qualité-prix",
            "Technologie de pointe, early adopter",
            "Simplicité d'usage, fiabilité"
        ]
        
        for i in range(1, NB_RECORDS + 1):
            preferences = random.choice(preferences_possibles)
            vector = self.generate_vector()
            
            data.append({
                "id_utilisateur": i,
                "preferences": preferences,
                "vector": vector
            })
        
        self.save_json_file("utilisateurs_embeddings.json", data)
    
    def generate_avis_embeddings_json(self):
        """Génère le fichier JSON pour les embeddings d'avis"""
        data = []
        
        avis_positifs = [
            "Excellent produit, très satisfait de mon achat. La qualité est au rendez-vous.",
            "Parfait pour mes besoins, je recommande vivement ce produit.",
            "Livraison rapide, produit conforme à la description. Très bon rapport qualité-prix.",
            "Interface intuitive, performance exceptionnelle. Un must-have !",
            "Design élégant et fonctionnalités avancées. Je suis conquis."
        ]
        
        avis_negatifs = [
            "Produit décevant, ne correspond pas à mes attentes.",
            "Problèmes de compatibilité, assistance client peu réactive.",
            "Qualité de construction discutable pour ce prix.",
            "Installation complexe, documentation insuffisante.",
            "Autonomie décevante, chauffe beaucoup."
        ]
        
        for i in range(1, NB_RECORDS + 1):
            id_produit = random.choice(self.produits_ids)
            
            if random.random() < 0.7:
                texte = random.choice(avis_positifs)
            else:
                texte = random.choice(avis_negatifs)
            
            vector = self.generate_vector()
            
            data.append({
                "id_avis": i,
                "id_produit": id_produit,
                "texte": texte,
                "vector": vector
            })
        
        self.save_json_file("avis_embeddings.json", data)
    
    def save_sql_file(self, filename: str, content: str):
        """Sauvegarde un fichier SQL"""
        filepath = os.path.join("data/sql", filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Fichier généré: {filepath}")
    
    def save_json_file(self, filename: str, data: List[Dict]):
        """Sauvegarde un fichier JSON"""
        filepath = os.path.join("data/json", filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ Fichier généré: {filepath}")
    
    def generate_all(self):
        """Génère tous les fichiers de données"""
        print("🚀 Génération des données de test pour l'électronique...")
        
        self.create_directories()
        
        # Génération des fichiers SQL (base relationnelle)
        print("\n📊 Génération des fichiers SQL...")
        self.generate_categories_sql()
        self.generate_produits_sql()
        self.generate_utilisateurs_sql()
        self.generate_commandes_sql()
        self.generate_commande_produits_sql()
        self.generate_paniers_sql()
        self.generate_panier_produits_sql()
        self.generate_tickets_service_client_sql()
        self.generate_durabilite_sql()
        
        # Génération des fichiers JSON (base vectorielle)
        print("\n🔍 Génération des fichiers JSON avec embeddings...")
        self.generate_produits_embeddings_json()
        self.generate_utilisateurs_embeddings_json()
        self.generate_avis_embeddings_json()
        
        print(f"\n🎉 Génération terminée !")
        print(f"   - {len(os.listdir('data/sql'))} fichiers SQL générés dans data/sql/")
        print(f"   - {len(os.listdir('data/json'))} fichiers JSON générés dans data/json/")
        print(f"   - {NB_RECORDS} enregistrements par table/fichier")


def main():
    """Point d'entrée principal"""
    generator = DataGenerator()
    generator.generate_all()


if __name__ == "__main__":
    main()

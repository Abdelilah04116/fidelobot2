import json
from faker import Faker
import random
import numpy as np
from sentence_transformers import SentenceTransformer

fake = Faker("fr_FR")

# Configuration
NB_AVIS = 40
NB_UTILISATEURS_EMBEDDINGS = 20
NB_PRODUITS_EMBEDDINGS = 50

# Charger le modèle d'embedding
model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_avis_embeddings():
    """Générer des avis avec leurs embeddings pour la collection avis_embeddings"""
    avis = []
    
    # Types d'avis
    types_avis = ["positif", "neutre", "négatif"]
    sentiments = {
        "positif": ["excellent", "super", "génial", "parfait", "recommandé"],
        "neutre": ["correct", "bien", "satisfait", "ok", "acceptable"],
        "négatif": ["décevant", "mauvais", "nul", "éviter", "insatisfait"]
    }
    
    for i in range(NB_AVIS):
        type_avis = random.choice(types_avis)
        sentiment_words = sentiments[type_avis]
        
        # Générer un avis réaliste
        if type_avis == "positif":
            avis_text = f"Produit {sentiment_words[0]} ! {fake.sentence(nb_words=15)}"
        elif type_avis == "neutre":
            avis_text = f"Produit {sentiment_words[0]}. {fake.sentence(nb_words=12)}"
        else:
            avis_text = f"Produit {sentiment_words[0]}. {fake.sentence(nb_words=10)}"
        
        # Générer l'embedding
        embedding = model.encode(avis_text)
        embedding = np.array(embedding, dtype=np.float32)
        
        avis_data = {
            "id": i+1,
            "id_produit": random.randint(1, NB_PRODUITS_EMBEDDINGS),
            "id_utilisateur": random.randint(1, 20),
            "texte": avis_text,
            "type": type_avis,
            "note": random.randint(1, 5) if type_avis != "négatif" else random.randint(1, 3),
            "embedding": embedding.tolist(),
            "date": fake.date_time_between(start_date="-6M", end_date="now").isoformat()
        }
        avis.append(avis_data)
    
    return avis

def generate_utilisateurs_embeddings():
    """Générer des embeddings utilisateurs pour la collection utilisateurs_embeddings"""
    utilisateurs_embeddings = []
    
    for i in range(NB_UTILISATEURS_EMBEDDINGS):
        # Profil utilisateur simulé
        preferences = {
            "categories_preferees": random.sample(["électronique", "mode", "maison", "sport", "livres"], 2),
            "budget_moyen": random.choice(["bas", "moyen", "élevé"]),
            "style_prefere": random.choice(["moderne", "classique", "vintage", "minimaliste"]),
            "frequence_achat": random.choice(["occasionnel", "régulier", "fréquent"])
        }
        
        # Créer un texte descriptif du profil
        profil_text = f"Utilisateur préférant {', '.join(preferences['categories_preferees'])} avec un budget {preferences['budget_moyen']} et un style {preferences['style_prefere']}. Fréquence d'achat: {preferences['frequence_achat']}."
        
        # Générer l'embedding
        embedding = model.encode(profil_text)
        embedding = np.array(embedding, dtype=np.float32)
        
        user_embedding = {
            "id": i+1,
            "profil_text": profil_text,
            "preferences": preferences,
            "embedding": embedding.tolist(),
            "date_creation": fake.date_time_between(start_date="-1y", end_date="now").isoformat()
        }
        utilisateurs_embeddings.append(user_embedding)
    
    return utilisateurs_embeddings

def generate_produits_embeddings():
    """Générer des embeddings produits pour la collection produits_embeddings"""
    produits_embeddings = []
    
    # Catégories de produits
    categories = ["électronique", "mode", "maison", "sport", "livres", "beauté", "jardin", "automobile"]
    
    for i in range(NB_PRODUITS_EMBEDDINGS):
        categorie = random.choice(categories)
        
        # Générer un nom et description de produit
        nom_produit = fake.unique.sentence(nb_words=3)
        description = fake.sentence(nb_words=15)
        
        # Créer un texte combiné pour l'embedding
        produit_text = f"{nom_produit} {description} Catégorie: {categorie}"
        
        # Générer l'embedding
        embedding = model.encode(produit_text)
        embedding = np.array(embedding, dtype=np.float32)
        
        produit_embedding = {
            "id": i+1,
            "nom": nom_produit,
            "description": description,
            "categorie": categorie,
            "prix": round(random.uniform(5, 500), 2),
            "embedding": embedding.tolist(),
            "caracteristiques": {
                "couleur": fake.color_name(),
                "marque": fake.company(),
                "disponibilite": random.choice(["en_stock", "stock_limite", "rupture"])
            }
        }
        produits_embeddings.append(produit_embedding)
    
    return produits_embeddings

def main():
    print("Génération des données pour la BDV (Qdrant)...")
    
    # Générer les embeddings
    avis = generate_avis_embeddings()
    utilisateurs_embeddings = generate_utilisateurs_embeddings()
    produits_embeddings = generate_produits_embeddings()
    
    # Sauvegarder en JSON
    bdv_data = {
        "avis_embeddings": avis,
        "utilisateurs_embeddings": utilisateurs_embeddings,
        "produits_embeddings": produits_embeddings
    }
    
    with open("bdv_data.json", "w", encoding="utf-8") as f:
        json.dump(bdv_data, f, ensure_ascii=False, indent=2)
    
    print("Données BDV générées et sauvegardées dans bdv_data.json")
    print(f"- {len(avis)} avis avec embeddings")
    print(f"- {len(utilisateurs_embeddings)} profils utilisateurs avec embeddings")
    print(f"- {len(produits_embeddings)} produits avec embeddings")
    
    # Afficher un exemple d'embedding
    if avis:
        print(f"\nExemple d'embedding (avis):")
        print(f"Texte: {avis[0]['texte']}")
        print(f"Dimension: {len(avis[0]['embedding'])}")
        print(f"Premiers éléments: {avis[0]['embedding'][:5]}")

if __name__ == "__main__":
    main()

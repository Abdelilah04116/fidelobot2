import json
from faker import Faker
import random
from datetime import datetime, timedelta
import os

fake = Faker("fr_FR")

# Configuration
NB_CATEGORIES = 8
NB_UTILISATEURS = 20
NB_PRODUITS = 50
NB_COMMANDES = 30
NB_PANIERS = 15
NB_TICKETS = 10
NB_DURABILITE = 20

def generate_categories():
    categories = []
    for i in range(NB_CATEGORIES):
        category = {
            "id": i + 1,
            "nom": fake.unique.word().capitalize()
        }
        categories.append(category)
    return categories

def generate_utilisateurs():
    utilisateurs = []
    for i in range(NB_UTILISATEURS):
        user = {
            "id": i + 1,
            "nom": fake.name(),
            "email": fake.unique.email(),
            "mot_de_passe": fake.password(length=12),
            "consentement_rgpd": fake.boolean()
        }
        utilisateurs.append(user)
    return utilisateurs

def generate_produits(categories):
    produits = []
    for i in range(NB_PRODUITS):
        produit = {
            "id": i + 1,
            "nom": fake.unique.sentence(nb_words=3),
            "prix": round(random.uniform(5, 500), 2),
            "stock": random.randint(0, 100),
            "categorie_id": random.choice(categories)["id"],
            "description_courte": fake.sentence(nb_words=10),
            "caracteristiques_structurées": {
                "couleur": fake.color_name(),
                "poids": f"{random.randint(100, 2000)}g",
                "marque": fake.company()
            }
        }
        produits.append(produit)
    return produits

def generate_commandes(utilisateurs, produits):
    commandes = []
    commande_produits = []
    
    for i in range(NB_COMMANDES):
        user = random.choice(utilisateurs)
        date = fake.date_time_between(start_date="-1y", end_date="now")
        statut = random.choice(["en_attente", "expédiée", "livrée", "annulée"])
        
        commande = {
            "id": i + 1,
            "utilisateur_id": user["id"],
            "date": date.isoformat(),
            "statut": statut,
            "total": 0.0
        }
        commandes.append(commande)
        
        # Ajouter des produits à la commande
        nb_items = random.randint(1, 4)
        produits_commande = random.sample(produits, nb_items)
        total = 0.0
        
        for j, produit in enumerate(produits_commande):
            quantite = random.randint(1, 3)
            prix_unitaire = produit["prix"]
            total += prix_unitaire * quantite
            
            cp = {
                "id_commande": commande["id"],
                "id_produit": produit["id"],
                "quantite": quantite,
                "prix_unitaire": prix_unitaire
            }
            commande_produits.append(cp)
        
        commande["total"] = round(total, 2)
    
    return commandes, commande_produits

def generate_paniers(utilisateurs, produits):
    paniers = []
    panier_produits = []
    
    for i in range(NB_PANIERS):
        user = random.choice(utilisateurs)
        date_creation = fake.date_time_between(start_date="-6M", end_date="now")
        
        panier = {
            "id": i + 1,
            "utilisateur_id": user["id"],
            "date_creation": date_creation.isoformat()
        }
        paniers.append(panier)
        
        # Ajouter des produits au panier
        nb_items = random.randint(1, 5)
        produits_panier = random.sample(produits, nb_items)
        
        for produit in produits_panier:
            pp = {
                "id_panier": panier["id"],
                "id_produit": produit["id"],
                "quantite": random.randint(1, 4)
            }
            panier_produits.append(pp)
    
    return paniers, panier_produits

def generate_tickets(utilisateurs):
    sujets = ["Problème de livraison", "Demande de remboursement", "Produit défectueux", 
               "Question sur une commande", "Demande d'information", "Réclamation"]
    
    tickets = []
    for i in range(NB_TICKETS):
        user = random.choice(utilisateurs)
        ticket = {
            "id": i + 1,
            "utilisateur_id": user["id"],
            "sujet": random.choice(sujets),
            "description": fake.paragraph(nb_sentences=3),
            "statut": random.choice(["ouvert", "en_cours", "fermé"])
        }
        tickets.append(ticket)
    
    return tickets

def generate_durabilite(produits):
    labels = ["EcoLabel", "Bio", "Recyclé", "FSC", "GOTS", "Aucun"]
    certifications = ["ISO 14001", "NF Environnement", "EU Ecolabel", "Aucune"]
    
    durabilite = []
    produits_choisis = random.sample(produits, min(NB_DURABILITE, len(produits)))
    
    for produit in produits_choisis:
        dur = {
            "id_produit": produit["id"],
            "label_ecologique": random.choice(labels),
            "certification": random.choice(certifications)
        }
        durabilite.append(dur)
    
    return durabilite

def main():
    print("Génération des données pour la BDR (Postgres)...")
    
    # Générer les données
    categories = generate_categories()
    utilisateurs = generate_utilisateurs()
    produits = generate_produits(categories)
    commandes, commande_produits = generate_commandes(utilisateurs, produits)
    paniers, panier_produits = generate_paniers(utilisateurs, produits)
    tickets = generate_tickets(utilisateurs)
    durabilite = generate_durabilite(produits)
    
    # Sauvegarder en JSON
    data = {
        "categories": categories,
        "utilisateurs": utilisateurs,
        "produits": produits,
        "commandes": commandes,
        "commande_produits": commande_produits,
        "paniers": paniers,
        "panier_produits": panier_produits,
        "tickets_service_client": tickets,
        "durabilite": durabilite
    }
    
    with open("bdr_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("Données BDR générées et sauvegardées dans bdr_data.json")
    print(f"- {len(categories)} catégories")
    print(f"- {len(utilisateurs)} utilisateurs")
    print(f"- {len(produits)} produits")
    print(f"- {len(commandes)} commandes")
    print(f"- {len(paniers)} paniers")
    print(f"- {len(tickets)} tickets")
    print(f"- {len(durabilite)} données de durabilité")

if __name__ == "__main__":
    main()

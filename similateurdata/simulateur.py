import yaml
from faker import Faker
import random
from sqlalchemy.orm import Session
from catalogue.backend.database import SessionLocal
from catalogue.backend.models import Product, Category, Utilisateur, Commande, CommandeProduit, Panier, PanierProduit, TicketServiceClient, Durabilite
from catalogue.backend.qdrant_client import insert_embedding
from sentence_transformers import SentenceTransformer
import numpy as np
from datetime import datetime, timedelta

# Charger la config
with open("similateurdata/config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

NB_PRODUITS = config.get("nb_produits", 50)
NB_CATEGORIES = config.get("nb_categories", 8)
NB_UTILISATEURS = config.get("nb_utilisateurs", 20)
NB_COMMANDES = config.get("nb_commandes", 30)
NB_AVIS = config.get("nb_avis", 40)
NB_PANIERS = config.get("nb_paniers", 15)
NB_TICKETS = config.get("nb_tickets", 10)
NB_DURABILITE = config.get("nb_durabilite", 20)

fake = Faker("fr_FR")
model = SentenceTransformer("all-MiniLM-L6-v2")

# --- Catégories, utilisateurs, produits ---
def create_categories(db: Session):
    categories = []
    for _ in range(NB_CATEGORIES):
        nom = fake.unique.word().capitalize()
        cat = Category(nom=nom)
        db.add(cat)
        categories.append(cat)
    db.commit()
    for cat in categories:
        db.refresh(cat)
    return categories

def create_utilisateurs(db: Session):
    utilisateurs = []
    for _ in range(NB_UTILISATEURS):
        user = Utilisateur(
            nom=fake.name(),
            email=fake.unique.email(),
            mot_de_passe=fake.password(length=12),
            consentement_rgpd=fake.boolean()
        )
        db.add(user)
        utilisateurs.append(user)
    db.commit()
    for user in utilisateurs:
        db.refresh(user)
    return utilisateurs

def create_produits(db: Session, categories):
    produits = []
    for _ in range(NB_PRODUITS):
        nom = fake.unique.sentence(nb_words=3)
        prix = round(random.uniform(5, 500), 2)
        stock = random.randint(0, 100)
        categorie = random.choice(categories)
        description_courte = fake.sentence(nb_words=10)
        caracteristiques = {"couleur": fake.color_name(), "poids": f"{random.randint(100, 2000)}g"}
        produit = Product(
            nom=nom,
            prix=prix,
            stock=stock,
            categorie_id=categorie.id,
            description_courte=description_courte,
            caracteristiques_structurées=caracteristiques
        )
        db.add(produit)
        produits.append(produit)
    db.commit()
    for produit in produits:
        db.refresh(produit)
    return produits

def index_produits_qdrant(produits):
    for produit in produits:
        text = f"{produit.nom} {produit.description_courte}"
        embedding = model.encode(text)
        embedding = np.array(embedding, dtype=np.float32)
        insert_embedding(
            collection="produits_embeddings",
            id=produit.id,
            embedding=embedding.tolist(),
            payload={"nom": produit.nom, "categorie_id": produit.categorie_id}
        )

# --- Commandes et commande_produits ---
def create_commandes(db: Session, utilisateurs, produits):
    commandes = []
    for _ in range(NB_COMMANDES):
        user = random.choice(utilisateurs)
        date = fake.date_time_between(start_date="-1y", end_date="now")
        statut = random.choice(["en_attente", "expédiée", "livrée", "annulée"])
        commande = Commande(
            utilisateur_id=user.id,
            date=date,
            statut=statut,
            total=0.0
        )
        db.add(commande)
        commandes.append(commande)
    db.commit()
    for commande in commandes:
        db.refresh(commande)
    # Ajouter les produits à chaque commande
    for commande in commandes:
        nb_items = random.randint(1, 4)
        produits_commande = random.sample(produits, nb_items)
        total = 0.0
        for produit in produits_commande:
            quantite = random.randint(1, 3)
            prix_unitaire = float(produit.prix)
            total += prix_unitaire * quantite
            cp = CommandeProduit(
                id_commande=commande.id,
                id_produit=produit.id,
                quantite=quantite,
                prix_unitaire=prix_unitaire
            )
            db.add(cp)
        commande.total = total
    db.commit()
    return commandes

# --- Paniers et panier_produits ---
def create_paniers(db: Session, utilisateurs, produits):
    paniers = []
    for _ in range(NB_PANIERS):
        user = random.choice(utilisateurs)
        date_creation = fake.date_time_between(start_date="-6M", end_date="now")
        panier = Panier(
            utilisateur_id=user.id,
            date_creation=date_creation
        )
        db.add(panier)
        paniers.append(panier)
    db.commit()
    for panier in paniers:
        db.refresh(panier)
    # Ajouter les produits à chaque panier
    for panier in paniers:
        nb_items = random.randint(1, 5)
        produits_panier = random.sample(produits, nb_items)
        for produit in produits_panier:
            quantite = random.randint(1, 4)
            pp = PanierProduit(
                id_panier=panier.id,
                id_produit=produit.id,
                quantite=quantite
            )
            db.add(pp)
    db.commit()
    return paniers

# --- Avis (embeddings) ---
def create_avis_qdrant(utilisateurs, produits):
    for _ in range(NB_AVIS):
        user = random.choice(utilisateurs)
        produit = random.choice(produits)
        texte = fake.sentence(nb_words=20)
        embedding = model.encode(texte)
        embedding = np.array(embedding, dtype=np.float32)
        insert_embedding(
            collection="avis_embeddings",
            id=f"{produit.id}_{user.id}_{random.randint(1,99999)}",
            embedding=embedding.tolist(),
            payload={"id_produit": produit.id, "id_utilisateur": user.id, "texte": texte}
        )

# --- Tickets de service client ---
def create_tickets(db: Session, utilisateurs):
    sujets = ["Problème de livraison", "Demande de remboursement", "Produit défectueux", "Question sur une commande", "Demande d'information"]
    tickets = []
    for _ in range(NB_TICKETS):
        user = random.choice(utilisateurs)
        sujet = random.choice(sujets)
        description = fake.paragraph(nb_sentences=3)
        statut = random.choice(["ouvert", "en_cours", "fermé"])
        ticket = TicketServiceClient(
            utilisateur_id=user.id,
            sujet=sujet,
            description=description,
            statut=statut
        )
        db.add(ticket)
        tickets.append(ticket)
    db.commit()
    return tickets

# --- Données de durabilité ---
def create_durabilite(db: Session, produits):
    labels = ["EcoLabel", "Bio", "Recyclé", "FSC", "GOTS", "Aucun"]
    certifications = ["ISO 14001", "NF Environnement", "EU Ecolabel", "Aucune"]
    produits_choisis = random.sample(produits, min(NB_DURABILITE, len(produits)))
    for produit in produits_choisis:
        dur = Durabilite(
            id_produit=produit.id,
            label_ecologique=random.choice(labels),
            certification=random.choice(certifications)
        )
        db.add(dur)
    db.commit()

# --- MAIN ---
def main():
    db = SessionLocal()
    print("Création des catégories...")
    categories = create_categories(db)
    print("Création des utilisateurs...")
    utilisateurs = create_utilisateurs(db)
    print("Création des produits...")
    produits = create_produits(db, categories)
    print("Indexation des produits dans Qdrant...")
    index_produits_qdrant(produits)
    print("Création des commandes...")
    create_commandes(db, utilisateurs, produits)
    print("Création des paniers...")
    create_paniers(db, utilisateurs, produits)
    print("Indexation des avis dans Qdrant...")
    create_avis_qdrant(utilisateurs, produits)
    print("Création des tickets de service client...")
    create_tickets(db, utilisateurs)
    print("Création des données de durabilité...")
    create_durabilite(db, produits)
    print("Simulation terminée !")
    db.close()

if __name__ == "__main__":
    main()

import json
import sys
import os

# Ajouter le dossier parent au PYTHONPATH pour importer catalogue
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from catalogue.backend.database import SessionLocal
from catalogue.backend.models import Category, Product, Utilisateur, Commande, CommandeProduit, Panier, PanierProduit, TicketServiceClient, Durabilite
from catalogue.backend.qdrant_client import insert_embedding, create_collections
from sqlalchemy.orm import Session

def insert_categories(db: Session, categories_data):
    """Insérer les catégories dans Postgres"""
    print("Insertion des catégories...")
    for cat_data in categories_data:
        category = Category(
            id=cat_data["id"],
            nom=cat_data["nom"]
        )
        db.add(category)
        db.commit()
    print(f"[OK] {len(categories_data)} catégories insérées")

def insert_utilisateurs(db: Session, utilisateurs_data):
    """Insérer les utilisateurs dans Postgres"""
    print("Insertion des utilisateurs...")
    for user_data in utilisateurs_data:
        user = Utilisateur(
            id=user_data["id"],
            nom=user_data["nom"],
            email=user_data["email"],
            mot_de_passe=user_data["mot_de_passe"],
            consentement_rgpd=user_data["consentement_rgpd"]
        )
        db.add(user)
        db.commit()
    print(f"[OK] {len(utilisateurs_data)} utilisateurs insérés")

def insert_produits(db: Session, produits_data):
    """Insérer les produits dans Postgres"""
    print("Insertion des produits...")
    for prod_data in produits_data:
        produit = Product(
            id=prod_data["id"],
            nom=prod_data["nom"],
            prix=prod_data["prix"],
            stock=prod_data["stock"],
            categorie_id=prod_data["categorie_id"],
            description_courte=prod_data["description_courte"],
            caracteristiques_structurées=prod_data["caracteristiques_structurées"]
        )
        db.add(produit)
        db.commit()
    print(f"[OK] {len(produits_data)} produits insérés")

def insert_commandes(db: Session, commandes_data, commande_produits_data):
    """Insérer les commandes et leurs produits dans Postgres"""
    print("Insertion des commandes...")
    for cmd_data in commandes_data:
        commande = Commande(
            id=cmd_data["id"],
            utilisateur_id=cmd_data["utilisateur_id"],
            date=cmd_data["date"],
            statut=cmd_data["statut"],
            total=cmd_data["total"]
        )
        db.add(commande)
    db.commit()
    
    print("Insertion des produits de commande...")
    for cp_data in commande_produits_data:
        cp = CommandeProduit(
            id_commande=cp_data["id_commande"],
            id_produit=cp_data["id_produit"],
            quantite=cp_data["quantite"],
            prix_unitaire=cp_data["prix_unitaire"]
        )
        db.add(cp)
        db.commit()
    print(f"[OK] {len(commandes_data)} commandes et {len(commande_produits_data)} produits de commande insérés")

def insert_paniers(db: Session, paniers_data, panier_produits_data):
    """Insérer les paniers et leurs produits dans Postgres"""
    print("Insertion des paniers...")
    for panier_data in paniers_data:
        panier = Panier(
            id=panier_data["id"],
            utilisateur_id=panier_data["utilisateur_id"],
            date_creation=panier_data["date_creation"]
        )
        db.add(panier)
    db.commit()
    
    print("Insertion des produits de panier...")
    for pp_data in panier_produits_data:
        pp = PanierProduit(
            id_panier=pp_data["id_panier"],
            id_produit=pp_data["id_produit"],
            quantite=pp_data["quantite"]
        )
        db.add(pp)
        db.commit()
    print(f"[OK] {len(paniers_data)} paniers et {len(panier_produits_data)} produits de panier insérés")

def insert_tickets(db: Session, tickets_data):
    """Insérer les tickets de service client dans Postgres"""
    print("Insertion des tickets...")
    for ticket_data in tickets_data:
        ticket = TicketServiceClient(
            id=ticket_data["id"],
            utilisateur_id=ticket_data["utilisateur_id"],
            sujet=ticket_data["sujet"],
            description=ticket_data["description"],
            statut=ticket_data["statut"]
        )
        db.add(ticket)
        db.commit()
    print(f"[OK] {len(tickets_data)} tickets insérés")

def insert_durabilite(db: Session, durabilite_data):
    """Insérer les données de durabilité dans Postgres"""
    print("Insertion des données de durabilité...")
    for dur_data in durabilite_data:
        dur = Durabilite(
            id_produit=dur_data["id_produit"],
            label_ecologique=dur_data["label_ecologique"],
            certification=dur_data["certification"]
        )
        db.add(dur)
        db.commit()
    print(f"[OK] {len(durabilite_data)} données de durabilité insérées")

def insert_qdrant_data(bdv_data):
    """Insérer les données vectorielles dans Qdrant"""
    print("Création des collections Qdrant...")
    create_collections()
    
    print("Insertion des embeddings produits...")
    for prod in bdv_data["produits_embeddings"]:
        insert_embedding(
            collection="produits_embeddings",
            id=prod["id"],
            embedding=prod["embedding"],
            payload={
                "nom": prod["nom"],
                "categorie": prod["categorie"],
                "prix": prod["prix"]
            }
        )
    
    print("Insertion des embeddings utilisateurs...")
    for user in bdv_data["utilisateurs_embeddings"]:
        insert_embedding(
            collection="utilisateurs_embeddings",
            id=user["id"],
            embedding=user["embedding"],
            payload=user["preferences"]
        )
    
    print("Insertion des embeddings avis...")
    for avis in bdv_data["avis_embeddings"]:
        insert_embedding(
            collection="avis_embeddings",
            id=avis["id"],
            embedding=avis["embedding"],
            payload={
                "id_produit": avis["id_produit"],
                "id_utilisateur": avis["id_utilisateur"],
                "texte": avis["texte"],
                "type": avis["type"],
                "note": avis["note"]
            }
        )
    
    print("[OK] Toutes les données vectorielles insérées dans Qdrant")

def main():
    print("=== INSERTION DES DONNÉES SIMULÉES ===")
    
    # Charger les données BDR
    try:
        with open("bdr_data.json", "r", encoding="utf-8") as f:
            bdr_data = json.load(f)
        print("[OK] Données BDR chargées")
    except FileNotFoundError:
        print("[ERREUR] Fichier bdr_data.json non trouvé. Exécutez d'abord generate_bdr_data.py")
        return
    
    # Charger les données BDV
    try:
        with open("bdv_data.json", "r", encoding="utf-8") as f:
            bdv_data = json.load(f)
        print("[OK] Données BDV chargées")
    except FileNotFoundError:
        print("[ERREUR] Fichier bdv_data.json non trouvé. Exécutez d'abord generate_bdv_data.py")
        return
    
    # Insertion dans Postgres (BDR)
    db = SessionLocal()
    try:
        print("\n--- INSERTION BDR (Postgres) ---")
        insert_categories(db, bdr_data["categories"])
        insert_utilisateurs(db, bdr_data["utilisateurs"])
        insert_produits(db, bdr_data["produits"])
        insert_commandes(db, bdr_data["commandes"], bdr_data["commande_produits"])
        insert_paniers(db, bdr_data["paniers"], bdr_data["panier_produits"])
        insert_tickets(db, bdr_data["tickets_service_client"])
        insert_durabilite(db, bdr_data["durabilite"])
        print("[OK] Toutes les données BDR insérées avec succès")
    except Exception as e:
        print(f"[ERREUR] Erreur lors de l'insertion BDR: {e}")
        db.rollback()
    finally:
        db.close()
    
    # Insertion dans Qdrant (BDV)
    try:
        print("\n--- INSERTION BDV (Qdrant) ---")
        insert_qdrant_data(bdv_data)
        print("[OK] Toutes les données BDV insérées avec succès")
    except Exception as e:
        print(f"[ERREUR] Erreur lors de l'insertion BDV: {e}")
    
    print("\n=== INSERTION TERMINÉE ===")

if __name__ == "__main__":
    main()

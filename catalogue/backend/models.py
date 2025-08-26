from sqlalchemy import Column, Integer, String, Numeric, Boolean, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), nullable=False)
    produits = relationship("Product", back_populates="categorie")

class Product(Base):
    __tablename__ = "produits"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), nullable=False)
    prix = Column(Numeric(10,2), nullable=False)
    stock = Column(Integer, nullable=False)
    categorie_id = Column(Integer, ForeignKey("categories.id"))
    description_courte = Column(Text)
    caracteristiques_structurées = Column(JSON)
    categorie = relationship("Category", back_populates="produits")
    durabilite = relationship("Durabilite", uselist=False, back_populates="produit")

class Utilisateur(Base):
    __tablename__ = "utilisateurs"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    mot_de_passe = Column(String(255), nullable=False)
    consentement_rgpd = Column(Boolean, default=False)
    
    # Alias pour compatibilité avec les agents existants
    username = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_vip = Column(Boolean, default=False)
    preferences = Column(JSON, default={})
    first_name = Column(String(255))
    last_name = Column(String(255))
    
    paniers = relationship("Panier", back_populates="utilisateur")
    commandes = relationship("Commande", back_populates="utilisateur")
    tickets = relationship("TicketServiceClient", back_populates="utilisateur")

class Commande(Base):
    __tablename__ = "commandes"
    id = Column(Integer, primary_key=True, index=True)
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id"))
    date = Column(DateTime, default=datetime.utcnow)
    statut = Column(String(50))
    total = Column(Numeric(10,2))
    utilisateur = relationship("Utilisateur", back_populates="commandes")
    produits = relationship("CommandeProduit", back_populates="commande")

class CommandeProduit(Base):
    __tablename__ = "commande_produits"
    id_commande = Column(Integer, ForeignKey("commandes.id"), primary_key=True)
    id_produit = Column(Integer, ForeignKey("produits.id"), primary_key=True)
    quantite = Column(Integer, nullable=False)
    prix_unitaire = Column(Numeric(10,2), nullable=False)
    commande = relationship("Commande", back_populates="produits")
    produit = relationship("Product")

class Panier(Base):
    __tablename__ = "paniers"
    id = Column(Integer, primary_key=True, index=True)
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id"))
    date_creation = Column(DateTime, default=datetime.utcnow)
    utilisateur = relationship("Utilisateur", back_populates="paniers")
    produits = relationship("PanierProduit", back_populates="panier")

class PanierProduit(Base):
    __tablename__ = "panier_produits"
    id_panier = Column(Integer, ForeignKey("paniers.id"), primary_key=True)
    id_produit = Column(Integer, ForeignKey("produits.id"), primary_key=True)
    quantite = Column(Integer, nullable=False)
    panier = relationship("Panier", back_populates="produits")
    produit = relationship("Product")

class TicketServiceClient(Base):
    __tablename__ = "tickets_service_client"
    id = Column(Integer, primary_key=True, index=True)
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id"))
    sujet = Column(String(255))
    description = Column(Text)
    statut = Column(String(50))
    utilisateur = relationship("Utilisateur", back_populates="tickets")

class Durabilite(Base):
    __tablename__ = "durabilite"
    id_produit = Column(Integer, ForeignKey("produits.id"), primary_key=True)
    label_ecologique = Column(String(255))
    certification = Column(String(255))
    produit = relationship("Product", back_populates="durabilite")

# Alias pour compatibilité avec les agents existants
User = Utilisateur
Order = Commande
OrderItem = CommandeProduit

-- Table des catégories
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL
);

-- Table des produits
CREATE TABLE produits (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    prix NUMERIC(10,2) NOT NULL CHECK (prix > 0),
    stock INTEGER NOT NULL CHECK (stock >= 0),
    categorie_id INTEGER REFERENCES categories(id),
    description_courte TEXT,
    caracteristiques_structurées JSONB
);

-- Table des utilisateurs
CREATE TABLE utilisateurs (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    consentement_rgpd BOOLEAN DEFAULT FALSE
);

-- Table des commandes
CREATE TABLE commandes (
    id SERIAL PRIMARY KEY,
    utilisateur_id INTEGER REFERENCES utilisateurs(id),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    statut VARCHAR(50),
    total NUMERIC(10,2)
);

-- Table de liaison commande/produits
CREATE TABLE commande_produits (
    id_commande INTEGER REFERENCES commandes(id),
    id_produit INTEGER REFERENCES produits(id),
    quantite INTEGER NOT NULL CHECK (quantite > 0),
    prix_unitaire NUMERIC(10,2) NOT NULL,
    PRIMARY KEY (id_commande, id_produit)
);

-- Table des paniers
CREATE TABLE paniers (
    id SERIAL PRIMARY KEY,
    utilisateur_id INTEGER REFERENCES utilisateurs(id),
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table de liaison panier/produits
CREATE TABLE panier_produits (
    id_panier INTEGER REFERENCES paniers(id),
    id_produit INTEGER REFERENCES produits(id),
    quantite INTEGER NOT NULL CHECK (quantite > 0),
    PRIMARY KEY (id_panier, id_produit)
);

-- Table des tickets de service client
CREATE TABLE tickets_service_client (
    id SERIAL PRIMARY KEY,
    utilisateur_id INTEGER REFERENCES utilisateurs(id),
    sujet VARCHAR(255),
    description TEXT,
    statut VARCHAR(50)
);

-- Table durabilité
CREATE TABLE durabilite (
    id_produit INTEGER REFERENCES produits(id) PRIMARY KEY,
    label_ecologique VARCHAR(255),
    certification VARCHAR(255)
);

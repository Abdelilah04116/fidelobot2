# Simulateur de données

Ce dossier contient des scripts pour générer et indexer des données simulées dans la base relationnelle (Postgres) et la base vectorielle (Qdrant).

## Scripts disponibles

### 1. **generate_bdr_data.py** - Génération des données BDR
Génère des données JSON pour Postgres (tables relationnelles) :
- Catégories, utilisateurs, produits
- Commandes et leurs produits
- Paniers et leurs produits  
- Tickets de service client
- Données de durabilité

**Exécution :**
```bash
python similateurdata/generate_bdr_data.py
```
**Résultat :** `bdr_data.json`

### 2. **generate_bdv_data.py** - Génération des données BDV
Génère des données JSON avec embeddings pour Qdrant (collections vectorielles) :
- Embeddings des produits
- Embeddings des profils utilisateurs
- Embeddings des avis

**Exécution :**
```bash
python similateurdata/generate_bdv_data.py
```
**Résultat :** `bdv_data.json`

### 3. **insert_data.py** - Insertion dans les bases
Charge les fichiers JSON et insère les données dans Postgres et Qdrant.

**Exécution :**
```bash
python similateurdata/insert_data.py
```

## Workflow complet

1. **Générer les données :**
   ```bash
   python similateurdata/generate_bdr_data.py
   python similateurdata/generate_bdv_data.py
   ```

2. **Insérer dans les bases :**
   ```bash
   python similateurdata/insert_data.py
   ```

## Dépendances
- faker
- sqlalchemy
- qdrant-client
- sentence-transformers
- pyyaml

Installez-les avec :
```bash
pip install faker sqlalchemy qdrant-client sentence-transformers pyyaml
```

## Configuration
Modifiez les paramètres dans `config.yaml` pour ajuster le volume de données générées.

## Structure des données

### BDR (Postgres)
- **categories** : id, nom
- **utilisateurs** : id, nom, email, mot_de_passe, consentement_rgpd
- **produits** : id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurées
- **commandes** : id, utilisateur_id, date, statut, total
- **commande_produits** : id_commande, id_produit, quantite, prix_unitaire
- **paniers** : id, utilisateur_id, date_creation
- **panier_produits** : id_panier, id_produit, quantite
- **tickets_service_client** : id, utilisateur_id, sujet, description, statut
- **durabilite** : id_produit, label_ecologique, certification

### BDV (Qdrant)
- **produits_embeddings** : embeddings des noms + descriptions
- **utilisateurs_embeddings** : embeddings des profils et préférences
- **avis_embeddings** : embeddings des textes d'avis

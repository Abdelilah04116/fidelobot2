# Guide de Test de l'Agent Multimodal

## 🎯 Objectif
Tester que l'agent multimodal fonctionne correctement pour analyser des images de produits et rechercher des alternatives dans la base de données.

## 📋 Prérequis
1. **Base de données** : PostgreSQL et Qdrant doivent être démarrés
2. **Dépendances** : Les packages Python requis doivent être installés
3. **Serveur backend** : Le serveur FastAPI doit être en cours d'exécution

## 🚀 Étapes de Test

### 1. Démarrer les Services

```bash
# Démarrer PostgreSQL et Qdrant (si pas déjà fait)
docker-compose up -d

# Démarrer le serveur backend
uvicorn catalogue.backend.main:app --reload

# Dans un autre terminal, démarrer l'interface frontend
cd interface/E-Commerce-Store-main/E-Commerce-Store-main
npm run dev
```

### 2. Test Basique de l'Agent

```bash
# Exécuter le script de test simple
python test_multimodal_simple.py
```

Ce script va :
- ✅ Vérifier que l'agent multimodal peut être importé
- ✅ Tester l'initialisation de l'agent
- ✅ Vérifier l'intégration avec l'orchestrateur
- ✅ Simuler un upload d'image

### 3. Test via l'Interface Web

1. **Ouvrir l'interface** : http://localhost:5173/
2. **Cliquer sur l'icône de chat** (bouton flottant en bas à droite)
3. **Envoyer une image** :
   - Cliquer sur l'icône d'attachement (📎)
   - Sélectionner une image de produit (téléphone, ordinateur, etc.)
   - Ajouter un message comme "Est-ce que vous avez ce produit en stock?"
   - Envoyer le message

### 4. Test via API Directe

```bash
# Test avec curl (remplacer IMAGE_BASE64 par une vraie image encodée)
curl -X POST "http://localhost:8000/api/chat/message" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Voici une image de téléphone",
    "session_id": "test-123",
    "user_id": 1,
    "audio_data": "IMAGE_BASE64_HERE",
    "audio_format": "png"
  }'
```

## 🔍 Ce que l'Agent Multimodal Fait

### 1. **Analyse d'Image**
- Décodage de l'image base64
- Extraction des caractéristiques visuelles
- Génération d'embeddings vectoriels
- Analyse du contenu (couleurs, objets détectés)

### 2. **Recherche de Produits**
- Recherche par similarité d'image dans Qdrant
- Recherche textuelle basée sur la description générée
- Recherche hybride combinant image + texte
- Filtrage par disponibilité et prix

### 3. **Réponse Structurée**
```json
{
  "detected_product": {
    "name": "iPhone 14",
    "confidence": 0.85,
    "features": ["smartphone", "apple", "black"]
  },
  "best_match": {
    "id": 123,
    "name": "iPhone 14 128GB Noir",
    "price": 899.99,
    "stock": 5,
    "image_url": "https://..."
  },
  "alternatives_ranked": [
    {
      "id": 124,
      "name": "iPhone 14 256GB Noir",
      "price": 999.99,
      "similarity": 0.92
    }
  ]
}
```

## 🧪 Tests Spécifiques

### Test 1 : Image de Téléphone
- **Image** : Photo d'un iPhone
- **Attendu** : Détection "smartphone", recherche d'iPhones dans la base
- **Vérification** : Produits trouvés avec similarité > 0.7

### Test 2 : Image d'Ordinateur
- **Image** : Photo d'un laptop
- **Attendu** : Détection "ordinateur portable", recherche de laptops
- **Vérification** : Produits trouvés dans la catégorie "électronique"

### Test 3 : Image Non-Product
- **Image** : Photo d'un chat ou paysage
- **Attendu** : Message d'erreur ou demande de clarification
- **Vérification** : Réponse appropriée indiquant qu'aucun produit n'est détecté

## 🐛 Dépannage

### Erreur : "ModuleNotFoundError"
```bash
# Installer les dépendances manquantes
pip install -r SMA/requirements_multimodal.txt
```

### Erreur : "Connection refused"
```bash
# Vérifier que PostgreSQL et Qdrant sont démarrés
docker-compose ps
```

### Erreur : "Invalid end tag" (Vue.js)
```bash
# Le fichier AssistantIA.vue a été corrigé
# Redémarrer le serveur de développement
npm run dev
```

### Erreur : "Node is a dead-end"
```bash
# L'orchestrateur a été corrigé
# Redémarrer le serveur backend
uvicorn catalogue.backend.main:app --reload
```

## 📊 Métriques de Performance

### Temps de Réponse
- **Analyse d'image** : < 2 secondes
- **Recherche vectorielle** : < 1 seconde
- **Réponse complète** : < 5 secondes

### Précision
- **Détection de produits** : > 80%
- **Similarité d'image** : > 70% pour les vrais positifs
- **Faux positifs** : < 10%

## 🎯 Résultats Attendus

### ✅ Succès
- L'agent détecte correctement le type de produit
- Des alternatives pertinentes sont proposées
- Les images des produits sont incluses dans la réponse
- La réponse est structurée et lisible

### ❌ Échec
- Aucun produit trouvé pour des images claires
- Réponses non pertinentes
- Erreurs de traitement d'image
- Timeout ou crash du système

## 🔄 Améliorations Futures

1. **Support de plus de formats d'image** (WebP, AVIF)
2. **Reconnaissance de marques** plus précise
3. **Détection de caractéristiques** (couleur, taille, modèle)
4. **Cache des embeddings** pour améliorer les performances
5. **Interface d'upload d'image** plus intuitive

## 📞 Support

Si vous rencontrez des problèmes :
1. Vérifiez les logs du serveur backend
2. Consultez la console du navigateur
3. Testez avec le script `test_multimodal_simple.py`
4. Vérifiez que toutes les dépendances sont installées

# Agent Multimodal - SMA E-commerce

## Vue d'ensemble

L'agent multimodal est un composant spécialisé du système multi-agents (SMA) qui traite les images de produits et recherche des correspondances dans le catalogue e-commerce.

## Fonctionnalités

### 🖼️ Traitement d'images
- **Analyse visuelle** : Extraction des caractéristiques visuelles (couleurs, luminosité, taille)
- **OCR intégré** : Détection et extraction de texte dans les images
- **Embeddings vectoriels** : Génération de représentations numériques des images
- **Préprocessing intelligent** : Redimensionnement et optimisation des images

### 🔍 Recherche de produits
- **Recherche par similarité d'image** : Utilisation de Qdrant pour la recherche vectorielle
- **Recherche hybride** : Combinaison image + texte pour de meilleurs résultats
- **Alternatives intelligentes** : Suggestion de produits similaires
- **Scoring de confiance** : Évaluation de la qualité des correspondances

### 📊 Sortie structurée
```json
{
  "detected_product": {...},
  "best_match": {...},
  "alternatives_ranked": [...],
  "confidence": 0.95,
  "search_query": "description extraite de l'image",
  "image_analysis": {...}
}
```

## Architecture

### Composants principaux

1. **`MultimodalAgent`** : Agent principal orchestrant le traitement
2. **`ImageProcessingTools`** : Outils d'analyse et de traitement d'images
3. **`VectorSearchTools`** : Outils de recherche vectorielle et hybride

### Flux de traitement

```
Image Upload → Analyse visuelle → Extraction embedding → Recherche vectorielle → Résultats structurés
     ↓              ↓                    ↓                    ↓                    ↓
  Décodage    Caractéristiques    Représentation    Qdrant + API    JSON + UI
```

## Installation

### Dépendances système

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-fra
sudo apt-get install libopencv-dev python3-opencv
```

#### Windows
1. Télécharger Tesseract depuis [UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
2. Installer OpenCV via pip ou conda

#### macOS
```bash
brew install tesseract tesseract-lang
brew install opencv
```

### Dépendances Python

```bash
pip install -r SMA/requirements_multimodal.txt
```

## Utilisation

### Intégration dans le SMA

L'agent multimodal est automatiquement intégré dans l'orchestrateur et peut être invoqué via :

```python
from SMA.agents.multimodal_agent import MultimodalAgent

agent = MultimodalAgent()
result = await agent.execute(state)
```

### Utilisation directe

```python
from SMA.tools.image_tools import ImageProcessingTools
from SMA.tools.vector_search import VectorSearchTools

# Traitement d'image
image_tools = ImageProcessingTools()
analysis = image_tools.analyze_image_content(image)
embedding = image_tools.extract_image_embedding(image)

# Recherche vectorielle
vector_tools = VectorSearchTools()
results = await vector_tools.hybrid_search(embedding, "description")
```

### Test de l'agent

```bash
python test_multimodal_agent.py
```

## Configuration

### Variables d'environnement

```bash
# Qdrant
QDRANT_HOST=localhost
QDRANT_PORT=6333

# API Backend
BACKEND_API_URL=http://localhost:8000

# Modèles
SENTENCE_TRANSFORMERS_MODEL=clip-ViT-B-32
```

### Paramètres de recherche

```python
# Poids de la recherche hybride
image_weight = 0.7    # Poids pour la similarité d'image
text_weight = 0.3     # Poids pour la similarité textuelle

# Seuils de confiance
image_threshold = 0.7  # Seuil minimal pour les résultats d'image
text_threshold = 0.6   # Seuil minimal pour les résultats textuels
```

## Exemples d'utilisation

### 1. Recherche par image de produit

```python
# L'utilisateur envoie une image
image_data = base64.b64encode(image_bytes).decode()

# Traitement via l'agent
state = {
    "audio_data": image_data,  # Réutilise le champ audio_data
    "audio_format": "png",
    "user_message": "Trouvez ce produit"
}

result = await multimodal_agent.execute(state)
```

### 2. Analyse d'image personnalisée

```python
from PIL import Image

# Charger une image
image = Image.open("product.jpg")

# Analyser le contenu
tools = ImageProcessingTools()
analysis = tools.analyze_image_content(image)
description = tools.generate_image_description(analysis)

print(f"Description: {description}")
```

### 3. Recherche vectorielle avancée

```python
# Recherche hybride
results = await vector_tools.hybrid_search(
    image_embedding=embedding,
    text_query="clavier mécanique RGB",
    image_weight=0.8,
    text_weight=0.2,
    limit=20
)

# Filtrer par score
high_confidence = [r for r in results if r["combined_score"] > 0.8]
```

## Performance et optimisation

### Optimisations recommandées

1. **Cache des embeddings** : Stocker les embeddings calculés
2. **Batch processing** : Traiter plusieurs images simultanément
3. **Modèles légers** : Utiliser des modèles optimisés pour la production
4. **Indexation Qdrant** : Optimiser les collections vectorielles

### Métriques de performance

- **Temps de traitement** : < 2 secondes par image
- **Précision de recherche** : > 85% de correspondances correctes
- **Utilisation mémoire** : < 2GB pour 1000 images
- **Latence API** : < 500ms pour la recherche

## Dépannage

### Problèmes courants

#### Erreur Tesseract
```
pytesseract.pytesseract.TesseractNotFoundError
```
**Solution** : Vérifier l'installation de Tesseract et le PATH

#### Erreur OpenCV
```
ImportError: No module named 'cv2'
```
**Solution** : Installer opencv-python

#### Erreur Qdrant
```
Connection refused to Qdrant
```
**Solution** : Vérifier que Qdrant est démarré sur localhost:6333

#### Erreur modèle SentenceTransformers
```
OSError: Model not found
```
**Solution** : Le modèle sera téléchargé automatiquement au premier usage

### Logs et débogage

```python
import logging

# Activer les logs détaillés
logging.basicConfig(level=logging.DEBUG)

# Logs spécifiques à l'agent
logger = logging.getLogger("multimodal_agent")
logger.setLevel(logging.DEBUG)
```

## Développement

### Ajout de nouvelles fonctionnalités

1. **Nouveaux outils** : Créer dans `SMA/tools/`
2. **Nouveaux agents** : Hériter de `BaseAgent`
3. **Tests** : Ajouter dans `test_multimodal_agent.py`

### Structure des tests

```python
async def test_new_feature():
    """Test de la nouvelle fonctionnalité"""
    # Arrange
    # Act
    # Assert
```

## Support et contribution

### Documentation
- [SentenceTransformers](https://www.sbert.net/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [OpenCV Python](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)

### Issues et bugs
Créer une issue sur le repository principal avec le label `multimodal`

### Pull requests
1. Fork le repository
2. Créer une branche feature
3. Ajouter les tests
4. Soumettre la PR

---

**Note** : L'agent multimodal est en développement actif. Les API peuvent changer entre les versions.

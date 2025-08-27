# 🎤 Système de Traitement Vocal Fidelo

## Vue d'ensemble

Le système de traitement vocal Fidelo est un composant avancé du SMA (Système Multi-Agent) qui permet la reconnaissance vocale, la synthèse vocale et l'extraction d'intention en temps réel. Il supporte le français, l'anglais et l'arabe.

## 🚀 Fonctionnalités

### Speech-to-Text (Reconnaissance vocale)
- **Google Speech Recognition** pour une transcription précise
- Support multilingue (français, anglais, arabe)
- Conversion automatique WebM → WAV avec FFmpeg
- Validation des fichiers audio
- Fallback avec pydub si FFmpeg n'est pas disponible

### Text-to-Speech (Synthèse vocale)
- **gTTS (Google Text-to-Speech)** pour une voix naturelle
- Support multilingue complet
- Fallback avec pyttsx3
- Formats de sortie : WAV, MP3

### Extraction d'Intention
- Analyse basique des intentions utilisateur
- Détection d'entités (noms de produits, etc.)
- Support multilingue pour l'analyse

## 📁 Architecture

```
SMA/
├── core/
│   ├── voice_processing_system.py    # Système principal
│   ├── voice_endpoints.py           # Endpoints FastAPI
│   └── main.py                      # Application principale
├── agents/
│   └── voice_agent.py               # Agent vocal intégré
├── requirements.txt                 # Dépendances
├── test_voice_system.py            # Tests
└── README_VOICE_SYSTEM.md          # Documentation
```

## 🛠️ Installation

### 1. Dépendances Python

```bash
cd SMA
pip install -r requirements.txt
```

### 2. FFmpeg (Recommandé)

**Windows:**
```bash
# Via Chocolatey
choco install ffmpeg

# Ou télécharger depuis https://ffmpeg.org/download.html
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

### 3. Vérification de l'installation

```bash
cd SMA
python test_voice_system.py
```

## 🔧 Configuration

### Variables d'environnement

Créez un fichier `.env` dans le dossier `SMA/` :

```env
# API Keys (optionnel pour certaines fonctionnalités)
GEMINI_API_KEY=your_gemini_api_key

# Configuration audio
AUDIO_TEMP_DIR=/tmp/fidelo_audio
AUDIO_SAMPLE_RATE=16000
AUDIO_CHANNELS=1

# Langues par défaut
DEFAULT_LANGUAGE=fr
SUPPORTED_LANGUAGES=fr,en,ar
```

## 📡 API Endpoints

### Endpoints principaux

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/voice/chat` | POST | Traitement complet vocal (transcription + intention) |
| `/voice/transcribe` | POST | Transcription audio → texte |
| `/voice/synthesize` | POST | Synthèse texte → audio |
| `/voice/intent` | POST | Extraction d'intention |
| `/voice/upload` | POST | Upload + transcription de fichier |
| `/voice/capabilities` | GET | Capacités du système |
| `/voice/languages` | GET | Langues supportées |
| `/voice/health` | GET | État de santé |

### Exemples d'utilisation

#### 1. Chat vocal complet

```python
import requests
import base64

# Encoder l'audio en base64
with open("audio.webm", "rb") as f:
    audio_base64 = base64.b64encode(f.read()).decode()

# Requête
response = requests.post("http://localhost:8000/voice/chat", json={
    "audio_data": audio_base64,
    "audio_format": "webm",
    "source_language": "fr"
})

result = response.json()
print(f"Texte transcrit: {result['transcribed_text']}")
print(f"Intention: {result['intent']}")
```

#### 2. Transcription simple

```python
response = requests.post("http://localhost:8000/voice/transcribe", json={
    "audio_data": audio_base64,
    "audio_format": "webm",
    "language": "fr"
})

result = response.json()
print(f"Texte: {result['transcribed_text']}")
```

#### 3. Synthèse vocale

```python
response = requests.post("http://localhost:8000/voice/synthesize", json={
    "text": "Bonjour, je suis Fidelo",
    "language": "fr",
    "output_format": "wav"
})

result = response.json()
if result['success']:
    # Décoder l'audio
    audio_data = base64.b64decode(result['audio_data'])
    with open("output.wav", "wb") as f:
        f.write(audio_data)
```

## 🎯 Intégration avec le Frontend

### WebSocket pour le chat vocal

```javascript
// Connexion WebSocket
const ws = new WebSocket(`ws://localhost:8000/ws/${sessionId}`);

// Envoi d'audio
function sendAudio(audioBlob) {
    const reader = new FileReader();
    reader.onload = () => {
        const base64Audio = reader.result.split(',')[1];
        ws.send(JSON.stringify({
            audio_data: base64Audio,
            audio_format: 'webm'
        }));
    };
    reader.readAsDataURL(audioBlob);
}

// Réception de la transcription
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'response' && data.transcribed_text) {
        // Afficher le texte transcrit dans l'input
        document.getElementById('userInput').value = data.transcribed_text;
    }
};
```

## 🧪 Tests

### Test local du système

```bash
cd SMA
python test_voice_system.py
```

### Test des endpoints

```bash
# Démarrer le serveur
cd SMA
python -m uvicorn core.main:app --reload

# Dans un autre terminal, lancer les tests
python test_voice_system.py
# Répondre 'y' pour tester les endpoints
```

### Tests automatisés

```bash
# Tests unitaires (à implémenter)
pytest tests/test_voice_system.py

# Tests d'intégration
pytest tests/test_voice_endpoints.py
```

## 🔍 Dépannage

### Problèmes courants

#### 1. FFmpeg non trouvé
```
Erreur: FFmpeg non disponible
Solution: Installer FFmpeg selon votre système d'exploitation
```

#### 2. Erreur de transcription
```
Erreur: Audio non reconnu ou trop silencieux
Solutions:
- Vérifier la qualité de l'audio
- S'assurer que l'audio n'est pas trop court
- Vérifier la langue configurée
```

#### 3. Erreur de synthèse vocale
```
Erreur: Impossible de générer l'audio
Solutions:
- Vérifier la connexion internet (gTTS)
- Vérifier que le texte n'est pas vide
- Essayer avec pyttsx3 en fallback
```

#### 4. Problèmes de WebSocket
```
Erreur: Connexion WebSocket échouée
Solutions:
- Vérifier que le serveur est démarré
- Vérifier l'URL de connexion
- Vérifier les paramètres CORS
```

### Logs et debugging

```python
import logging

# Activer les logs détaillés
logging.basicConfig(level=logging.DEBUG)

# Dans le code
logger = logging.getLogger(__name__)
logger.debug("Message de debug")
logger.info("Message d'information")
logger.error("Message d'erreur")
```

## 📊 Performance

### Métriques recommandées

- **Latence de transcription**: < 2 secondes
- **Latence de synthèse**: < 1 seconde
- **Précision de transcription**: > 90%
- **Support concurrent**: 100+ utilisateurs

### Optimisations

1. **Cache des modèles**: Garder les modèles en mémoire
2. **Pool de connexions**: Réutiliser les connexions HTTP
3. **Compression audio**: Optimiser la taille des fichiers
4. **CDN**: Utiliser un CDN pour les fichiers audio

## 🔒 Sécurité

### Bonnes pratiques

1. **Validation des fichiers**: Vérifier les types MIME
2. **Limitation de taille**: Limiter la taille des fichiers audio
3. **Rate limiting**: Limiter le nombre de requêtes par utilisateur
4. **Authentification**: Implémenter l'authentification pour les endpoints sensibles

### Configuration sécurisée

```python
# Limites de sécurité
MAX_AUDIO_SIZE = 10 * 1024 * 1024  # 10MB
MAX_AUDIO_DURATION = 60  # 60 secondes
ALLOWED_FORMATS = ['webm', 'mp3', 'wav', 'm4a']
```

## 🚀 Déploiement

### Docker

```dockerfile
FROM python:3.11-slim

# Installer FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Copier le code
COPY . /app
WORKDIR /app

# Installer les dépendances
RUN pip install -r requirements.txt

# Exposer le port
EXPOSE 8000

# Démarrer l'application
CMD ["uvicorn", "core.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production

```bash
# Avec Gunicorn
pip install gunicorn
gunicorn core.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Avec Docker Compose
docker-compose up -d
```

## 📈 Évolutions futures

### Fonctionnalités prévues

1. **Reconnaissance d'émotions** dans la voix
2. **Diarisation** (identification des locuteurs)
3. **Traduction en temps réel**
4. **Modèles personnalisés** par utilisateur
5. **Support de plus de langues**
6. **Intégration avec des services cloud** (AWS, Azure, Google)

### Améliorations techniques

1. **Streaming audio** pour une latence réduite
2. **Modèles locaux** pour la confidentialité
3. **Optimisation GPU** pour les modèles de transcription
4. **Cache intelligent** pour les réponses fréquentes

## 📞 Support

Pour toute question ou problème :

1. Consulter cette documentation
2. Vérifier les logs d'erreur
3. Tester avec le script de test
4. Ouvrir une issue sur le repository

---

**Fidelo Voice System** - Système de traitement vocal avancé pour l'e-commerce 🎤🛒










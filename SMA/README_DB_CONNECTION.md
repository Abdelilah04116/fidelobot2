# Couche d'Abstraction des Bases de Données

Cette couche d'abstraction permet de connecter facilement votre SMA (Système Multi-Agents) aux deux bases de données :
- **PostgreSQL** (relationnelle) pour les métadonnées
- **Qdrant** (vectorielle) pour les embeddings et la recherche sémantique

## 🏗️ Architecture

```
SMA/
├── core/
│   └── db_connection.py          # Couche d'abstraction principale
├── agents/
│   ├── product_search_agent.py   # Utilise PostgreSQL + Qdrant
│   ├── recommendation_agent.py   # Utilise PostgreSQL + Qdrant
│   └── cart_management_agent.py  # Utilise PostgreSQL uniquement
└── test_db_connections.py        # Script de test
```

## 🚀 Installation

### 1. Variables d'environnement

Créez un fichier `.env` dans le dossier `SMA/` :

```env
# Configuration PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=catalogue_user
POSTGRES_PASSWORD=catalogue_pass
POSTGRES_DB=catalogue

# Configuration Qdrant
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_API_KEY=

# Configuration Gemini (pour les agents)
GEMINI_API_KEY=your_gemini_api_key_here
```

### 2. Dépendances

```bash
pip install sqlalchemy psycopg2-binary qdrant-client python-dotenv
```

## 📖 Utilisation

### Connexion PostgreSQL

```python
from core.db_connection import get_postgres_session

# Utilisation avec context manager (recommandé)
with get_postgres_session() as session:
    # Votre code SQLAlchemy ici
    products = session.query(Product).all()
    # La session est automatiquement commitée et fermée
```

### Connexion Qdrant

```python
from core.db_connection import get_qdrant_client

# Obtenir le client Qdrant
client = get_qdrant_client()

# Recherche vectorielle
results = client.search(
    collection_name="produits_embeddings",
    query_vector=your_vector,
    limit=10
)
```

### Vérification de l'état

```python
from core.db_connection import health_check

# Vérifier l'état des connexions
status = health_check()
print(status)
# Retourne: {"postgres": {"status": "healthy"}, "qdrant": {"status": "healthy"}}
```

## 🔧 Intégration dans les Agents

### Agent utilisant PostgreSQL uniquement

```python
from ..core.db_connection import get_postgres_session

class CartManagementAgent(BaseAgent):
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            with get_postgres_session() as session:
                # Logique métier avec PostgreSQL
                cart_items = session.query(CartItem).filter_by(user_id=user_id).all()
                # ...
        except Exception as e:
            self.logger.error(f"Erreur: {str(e)}")
```

### Agent utilisant PostgreSQL + Qdrant

```python
from ..core.db_connection import get_postgres_session, get_qdrant_client

class ProductSearchAgent(BaseAgent):
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Recherche vectorielle dans Qdrant
            qdrant_client = get_qdrant_client()
            vector_results = qdrant_client.search(
                collection_name="produits_embeddings",
                query_vector=embedding,
                limit=10
            )
            
            # Enrichissement avec PostgreSQL
            with get_postgres_session() as session:
                product_ids = [hit.id for hit in vector_results]
                products = session.query(Product).filter(Product.id.in_(product_ids)).all()
                # ...
        except Exception as e:
            self.logger.error(f"Erreur: {str(e)}")
```

## 🧪 Tests

### Lancer les tests de connexion

```bash
cd SMA
python test_db_connections.py
```

### Tests inclus

- ✅ Test de connexion PostgreSQL
- ✅ Test de connexion Qdrant
- ✅ Test de la fonction health_check
- ✅ Test d'intégration avec un agent

## 🔍 Gestion des Erreurs

### Exceptions personnalisées

```python
from core.db_connection import DatabaseConnectionError

try:
    with get_postgres_session() as session:
        # Votre code
        pass
except DatabaseConnectionError as e:
    print(f"Erreur de connexion: {e}")
```

### Logging

La couche d'abstraction utilise le logging Python standard :

```python
import logging
logging.getLogger("core.db_connection").setLevel(logging.DEBUG)
```

## 📊 Monitoring

### Health Check

```python
from core.db_connection import health_check

# Vérification complète
status = health_check()
for db_name, db_status in status.items():
    print(f"{db_name}: {db_status['status']}")
    if db_status.get('error'):
        print(f"  Erreur: {db_status['error']}")
```

### Métriques

Vous pouvez étendre la classe `DatabaseManager` pour ajouter des métriques :

```python
class DatabaseManager:
    def get_metrics(self):
        return {
            "postgres_connections": self._postgres_engine.pool.size(),
            "qdrant_collections": len(self._qdrant_client.get_collections().collections)
        }
```

## 🔒 Sécurité

### Bonnes pratiques

1. **Variables d'environnement** : Ne jamais hardcoder les credentials
2. **Connection pooling** : Utiliser les context managers pour les sessions
3. **Gestion d'erreurs** : Toujours gérer les exceptions de connexion
4. **Logging** : Logger les erreurs sans exposer les credentials

### Configuration sécurisée

```python
# Dans votre .env
POSTGRES_PASSWORD=your_secure_password_here
QDRANT_API_KEY=your_qdrant_api_key_here

# Utilisation
import os
from dotenv import load_dotenv
load_dotenv()

# Les credentials sont automatiquement chargés
```

## 🚀 Déploiement

### Docker

```yaml
# docker-compose.yml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: catalogue
      POSTGRES_USER: catalogue_user
      POSTGRES_PASSWORD: catalogue_pass
    ports:
      - "5432:5432"
  
  qdrant:
    image: qdrant/qdrant:v1.7.3
    ports:
      - "6333:6333"
      - "6334:6334"
```

### Variables d'environnement en production

```bash
# Dans votre serveur de production
export POSTGRES_HOST=your_prod_db_host
export POSTGRES_PASSWORD=your_prod_password
export QDRANT_HOST=your_prod_qdrant_host
```

## 📝 Exemples Complets

### Exemple 1 : Recherche de produits

```python
async def search_products(query: str, limit: int = 10):
    try:
        # 1. Recherche vectorielle dans Qdrant
        qdrant_client = get_qdrant_client()
        embedding = generate_embedding(query)
        vector_results = qdrant_client.search(
            collection_name="produits_embeddings",
            query_vector=embedding,
            limit=limit
        )
        
        # 2. Enrichissement avec PostgreSQL
        with get_postgres_session() as session:
            product_ids = [hit.id for hit in vector_results]
            products = session.query(Product).filter(Product.id.in_(product_ids)).all()
            
            return [{
                "id": p.id,
                "name": p.nom,
                "price": p.prix,
                "score": next(hit.score for hit in vector_results if hit.id == p.id)
            } for p in products]
            
    except Exception as e:
        logger.error(f"Erreur recherche: {e}")
        return []
```

### Exemple 2 : Gestion du panier

```python
async def add_to_cart(user_id: int, product_id: int, quantity: int = 1):
    try:
        with get_postgres_session() as session:
            # Vérifier le stock
            product = session.query(Product).filter_by(id=product_id).first()
            if not product or product.stock < quantity:
                raise ValueError("Produit non disponible")
            
            # Ajouter au panier
            cart_item = CartItem(
                user_id=user_id,
                product_id=product_id,
                quantity=quantity
            )
            session.add(cart_item)
            session.commit()
            
            return {"success": True, "message": "Produit ajouté au panier"}
            
    except Exception as e:
        logger.error(f"Erreur ajout panier: {e}")
        return {"success": False, "error": str(e)}
```

## 🤝 Contribution

Pour contribuer à cette couche d'abstraction :

1. Respectez les conventions de nommage
2. Ajoutez des tests pour les nouvelles fonctionnalités
3. Documentez les nouvelles méthodes
4. Utilisez le logging pour le debugging

## 📞 Support

En cas de problème :

1. Vérifiez les logs : `logging.getLogger("core.db_connection")`
2. Lancez les tests : `python test_db_connections.py`
3. Vérifiez la configuration : variables d'environnement
4. Consultez la documentation des drivers : SQLAlchemy, qdrant-client

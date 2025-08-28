"""
Couche d'abstraction pour la connexion aux bases de données
PostgreSQL (relationnelle) et Qdrant (vectorielle)

# 🔗 Mapping des agents et leurs bases de données

## 📊 Agents liés à la Base Relationnelle (PostgreSQL)
- cart_management_agent.py → gestion du panier (tables: paniers, panier_produits)
- order_management_agent.py → gestion des commandes et suivi (tables: commandes, commande_produits)
- customer_service_agent.py → tickets service client (table: tickets_service_client)
- customer_profiling_agent.py → stockage des profils clients (table: utilisateurs)
- profiling_agent.py → données comportementales utilisateurs (table: utilisateurs)
- sustainability_agent.py → options écologiques (table: durabilite)

## 🔎 Agents liés à la Base Vectorielle (Qdrant)
- product_search_agent.py → recherche produit via embeddings (collection: produits_embeddings)
- recommendation_agent.py → recommandations hybrides (collections: produits_embeddings, utilisateurs_embeddings)
- social_agent.py → gestion des avis/communauté (collection: avis_embeddings)
- multimodal_agent.py → recherche multimodale (embeddings image/texte, ex: produits_embeddings)

## 🚫 Agents ne nécessitant PAS de base de données
- base_agent.py → classe abstraite
- conversation_agent.py → analyse intention et routage
- escalation_agent.py → escalade vers humain
- summarizer_agent.py → synthèse des réponses
- gdpr_agent.py → conformité RGPD
"""

import os
from typing import Optional, Generator
from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
import logging
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration du logging
logger = logging.getLogger(__name__)

class DatabaseConnectionError(Exception):
    """Exception personnalisée pour les erreurs de connexion"""
    pass

class DatabaseManager:
    """Gestionnaire centralisé des connexions aux bases de données"""
    
    def __init__(self):
        self._postgres_engine = None
        self._postgres_session_factory = None
        self._qdrant_client = None
        self._initialized = False
    
    def initialize(self):
        """Initialise les connexions aux bases de données"""
        if self._initialized:
            return
            
        try:
            # Configuration PostgreSQL
            postgres_host = os.getenv('POSTGRES_HOST', 'localhost')
            postgres_port = os.getenv('POSTGRES_PORT', '5432')
            postgres_user = os.getenv('POSTGRES_USER', 'catalogue_user')
            postgres_password = os.getenv('POSTGRES_PASSWORD', 'catalogue_pass')
            postgres_db = os.getenv('POSTGRES_DB', 'catalogue')
            
            # URL de connexion PostgreSQL
            postgres_url = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
            
            # Créer l'engine PostgreSQL (pool par défaut de SQLAlchemy)
            self._postgres_engine = create_engine(
                postgres_url,
                pool_pre_ping=True,
                pool_recycle=300,
                echo=False  # Mettre à True pour debug SQL
            )
            
            # Créer la factory de sessions
            self._postgres_session_factory = sessionmaker(
                bind=self._postgres_engine,
                autocommit=False,
                autoflush=False
            )
            
            # Configuration Qdrant
            qdrant_host = os.getenv('QDRANT_HOST', 'localhost')
            qdrant_port = int(os.getenv('QDRANT_PORT', '6333'))
            qdrant_api_key = os.getenv('QDRANT_API_KEY', None)
            
            # Créer le client Qdrant
            self._qdrant_client = QdrantClient(
                host=qdrant_host,
                port=qdrant_port,
                api_key=qdrant_api_key,
                prefer_grpc=False,
                timeout=60,
                check_compatibility=False  # Ignorer la vérification de version
            )
            
            # Test des connexions
            self._test_connections()
            
            self._initialized = True
            logger.info("✅ Connexions aux bases de données initialisées avec succès")
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'initialisation des bases de données: {str(e)}")
            raise DatabaseConnectionError(f"Impossible d'initialiser les connexions: {str(e)}")
    
    def _test_connections(self):
        """Teste les connexions aux bases de données"""
        # Test PostgreSQL
        try:
            with self._postgres_engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("✅ Connexion PostgreSQL OK")
        except Exception as e:
            logger.error(f"❌ Erreur connexion PostgreSQL: {str(e)}")
            raise DatabaseConnectionError(f"Connexion PostgreSQL échouée: {str(e)}")
        
        # Test Qdrant
        try:
            collections = self._qdrant_client.get_collections()
            logger.info(f"✅ Connexion Qdrant OK - {len(collections.collections)} collections trouvées")
        except Exception as e:
            logger.warning(f"⚠️ Erreur connexion Qdrant: {str(e)}")
            # On ne lève pas d'exception car Qdrant peut être optionnel
    
    @contextmanager
    def get_postgres_session(self) -> Generator[Session, None, None]:
        """
        Context manager pour obtenir une session PostgreSQL (lecture par défaut).
        Les commits doivent être effectués explicitement par les fonctions d'écriture.
        """
        if not self._initialized:
            self.initialize()
        
        session = self._postgres_session_factory()
        try:
            yield session
        except Exception as e:
            session.rollback()
            logger.error(f"Erreur dans la session PostgreSQL: {str(e)}")
            raise
        finally:
            session.close()
    
    def get_qdrant_client(self) -> QdrantClient:
        """
        Retourne le client Qdrant
        Usage:
            client = db_manager.get_qdrant_client()
            results = client.search(collection_name="produits_embeddings", query_vector=vector)
        """
        if not self._initialized:
            self.initialize()
        
        return self._qdrant_client
    
    def health_check(self) -> dict:
        """Vérifie l'état des connexions aux bases de données"""
        status = {
            "postgres": {"status": "unknown", "error": None},
            "qdrant": {"status": "unknown", "error": None}
        }
        
        # Test PostgreSQL
        try:
            with self.get_postgres_session() as session:
                session.execute(text("SELECT 1"))
            status["postgres"]["status"] = "healthy"
        except Exception as e:
            status["postgres"]["status"] = "unhealthy"
            status["postgres"]["error"] = str(e)
        
        # Test Qdrant
        try:
            self._qdrant_client.get_collections()
            status["qdrant"]["status"] = "healthy"
        except Exception as e:
            status["qdrant"]["status"] = "unhealthy"
            status["qdrant"]["error"] = str(e)
        
        return status
    
    def close(self):
        """Ferme les connexions"""
        if self._postgres_engine:
            self._postgres_engine.dispose()
        if self._qdrant_client:
            self._qdrant_client.close()
        self._initialized = False
        logger.info("🔌 Connexions aux bases de données fermées")

# Instance globale du gestionnaire
db_manager = DatabaseManager()

# Fonctions d'interface simplifiées
def get_postgres_session():
    """Fonction d'interface pour obtenir une session PostgreSQL"""
    return db_manager.get_postgres_session()

def get_qdrant_client():
    """Fonction d'interface pour obtenir le client Qdrant"""
    return db_manager.get_qdrant_client()

def health_check():
    """Fonction d'interface pour vérifier l'état des bases"""
    return db_manager.health_check()

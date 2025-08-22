"""
Configuration de la base de données pour le catalogue des produits
Gestion des connexions, sessions et opérations CRUD
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
from typing import Generator, Optional
import logging
from .catalog_models import Base

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CatalogDatabase:
    """Gestionnaire de base de données pour le catalogue"""
    
    def __init__(self, database_url: str = None):
        """
        Initialise la connexion à la base de données
        
        Args:
            database_url: URL de connexion à la base de données
        """
        self.database_url = database_url or self._get_default_database_url()
        self.engine = None
        self.SessionLocal = None
        self._initialize_database()
    
    def _get_default_database_url(self) -> str:
        """Retourne l'URL de base de données par défaut"""
        # Configuration par défaut pour SQLite (plus simple)
        return "sqlite:///catalogue.db"
    
    def _initialize_database(self):
        """Initialise la connexion et les sessions de base de données"""
        try:
            # Configuration de l'engine avec pool de connexions
            self.engine = create_engine(
                self.database_url,
                poolclass=QueuePool,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                pool_recycle=3600,
                echo=False  # Mettre à True pour le debugging SQL
            )
            
            # Création de la session factory
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
            logger.info("Base de données catalogue initialisée avec succès")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation de la base de données: {e}")
            raise
    
    def create_tables(self):
        """Crée toutes les tables du catalogue"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Tables du catalogue créées avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de la création des tables: {e}")
            raise
    
    def drop_tables(self):
        """Supprime toutes les tables du catalogue"""
        try:
            Base.metadata.drop_all(bind=self.engine)
            logger.info("Tables du catalogue supprimées avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de la suppression des tables: {e}")
            raise
    
    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """
        Context manager pour obtenir une session de base de données
        
        Yields:
            Session: Session SQLAlchemy
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Erreur de session: {e}")
            raise
        finally:
            session.close()
    
    def get_session_direct(self) -> Session:
        """
        Retourne une session directe (à fermer manuellement)
        
        Returns:
            Session: Session SQLAlchemy
        """
        return self.SessionLocal()
    
    def test_connection(self) -> bool:
        """
        Teste la connexion à la base de données
        
        Returns:
            bool: True si la connexion fonctionne
        """
        try:
            with self.get_session() as session:
                result = session.execute(text("SELECT 1"))
                return result.scalar() == 1
        except Exception as e:
            logger.error(f"Test de connexion échoué: {e}")
            return False
    
    def get_database_info(self) -> dict:
        """
        Retourne les informations sur la base de données
        
        Returns:
            dict: Informations sur la base de données
        """
        try:
            with self.get_session() as session:
                # Informations sur les tables
                tables_info = {}
                for table_name in Base.metadata.tables.keys():
                    table = Base.metadata.tables[table_name]
                    tables_info[table_name] = {
                        "columns": len(table.columns),
                        "foreign_keys": len(table.foreign_keys),
                        "indexes": len(table.indexes)
                    }
                
                return {
                    "database_url": self.database_url,
                    "tables_count": len(tables_info),
                    "tables_info": tables_info,
                    "connection_status": "active" if self.test_connection() else "inactive"
                }
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des infos: {e}")
            return {"error": str(e)}
    
    def close(self):
        """Ferme la connexion à la base de données"""
        if self.engine:
            self.engine.dispose()
            logger.info("Connexion à la base de données fermée")

# Instance globale de la base de données
catalog_db = CatalogDatabase()

# Fonction utilitaire pour obtenir une session
def get_catalog_session() -> Session:
    """
    Retourne une session de base de données pour le catalogue
    
    Returns:
        Session: Session SQLAlchemy
    """
    return catalog_db.get_session_direct()

# Fonction utilitaire pour fermer la base de données
def close_catalog_database():
    """Ferme la connexion à la base de données du catalogue"""
    catalog_db.close()

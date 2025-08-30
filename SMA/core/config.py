"""
Configuration du SMA
Fichier temporaire pour éviter les erreurs d'import
"""

import os
from typing import Optional

class Settings:
    """Configuration du système SMA"""
    
    # API Keys (à configurer selon ton environnement)
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY", "AIzaSyBmBWbHclLMWi5b_1r1NLrazOpZWbK5wGs")
    
    # Configuration des bases de données
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/db")
    POSTGRES_URL: Optional[str] = os.getenv("POSTGRES_URL", "postgresql://user:pass@localhost/db")
    QDRANT_URL: Optional[str] = os.getenv("QDRANT_URL", "http://localhost:6333")
    
    # Configuration du système
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Limites et timeouts
    MAX_CONCURRENT_REQUESTS: int = int(os.getenv("MAX_CONCURRENT_REQUESTS", "10"))
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "30"))

# Instance globale des paramètres
settings = Settings()
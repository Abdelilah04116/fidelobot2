import sys
import os

# Ajoute la racine du projet au PYTHONPATH pour l'import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from catalogue.database.catalog_database import catalog_db
from catalogue.database.catalog_models import Base

if __name__ == "__main__":
    print("Création de la base de données du catalogue...")
    Base.metadata.create_all(bind=catalog_db.engine)
    print("Base de données et tables créées avec succès !")
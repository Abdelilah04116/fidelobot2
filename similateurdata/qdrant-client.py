import os
import json
from qdrant_client import QdrantClient

QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
VECTOR_SIZE = 384  # Valeur par défaut

JSON_DIR = "data/json"

client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

for filename in os.listdir(JSON_DIR):
    if filename.endswith(".json"):
        filepath = os.path.join(JSON_DIR, filename)
        collection_name = filename.replace(".json", "")

        print(f"Traitement de {filename} → collection {collection_name}")

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Détection automatique des clés
        sample = data[0]
        id_key = next((k for k in sample.keys() if k in ["id", "id_utilisateur", "id_produit", "id_avis"]), None)
        vector_key = next((k for k in sample.keys() if k in ["embedding", "vector"]), None)

        if not id_key or not vector_key:
            raise ValueError(f"Impossible de trouver la clé d'id ou de vecteur dans {filename}")

        vector_size = len(sample[vector_key])

        # Supprimer la collection si elle existe déjà (ignore l'erreur si elle n'existe pas)
        try:
            client.delete_collection(collection_name)
        except Exception:
            pass

        # Créer la collection
        client.create_collection(
            collection_name=collection_name,
            vectors_config={"size": vector_size, "distance": "Cosine"}
        )

        points = []
        for idx, item in enumerate(data):
            points.append({
                "id": item.get(id_key, idx),
                "vector": item[vector_key],
                "payload": {k: v for k, v in item.items() if k not in [id_key, vector_key]}
            })

        client.upsert(
            collection_name=collection_name,
            points=points
        )

        print(f"  → {len(points)} points insérés dans {collection_name}")

print("Tous les fichiers JSON ont été insérés dans Qdrant !")
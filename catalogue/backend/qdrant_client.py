from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, PointStruct
import os

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))

client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

# Définition des collections et dimensions d'embeddings
COLLECTIONS = {
    "produits_embeddings": 384,  # all-MiniLM-L6-v2
    "utilisateurs_embeddings": 384,
    "avis_embeddings": 384
}

def create_collections():
    for name, dim in COLLECTIONS.items():
        if not client.collection_exists(name):
            client.recreate_collection(
                collection_name=name,
                vectors_config=VectorParams(size=dim, distance=Distance.COSINE)
            )

def insert_embedding(collection, id, embedding, payload=None):
    point = PointStruct(id=id, vector=embedding, payload=payload or {})
    client.upsert(collection_name=collection, points=[point])

def search_embedding(collection, embedding, top_k=5):
    return client.search(collection_name=collection, query_vector=embedding, limit=top_k)

if __name__ == "__main__":
    create_collections()
    print("Collections Qdrant prêtes.")

"""
Outils de recherche vectorielle pour l'agent multimodal
"""
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
import httpx
import asyncio
from qdrant_client import QdrantClient
from qdrant_client.models import SearchRequest, Filter, FieldCondition, MatchValue
import json

class VectorSearchTools:
    """Outils pour la recherche vectorielle de produits"""
    
    def __init__(self, qdrant_host: str = "localhost", qdrant_port: int = 6333):
        self.qdrant_client = QdrantClient(host=qdrant_host, port=qdrant_port)
        self.collection_name = "produits_embeddings"
        
    async def search_products_by_image_similarity(
        self, 
        image_embedding: np.ndarray, 
        limit: int = 10,
        threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Recherche des produits par similarité d'image
        """
        try:
            # Normaliser l'embedding
            normalized_embedding = image_embedding.flatten().astype(np.float32)
            
            # Recherche dans Qdrant
            search_results = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=normalized_embedding.tolist(),
                limit=limit,
                score_threshold=threshold
            )
            
            # Récupérer les détails des produits
            products = []
            for result in search_results:
                product_data = result.payload
                product_data["similarity_score"] = result.score
                products.append(product_data)
            
            return products
            
        except Exception as e:
            print(f"Erreur recherche vectorielle: {e}")
            return []
    
    async def search_products_by_text_similarity(
        self, 
        text_query: str, 
        limit: int = 10,
        threshold: float = 0.6
    ) -> List[Dict[str, Any]]:
        """
        Recherche des produits par similarité textuelle
        """
        try:
            # Utiliser l'API de recherche textuelle
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "http://localhost:8000/api/products/search",
                    params={
                        "q": text_query,
                        "limit": limit,
                        "threshold": threshold
                    }
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"Erreur API recherche: {response.status_code}")
                    return []
                    
        except Exception as e:
            print(f"Erreur recherche textuelle: {e}")
            return []
    
    async def hybrid_search(
        self,
        image_embedding: np.ndarray,
        text_query: str,
        image_weight: float = 0.7,
        text_weight: float = 0.3,
        limit: int = 15
    ) -> List[Dict[str, Any]]:
        """
        Recherche hybride combinant similarité d'image et de texte
        """
        try:
            # Recherche par image
            image_results = await self.search_products_by_image_similarity(
                image_embedding, limit=limit
            )
            
            # Recherche par texte
            text_results = await self.search_products_by_text_similarity(
                text_query, limit=limit
            )
            
            # Combiner et scorer les résultats
            combined_results = self._combine_search_results(
                image_results, text_results, image_weight, text_weight
            )
            
            # Trier par score combiné
            combined_results.sort(key=lambda x: x.get("combined_score", 0), reverse=True)
            
            return combined_results[:limit]
            
        except Exception as e:
            print(f"Erreur recherche hybride: {e}")
            return []
    
    def _combine_search_results(
        self,
        image_results: List[Dict[str, Any]],
        text_results: List[Dict[str, Any]],
        image_weight: float,
        text_weight: float
    ) -> List[Dict[str, Any]]:
        """
        Combine les résultats de recherche image et texte
        """
        # Créer un dictionnaire des produits par ID
        products_dict = {}
        
        # Ajouter les résultats d'image
        for product in image_results:
            product_id = product.get("id")
            if product_id:
                products_dict[product_id] = {
                    **product,
                    "image_score": product.get("similarity_score", 0),
                    "text_score": 0,
                    "combined_score": 0
                }
        
        # Ajouter les résultats de texte
        for product in text_results:
            product_id = product.get("id")
            if product_id:
                if product_id in products_dict:
                    # Produit déjà présent, ajouter le score texte
                    products_dict[product_id]["text_score"] = product.get("similarity_score", 0)
                else:
                    # Nouveau produit
                    products_dict[product_id] = {
                        **product,
                        "image_score": 0,
                        "text_score": product.get("similarity_score", 0),
                        "combined_score": 0
                    }
        
        # Calculer les scores combinés
        for product in products_dict.values():
            combined_score = (
                image_weight * product["image_score"] +
                text_weight * product["text_score"]
            )
            product["combined_score"] = combined_score
        
        return list(products_dict.values())
    
    async def get_product_details(self, product_ids: List[int]) -> List[Dict[str, Any]]:
        """
        Récupère les détails complets des produits
        """
        try:
            # Utiliser l'API pour récupérer les détails
            async with httpx.AsyncClient() as client:
                products = []
                
                for product_id in product_ids:
                    response = await client.get(
                        f"http://localhost:8000/api/products/{product_id}"
                    )
                    
                    if response.status_code == 200:
                        product_data = response.json()
                        products.append(product_data)
                
                return products
                
        except Exception as e:
            print(f"Erreur récupération détails produits: {e}")
            return []
    
    async def search_alternatives(
        self,
        base_product: Dict[str, Any],
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Recherche des alternatives à un produit donné
        """
        try:
            # Extraire les caractéristiques du produit de base
            category = base_product.get("category", "")
            brand = base_product.get("brand", "")
            price_range = base_product.get("price", 0)
            
            # Construire la requête de recherche
            search_query = f"{category} {brand}"
            
            # Rechercher des alternatives
            alternatives = await self.search_products_by_text_similarity(
                search_query, limit=limit * 2
            )
            
            # Filtrer pour exclure le produit de base et les produits trop similaires
            filtered_alternatives = []
            base_id = base_product.get("id")
            
            for alt in alternatives:
                if alt.get("id") != base_id:
                    # Vérifier que le prix est dans une fourchette raisonnable
                    alt_price = alt.get("price", 0)
                    if 0.5 * price_range <= alt_price <= 2.0 * price_range:
                        filtered_alternatives.append(alt)
                        
                        if len(filtered_alternatives) >= limit:
                            break
            
            return filtered_alternatives
            
        except Exception as e:
            print(f"Erreur recherche alternatives: {e}")
            return []
    
    def calculate_similarity_score(
        self,
        embedding1: np.ndarray,
        embedding2: np.ndarray
    ) -> float:
        """
        Calcule le score de similarité entre deux embeddings
        """
        try:
            # Normaliser les embeddings
            norm1 = np.linalg.norm(embedding1)
            norm2 = np.linalg.norm(embedding2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            # Calculer la similarité cosinus
            similarity = np.dot(embedding1.flatten(), embedding2.flatten()) / (norm1 * norm2)
            
            return float(similarity)
            
        except Exception as e:
            print(f"Erreur calcul similarité: {e}")
            return 0.0
    
    async def get_product_images(self, product_id: int) -> List[str]:
        """
        Récupère les URLs des images d'un produit
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"http://localhost:8000/api/products/{product_id}/images"
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return []
                    
        except Exception as e:
            print(f"Erreur récupération images: {e}")
            return []

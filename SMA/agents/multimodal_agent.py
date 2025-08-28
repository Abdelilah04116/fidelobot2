from .base_agent import BaseAgent
from ..tools import ImageProcessingTools, VectorSearchTools
from typing import Dict, Any, List, Optional
import json
import base64
import asyncio

class MultimodalAgent(BaseAgent):
    """
    Agent multimodal pour traiter les images et rechercher des produits
    """
    
    def __init__(self):
        super().__init__(
            name="multimodal_agent",
            description="Agent multimodal pour analyse d'images et recherche de produits"
        )
        # Initialiser les outils
        self.image_tools = ImageProcessingTools()
        self.vector_tools = VectorSearchTools()
    
    def get_system_prompt(self) -> str:
        return """Tu es un agent multimodal spécialisé dans l'analyse d'images de produits e-commerce.

Ton rôle :
1. Analyser les images envoyées par l'utilisateur
2. Extraire les caractéristiques visuelles et textuelles
3. Rechercher des produits correspondants dans le catalogue
4. Proposer des alternatives si le produit exact n'existe pas
5. Retourner des résultats structurés avec images

Contraintes :
- N'invente jamais de produits ou d'images
- Utilise uniquement les résultats des outils de recherche
- Demande des clarifications si nécessaire
- Travaille en collaboration avec les autres agents

Format de sortie JSON strict :
{
  "detected_product": {...},
  "best_match": {...},
  "alternatives_ranked": [...],
  "confidence": 0.95,
  "search_query": "description extraite de l'image"
}"""

    async def process_image(self, image_data: bytes, image_format: str = "webm") -> Dict[str, Any]:
        """
        Traite une image et recherche des produits correspondants
        """
        try:
            # Convertir l'image en format PIL
            image = self._convert_to_pil(image_data, image_format)
            if image is None:
                return self._create_error_response("Impossible de traiter l'image")
            
            # Analyser le contenu de l'image
            image_analysis = self.image_tools.analyze_image_content(image)
            
            # Extraire l'embedding de l'image
            image_embedding = self.image_tools.extract_image_embedding(image)
            if image_embedding is None:
                return self._create_error_response("Impossible d'extraire les caractéristiques de l'image")
            
            # Générer une description textuelle
            search_query = self.image_tools.generate_image_description(image_analysis)
            
            # Recherche hybride (image + texte)
            search_results = await self.vector_tools.hybrid_search(
                image_embedding=image_embedding,
                text_query=search_query,
                image_weight=0.7,
                text_weight=0.3,
                limit=15
            )
            
            # Structurer la réponse
            response = self._structure_response(search_results, search_query, image_analysis)
            
            return response
            
        except Exception as e:
            return self._create_error_response(f"Erreur lors du traitement de l'image: {str(e)}")

    def _convert_to_pil(self, image_data: bytes, image_format: str) -> Optional[Any]:
        """Convertit les données d'image en objet PIL"""
        try:
            # Utiliser les outils d'image pour le décodage
            if image_format == "webm":
                # Pour les images WebM, on essaie de les traiter comme des images
                # En production, il faudrait un décodeur WebM approprié
                return self.image_tools.decode_base64_image(image_data.decode())
            else:
                return self.image_tools.decode_base64_image(image_data.decode())
        except Exception:
            return None

    def _structure_response(self, search_results: List[Dict[str, Any]], search_query: str, image_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Structure la réponse finale de l'agent"""
        try:
            if not search_results:
                return {
                    "detected_product": None,
                    "best_match": None,
                    "alternatives_ranked": [],
                    "confidence": 0.0,
                    "search_query": search_query,
                    "image_analysis": image_analysis,
                    "message": "Aucun produit trouvé correspondant à l'image"
                }
            
            # Premier produit comme meilleur match
            best_match = search_results[0] if search_results else None
            
            # Alternatives classées par pertinence
            alternatives = search_results[1:6] if len(search_results) > 1 else []
            
            # Produit détecté (même que le meilleur match pour l'instant)
            detected_product = best_match
            
            # Calculer la confiance basée sur les scores
            confidence = min(0.95, best_match.get("combined_score", 0.7) if best_match else 0.0)
            
            response = {
                "detected_product": detected_product,
                "best_match": best_match,
                "alternatives_ranked": alternatives,
                "confidence": confidence,
                "search_query": search_query,
                "image_analysis": image_analysis,
                "message": f"Produit trouvé: {best_match.get('name', 'Nom inconnu')} avec {len(alternatives)} alternatives"
            }
            
            return response
            
        except Exception as e:
            return self._create_error_response(f"Erreur structuration: {str(e)}")

    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Crée une réponse d'erreur standardisée"""
            return {
            "detected_product": None,
            "best_match": None,
            "alternatives_ranked": [],
            "confidence": 0.0,
            "search_query": "",
            "error": error_message,
            "message": "Erreur lors du traitement de l'image"
        }

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Méthode principale d'exécution de l'agent
        """
        try:
            # Vérifier si on a des données d'image
            image_data = state.get("audio_data")  # Réutilise le champ audio_data pour les images
            image_format = state.get("audio_format", "webm")
            
            if not image_data:
            return {
                    "response_text": "Aucune image reçue. Veuillez envoyer une image de produit.",
                    "error": "Pas d'image"
                }
            
            # Décoder l'image base64
            try:
                image_bytes = base64.b64decode(image_data)
        except Exception:
            return {
                    "response_text": "Format d'image non reconnu. Veuillez envoyer une image valide.",
                    "error": "Format invalide"
                }
            
            # Traiter l'image
            result = await self.process_image(image_bytes, image_format)
            
            # Mettre à jour l'état
            state["multimodal_result"] = result
            state["agents_used"] = state.get("agents_used", []) + ["multimodal_agent"]
            
            # Générer le texte de réponse
            response_text = self._generate_response_text(result)
            
            # Extraire les produits pour l'UI
            products = self._extract_products_for_ui(result)
                
                return {
                "response_text": response_text,
                "multimodal_result": result,
                "products": products
            }
            
        except Exception as e:
            return {
                "response_text": f"Erreur lors du traitement de l'image: {str(e)}",
                "error": str(e)
            }

    def _generate_response_text(self, result: Dict[str, Any]) -> str:
        """Génère un texte de réponse lisible pour l'utilisateur"""
        if "error" in result:
            return f"❌ {result['error']}"
        
        if not result.get("best_match"):
            return "🔍 Aucun produit correspondant trouvé dans notre catalogue."
        
        best_match = result["best_match"]
        alternatives_count = len(result.get("alternatives_ranked", []))
        confidence = result.get("confidence", 0.0)
        
        response = f"✅ **Produit trouvé !** (Confiance: {confidence:.1%})\n\n"
        response += f"**{best_match.get('name', 'Nom inconnu')}**\n"
        response += f"Prix: {best_match.get('price', 'N/A')}€\n"
        response += f"Stock: {best_match.get('stock', 'N/A')} unités\n\n"
        
        if alternatives_count > 0:
            response += f"🔄 **{alternatives_count} alternatives disponibles**\n"
            for i, alt in enumerate(result["alternatives_ranked"][:3], 1):
                response += f"{i}. {alt.get('name', 'Nom inconnu')} - {alt.get('price', 'N/A')}€\n"
        
        # Ajouter l'analyse de l'image
        if result.get("image_analysis"):
            analysis = result["image_analysis"]
            if analysis.get("text_detected"):
                response += f"\n📝 **Texte détecté dans l'image:** {analysis['text_detected'][:100]}...\n"
        
        return response

    def _extract_products_for_ui(self, result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extrait les produits pour l'affichage dans l'UI"""
        products = []
        
        # Ajouter le meilleur match
        if result.get("best_match"):
            products.append(result["best_match"])
        
        # Ajouter les alternatives
        products.extend(result.get("alternatives_ranked", []))
        
        return products


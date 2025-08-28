"""
Outils de traitement d'images pour l'agent multimodal
"""
import base64
import io
from PIL import Image
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import Dict, Any, List, Optional, Tuple
import cv2
import pytesseract

class ImageProcessingTools:
    """Outils pour le traitement et l'analyse d'images"""
    
    def __init__(self):
        # Modèle d'embedding pour les images
        self.image_encoder = SentenceTransformer('clip-ViT-B-32')
        
        # Modèle de détection d'objets (optionnel)
        self.object_detector = None
        
    def decode_base64_image(self, image_data: str) -> Optional[Image.Image]:
        """Décode une image base64 en objet PIL"""
        try:
            # Enlever le préfixe data:image/...;base64, si présent
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            return image
        except Exception as e:
            print(f"Erreur décodage image: {e}")
            return None
    
    def preprocess_image(self, image: Image.Image, target_size: Tuple[int, int] = (224, 224)) -> Image.Image:
        """Préprocesse l'image pour l'analyse"""
        try:
            # Convertir en RGB si nécessaire
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Redimensionner
            image_resized = image.resize(target_size, Image.Resampling.LANCZOS)
            
            return image_resized
        except Exception as e:
            print(f"Erreur préprocessing: {e}")
            return image
    
    def extract_image_embedding(self, image: Image.Image) -> Optional[np.ndarray]:
        """Extrait l'embedding vectoriel de l'image"""
        try:
            # Préprocesser l'image
            processed_image = self.preprocess_image(image)
            
            # Convertir en array numpy
            image_array = np.array(processed_image)
            
            # Générer l'embedding
            embedding = self.image_encoder.encode([image_array])
            
            return embedding
        except Exception as e:
            print(f"Erreur extraction embedding: {e}")
            return None
    
    def extract_text_from_image(self, image: Image.Image) -> str:
        """Extrait le texte de l'image avec OCR"""
        try:
            # Convertir PIL en OpenCV
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Préprocessing pour améliorer l'OCR
            gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            
            # Extraction du texte
            text = pytesseract.image_to_string(thresh, lang='fra+eng')
            
            return text.strip()
        except Exception as e:
            print(f"Erreur OCR: {e}")
            return ""
    
    def analyze_image_content(self, image: Image.Image) -> Dict[str, Any]:
        """Analyse le contenu de l'image et extrait des métadonnées"""
        try:
            analysis = {
                "size": image.size,
                "mode": image.mode,
                "format": image.format,
                "text_detected": "",
                "dominant_colors": [],
                "brightness": 0.0
            }
            
            # Extraire le texte
            text = self.extract_text_from_image(image)
            analysis["text_detected"] = text
            
            # Analyser les couleurs dominantes
            if image.mode == 'RGB':
                colors = self._extract_dominant_colors(image)
                analysis["dominant_colors"] = colors
            
            # Analyser la luminosité
            brightness = self._calculate_brightness(image)
            analysis["brightness"] = brightness
            
            return analysis
            
        except Exception as e:
            print(f"Erreur analyse contenu: {e}")
            return {"error": str(e)}
    
    def _extract_dominant_colors(self, image: Image.Image, num_colors: int = 5) -> List[Tuple[int, int, int]]:
        """Extrait les couleurs dominantes de l'image"""
        try:
            # Redimensionner pour accélérer le traitement
            small_image = image.resize((50, 50))
            
            # Convertir en array et remodeler
            pixels = np.array(small_image).reshape(-1, 3)
            
            # Utiliser K-means pour trouver les couleurs dominantes
            from sklearn.cluster import KMeans
            kmeans = KMeans(n_clusters=num_colors, random_state=42)
            kmeans.fit(pixels)
            
            # Récupérer les couleurs des centres
            colors = kmeans.cluster_centers_.astype(int)
            
            return [tuple(color) for color in colors]
            
        except Exception as e:
            print(f"Erreur extraction couleurs: {e}")
            return []
    
    def _calculate_brightness(self, image: Image.Image) -> float:
        """Calcule la luminosité moyenne de l'image"""
        try:
            # Convertir en niveaux de gris
            gray = image.convert('L')
            
            # Calculer la luminosité moyenne
            brightness = np.mean(np.array(gray))
            
            return float(brightness) / 255.0  # Normaliser entre 0 et 1
            
        except Exception as e:
            print(f"Erreur calcul luminosité: {e}")
            return 0.0
    
    def generate_image_description(self, analysis: Dict[str, Any]) -> str:
        """Génère une description textuelle de l'image basée sur l'analyse"""
        try:
            description_parts = []
            
            # Ajouter la taille
            if "size" in analysis:
                width, height = analysis["size"]
                description_parts.append(f"Image de {width}x{height} pixels")
            
            # Ajouter le texte détecté
            if analysis.get("text_detected"):
                text = analysis["text_detected"][:100]  # Limiter la longueur
                description_parts.append(f"Contient du texte: {text}")
            
            # Ajouter les couleurs dominantes
            if analysis.get("dominant_colors"):
                colors = analysis["dominant_colors"][:3]  # Limiter à 3 couleurs
                color_names = [self._rgb_to_color_name(color) for color in colors]
                description_parts.append(f"Couleurs dominantes: {', '.join(color_names)}")
            
            # Ajouter la luminosité
            if "brightness" in analysis:
                brightness = analysis["brightness"]
                if brightness > 0.7:
                    description_parts.append("Image claire")
                elif brightness < 0.3:
                    description_parts.append("Image sombre")
                else:
                    description_parts.append("Image de luminosité moyenne")
            
            return ". ".join(description_parts) if description_parts else "Image de produit"
            
        except Exception as e:
            print(f"Erreur génération description: {e}")
            return "Image de produit"
    
    def _rgb_to_color_name(self, rgb: Tuple[int, int, int]) -> str:
        """Convertit des valeurs RGB en noms de couleurs approximatifs"""
        r, g, b = rgb
        
        # Définitions de couleurs basiques
        colors = {
            'rouge': (255, 0, 0),
            'vert': (0, 255, 0),
            'bleu': (0, 0, 255),
            'jaune': (255, 255, 0),
            'cyan': (0, 255, 255),
            'magenta': (255, 0, 255),
            'blanc': (255, 255, 255),
            'noir': (0, 0, 0),
            'gris': (128, 128, 128)
        }
        
        # Trouver la couleur la plus proche
        min_distance = float('inf')
        closest_color = "inconnue"
        
        for color_name, color_rgb in colors.items():
            distance = sum((a - b) ** 2 for a, b in zip(rgb, color_rgb))
            if distance < min_distance:
                min_distance = distance
                closest_color = color_name
        
        return closest_color

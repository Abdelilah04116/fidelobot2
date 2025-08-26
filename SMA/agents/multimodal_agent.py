from .base_agent import BaseAgent
from typing import Dict, Any, List, Optional, Union
from catalogue.backend.database import SessionLocal
from catalogue.backend.models import User, Product, Order
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
import logging
from datetime import datetime, timedelta
import base64
import json
import re
from catalogue.backend.qdrant_client import client as qdrant_client, search_embedding

class MultimodalAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="multimodal_agent",
            description="Agent spécialisé dans l'interaction multimodale (voix, image, vidéo)"
        )
        self.logger = logging.getLogger(__name__)
        
        # Types de médias supportés
        self.supported_media_types = {
            "voice": ["wav", "mp3", "m4a", "ogg"],
            "image": ["jpg", "jpeg", "png", "webp", "gif"],
            "video": ["mp4", "avi", "mov", "webm"]
        }
        
        # Mots-clés pour la recherche visuelle
        self.visual_search_keywords = {
            "couleur": ["rouge", "bleu", "vert", "jaune", "noir", "blanc", "rose", "violet"],
            "style": ["moderne", "classique", "vintage", "minimaliste", "coloré", "neutre"],
            "matériau": ["bois", "métal", "plastique", "tissu", "cuir", "verre", "céramique"],
            "forme": ["rond", "carré", "rectangulaire", "ovale", "triangulaire", "irrégulier"]
        }
    
    def get_system_prompt(self) -> str:
        return """
        Vous êtes un expert en interaction multimodale e-commerce.
        Votre rôle est de traiter et comprendre les entrées vocales, visuelles et vidéo.
        
        Capacités:
        - Reconnaissance et traitement vocal
        - Analyse d'images et recherche visuelle
        - Traitement de vidéos et démonstrations
        - Conversion multimodale (voix vers texte, image vers description)
        - Interface adaptative selon le type de média
        
        Soyez toujours accessible et adaptez votre réponse au format d'entrée.
        """
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        # Exemple de réponse dynamique
        state["response_text"] = "Vous pouvez interagir avec le chatbot via texte, voix ou image pour une expérience enrichie."
        return state
    
    async def process_voice_input_safe(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Traiter une entrée vocale de manière sécurisée"""
        try:
            voice_data = state.get("voice_data", "")
            audio_format = state.get("audio_format", "mp3")
            user_id = state.get("user_id")
            
            if not voice_data:
                return {"error": "Données vocales manquantes"}
            
            if audio_format not in self.supported_media_types["voice"]:
                return {"error": f"Format audio non supporté: {audio_format}"}
            
            # Simulation de traitement vocal (en production, utiliser un service ASR)
            # Ici on simule la conversion voix vers texte
            processed_text = await self._simulate_speech_to_text(voice_data, audio_format)
            
            # Analyser l'intention de la requête vocale
            intent_analysis = await self._analyze_voice_intent(processed_text)
            
            # Générer une réponse adaptée
            voice_response = await self._generate_voice_response(intent_analysis, user_id)
            
            return {
                "success": True,
                "original_audio": {
                    "format": audio_format,
                    "size_bytes": len(voice_data),
                    "duration_estimated": "3-5 secondes"  # Estimation
                },
                "processed_text": processed_text,
                "intent_analysis": intent_analysis,
                "voice_response": voice_response,
                "accessibility": {
                    "text_to_speech_available": True,
                    "voice_commands_supported": True,
                    "language_detection": "français"
                }
            }
            
        except Exception as e:
            self.logger.error(f"Erreur traitement vocal: {str(e)}")
            return {"error": str(e)}
    
    async def _simulate_speech_to_text(self, voice_data: str, audio_format: str) -> str:
        """Simuler la conversion voix vers texte"""
        try:
            # En production, utiliser un service comme Google Speech-to-Text, Azure Speech, etc.
            # Ici on simule avec des patterns courants
            
            # Simuler différents types de requêtes vocales
            simulated_queries = [
                "Je cherche un smartphone pas cher",
                "Montrez-moi les promotions du jour",
                "Quel est le statut de ma commande ?",
                "Je veux retourner un produit",
                "Pouvez-vous m'aider à choisir ?"
            ]
            
            # Retourner une requête simulée basée sur la taille des données
            data_size = len(voice_data)
            query_index = (data_size % len(simulated_queries))
            
            return simulated_queries[query_index]
            
        except Exception:
            return "Requête vocale non comprise"
    
    async def _analyze_voice_intent(self, text: str) -> Dict[str, Any]:
        """Analyser l'intention d'une requête vocale"""
        try:
            text_lower = text.lower()
            
            # Catégoriser l'intention
            intent_categories = {
                "search": ["cherche", "trouve", "montre", "recherche"],
                "order_status": ["commande", "statut", "livraison", "suivi"],
                "help": ["aide", "aide-moi", "peux-tu", "pouvez-vous"],
                "return": ["retour", "retourner", "remboursement", "échange"],
                "promotion": ["promotion", "réduction", "bon plan", "offre"]
            }
            
            detected_intent = "general"
            confidence = 0.0
            
            for intent, keywords in intent_categories.items():
                matches = sum(1 for keyword in keywords if keyword in text_lower)
                if matches > 0:
                    confidence = min(matches / len(keywords), 1.0)
                    if confidence > 0.3:  # Seuil de confiance
                        detected_intent = intent
                        break
            
            # Extraire les entités
            entities = []
            if "smartphone" in text_lower or "téléphone" in text_lower:
                entities.append({"type": "product_category", "value": "smartphone"})
            if "pas cher" in text_lower or "bon marché" in text_lower:
                entities.append({"type": "price_range", "value": "low"})
            if "promotion" in text_lower or "réduction" in text_lower:
                entities.append({"type": "discount", "value": "yes"})
            
            return {
                "intent": detected_intent,
                "confidence": round(confidence, 2),
                "entities": entities,
                "language": "fr",
                "complexity": "simple" if len(text.split()) < 10 else "complex"
            }
            
        except Exception:
            return {"intent": "unknown", "confidence": 0.0, "entities": []}
    
    async def _generate_voice_response(self, intent_analysis: Dict[str, Any], user_id: int) -> Dict[str, Any]:
        """Générer une réponse vocale adaptée"""
        try:
            intent = intent_analysis.get("intent", "general")
            confidence = intent_analysis.get("confidence", 0.0)
            
            # Réponses vocales selon l'intention
            voice_responses = {
                "search": {
                    "text": "Je vais rechercher des produits pour vous. Pouvez-vous me donner plus de détails ?",
                    "suggestions": ["Prix maximum ?", "Marque préférée ?", "Couleur souhaitée ?"],
                    "next_action": "product_search"
                },
                "order_status": {
                    "text": "Je vais vérifier le statut de votre commande. Un instant s'il vous plaît.",
                    "suggestions": ["Numéro de commande ?", "Date d'achat ?"],
                    "next_action": "order_status_check"
                },
                "help": {
                    "text": "Bien sûr, je suis là pour vous aider. Que souhaitez-vous faire ?",
                    "suggestions": ["Rechercher un produit", "Suivre une commande", "Retourner un article"],
                    "next_action": "general_help"
                },
                "return": {
                    "text": "Je vais vous aider pour le retour. Quel est le numéro de commande ?",
                    "suggestions": ["Numéro de commande", "Raison du retour"],
                    "next_action": "return_process"
                },
                "promotion": {
                    "text": "Voici nos promotions actuelles. Je vais vous les présenter.",
                    "suggestions": ["Voir les offres", "Filtrer par catégorie"],
                    "next_action": "promotions_display"
                }
            }
            
            response = voice_responses.get(intent, voice_responses["help"])
            
            return {
                "text": response["text"],
                "suggestions": response["suggestions"],
                "next_action": response["next_action"],
                "confidence": confidence,
                "voice_style": "friendly" if confidence > 0.7 else "clarifying"
            }
            
        except Exception as e:
            self.logger.error(f"Erreur génération réponse vocale: {str(e)}")
            return {"text": "Désolé, je n'ai pas compris. Pouvez-vous reformuler ?"}
    
    async def process_image_input_safe(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Traiter une entrée image de manière sécurisée"""
        try:
            image_data = state.get("image_data", "")
            image_format = state.get("image_format", "jpg")
            user_id = state.get("user_id")
            
            if not image_data:
                return {"error": "Données image manquantes"}
            
            if image_format not in self.supported_media_types["image"]:
                return {"error": f"Format image non supporté: {image_format}"}
            
            # Analyser l'image (en production, utiliser un service de vision par ordinateur)
            image_analysis = await self._analyze_image_content(image_data, image_format)
            
            # Effectuer une recherche visuelle
            visual_search_results = await self.perform_visual_search_safe({
                "image_analysis": image_analysis,
                "user_id": user_id
            })
            
            return {
                "success": True,
                "original_image": {
                    "format": image_format,
                    "size_bytes": len(image_data),
                    "dimensions": "800x600"  # Estimation
                },
                "image_analysis": image_analysis,
                "visual_search_results": visual_search_results,
                "accessibility": {
                    "image_description": image_analysis.get("description", ""),
                    "alt_text_generated": True,
                    "screen_reader_compatible": True
                }
            }
            
        except Exception as e:
            self.logger.error(f"Erreur traitement image: {str(e)}")
            return {"error": str(e)}
    
    async def _analyze_image_content(self, image_data: str, image_format: str) -> Dict[str, Any]:
        """Analyser le contenu d'une image"""
        try:
            # En production, utiliser un service comme Google Vision, Azure Computer Vision, etc.
            # Ici on simule l'analyse avec des patterns courants
            
            # Simuler différents types d'images
            simulated_analyses = [
                {
                    "objects": ["smartphone", "main", "table"],
                    "colors": ["noir", "blanc", "gris"],
                    "style": "moderne",
                    "brand_detected": "Apple",
                    "description": "Smartphone noir moderne sur une table"
                },
                {
                    "objects": ["vêtement", "personne", "miroir"],
                    "colors": ["bleu", "blanc"],
                    "style": "casual",
                    "brand_detected": "Zara",
                    "description": "Vêtement bleu porté par une personne"
                },
                {
                    "objects": ["meuble", "bois", "décoration"],
                    "colors": ["marron", "beige"],
                    "style": "vintage",
                    "brand_detected": "IKEA",
                    "description": "Meuble en bois vintage avec décoration"
                }
            ]
            
            # Retourner une analyse simulée basée sur la taille des données
            data_size = len(image_data)
            analysis_index = (data_size % len(simulated_analyses))
            
            return simulated_analyses[analysis_index]
            
        except Exception:
            return {
                "objects": [],
                "colors": [],
                "style": "unknown",
                "brand_detected": None,
                "description": "Image non analysable"
            }
    
    async def perform_visual_search_safe(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Effectuer une recherche visuelle basée sur l'analyse d'image"""
        try:
            image_analysis = state.get("image_analysis", {})
            user_id = state.get("user_id")
            limit = state.get("limit", 10)
            
            if not image_analysis:
                return {"error": "Analyse d'image requise"}
            
            db = SessionLocal()
            
            try:
                # Construire la requête de recherche basée sur l'analyse
                search_criteria = []
                
                # Recherche par objets détectés
                objects = image_analysis.get("objects", [])
                if objects:
                    for obj in objects:
                        search_criteria.append(f"name LIKE '%{obj}%' OR description LIKE '%{obj}%'")
                
                # Recherche par couleur
                colors = image_analysis.get("colors", [])
                if colors:
                    for color in colors:
                        search_criteria.append(f"description LIKE '%{color}%'")
                
                # Recherche par style
                style = image_analysis.get("style", "")
                if style:
                    search_criteria.append(f"description LIKE '%{style}%'")
                
                # Recherche par marque
                brand = image_analysis.get("brand_detected", "")
                if brand:
                    search_criteria.append(f"brand LIKE '%{brand}%'")
                
                # Construire la requête SQL
                if search_criteria:
                    query_string = " OR ".join(search_criteria)
                    products = db.query(Product).filter(
                        Product.is_active == True,
                        Product.stock_quantity > 0
                    ).filter(query_string).limit(limit).all()
                else:
                    # Recherche par défaut si aucune analyse
                    products = db.query(Product).filter(
                        Product.is_active == True,
                        Product.stock_quantity > 0
                    ).order_by(Product.rating.desc()).limit(limit).all()
                
                # Formater les résultats
                search_results = []
                for product in products:
                    relevance_score = self._calculate_visual_relevance(product, image_analysis)
                    search_results.append({
                        "id": product.id,
                        "name": product.name,
                        "description": product.description,
                        "price": product.price,
                        "image_url": product.image_url,
                        "relevance_score": round(relevance_score, 2),
                        "match_reasons": self._get_match_reasons(product, image_analysis)
                    })
                
                # Trier par pertinence
                search_results.sort(key=lambda x: x["relevance_score"], reverse=True)
                
                return {
                    "search_results": search_results,
                    "total_found": len(search_results),
                    "search_criteria": {
                        "objects": objects,
                        "colors": colors,
                        "style": style,
                        "brand": brand
                    },
                    "visual_search_quality": "high" if search_results else "low"
                }
                
            finally:
                db.close()
                
        except Exception as e:
            self.logger.error(f"Erreur recherche visuelle: {str(e)}")
            return {"error": str(e)}
    
    def _calculate_visual_relevance(self, product: Any, image_analysis: Dict[str, Any]) -> float:
        """Calculer la pertinence visuelle d'un produit"""
        try:
            score = 0.0
            
            # Score par objets
            objects = image_analysis.get("objects", [])
            for obj in objects:
                if obj.lower() in product.name.lower() or obj.lower() in product.description.lower():
                    score += 0.3
            
            # Score par couleur
            colors = image_analysis.get("colors", [])
            for color in colors:
                if color.lower() in product.description.lower():
                    score += 0.2
            
            # Score par style
            style = image_analysis.get("style", "")
            if style and style.lower() in product.description.lower():
                score += 0.25
            
            # Score par marque
            brand = image_analysis.get("brand_detected", "")
            if brand and hasattr(product, 'brand') and brand.lower() in product.brand.lower():
                score += 0.25
            
            return min(score, 1.0)
            
        except Exception:
            return 0.0
    
    def _get_match_reasons(self, product: Any, image_analysis: Dict[str, Any]) -> List[str]:
        """Obtenir les raisons de correspondance"""
        reasons = []
        
        try:
            objects = image_analysis.get("objects", [])
            for obj in objects:
                if obj.lower() in product.name.lower() or obj.lower() in product.description.lower():
                    reasons.append(f"Correspondance avec l'objet: {obj}")
            
            colors = image_analysis.get("colors", [])
            for color in colors:
                if color.lower() in product.description.lower():
                    reasons.append(f"Correspondance de couleur: {color}")
            
            style = image_analysis.get("style", "")
            if style and style.lower() in product.description.lower():
                reasons.append(f"Style similaire: {style}")
            
            brand = image_analysis.get("brand_detected", "")
            if brand and hasattr(product, 'brand') and brand.lower() in product.brand.lower():
                reasons.append(f"Marque détectée: {brand}")
            
        except Exception:
            reasons.append("Correspondance générale")
        
        return reasons[:3]  # Limiter à 3 raisons
    
    async def process_video_input_safe(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Traiter une entrée vidéo de manière sécurisée"""
        try:
            video_data = state.get("video_data", "")
            video_format = state.get("video_format", "mp4")
            user_id = state.get("user_id")
            
            if not video_data:
                return {"error": "Données vidéo manquantes"}
            
            if video_format not in self.supported_media_types["video"]:
                return {"error": f"Format vidéo non supporté: {video_format}"}
            
            # Analyser la vidéo (en production, utiliser un service de vidéo AI)
            video_analysis = await self._analyze_video_content(video_data, video_format)
            
            # Générer des recommandations basées sur la vidéo
            video_recommendations = await self._generate_video_recommendations(video_analysis, user_id)
            
            return {
                "success": True,
                "original_video": {
                    "format": video_format,
                    "size_bytes": len(video_data),
                    "duration_estimated": "15-30 secondes"  # Estimation
                },
                "video_analysis": video_analysis,
                "recommendations": video_recommendations,
                "accessibility": {
                    "video_description": video_analysis.get("description", ""),
                    "subtitles_available": True,
                    "audio_description": False
                }
            }
            
        except Exception as e:
            self.logger.error(f"Erreur traitement vidéo: {str(e)}")
            return {"error": str(e)}
    
    async def _analyze_video_content(self, video_data: str, video_format: str) -> Dict[str, Any]:
        """Analyser le contenu d'une vidéo"""
        try:
            # En production, utiliser un service comme Google Video Intelligence, Azure Video Indexer, etc.
            # Ici on simule l'analyse avec des patterns courants
            
            # Simuler différents types de vidéos
            simulated_analyses = [
                {
                    "type": "product_demo",
                    "objects": ["smartphone", "main", "écran"],
                    "actions": ["défilement", "tap", "swipe"],
                    "duration": "20 secondes",
                    "description": "Démonstration d'un smartphone avec navigation tactile"
                },
                {
                    "type": "unboxing",
                    "objects": ["boîte", "produit", "accessoires"],
                    "actions": ["ouverture", "extraction", "présentation"],
                    "duration": "45 secondes",
                    "description": "Déballage d'un produit avec présentation des accessoires"
                },
                {
                    "type": "tutorial",
                    "objects": ["produit", "personne", "outils"],
                    "actions": ["explication", "démonstration", "instruction"],
                    "duration": "2 minutes",
                    "description": "Tutoriel d'utilisation d'un produit"
                }
            ]
            
            # Retourner une analyse simulée basée sur la taille des données
            data_size = len(video_data)
            analysis_index = (data_size % len(simulated_analyses))
            
            return simulated_analyses[analysis_index]
            
        except Exception:
            return {
                "type": "unknown",
                "objects": [],
                "actions": [],
                "duration": "unknown",
                "description": "Vidéo non analysable"
            }
    
    async def _generate_video_recommendations(self, video_analysis: Dict[str, Any], user_id: int) -> Dict[str, Any]:
        """Générer des recommandations basées sur l'analyse vidéo"""
        try:
            video_type = video_analysis.get("type", "")
            objects = video_analysis.get("objects", [])
            
            recommendations = {
                "related_products": [],
                "tutorials": [],
                "accessories": [],
                "similar_videos": []
            }
            
            # Recommandations selon le type de vidéo
            if video_type == "product_demo":
                recommendations["related_products"] = [
                    "Produits similaires",
                    "Accessoires compatibles",
                    "Versions plus récentes"
                ]
                recommendations["tutorials"] = [
                    "Guide d'utilisation complet",
                    "Astuces et conseils",
                    "Dépannage"
                ]
            elif video_type == "unboxing":
                recommendations["accessories"] = [
                    "Accessoires inclus",
                    "Accessoires recommandés",
                    "Protection et transport"
                ]
            elif video_type == "tutorial":
                recommendations["tutorials"] = [
                    "Tutoriels avancés",
                    "Formation complète",
                    "Support technique"
                ]
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Erreur génération recommandations vidéo: {str(e)}")
            return {"error": str(e)}
    
    async def generate_voice_response_safe(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Générer une réponse vocale à partir de texte"""
        try:
            text = state.get("text", "")
            voice_style = state.get("voice_style", "neutral")
            language = state.get("language", "fr")
            
            if not text:
                return {"error": "Texte requis pour la synthèse vocale"}
            
            # En production, utiliser un service TTS comme Google Text-to-Speech, Azure Speech, etc.
            # Ici on simule la génération vocale
            
            voice_response = {
                "text": text,
                "audio_generated": True,
                "format": "mp3",
                "duration_estimated": f"{len(text.split()) * 0.5:.1f} secondes",
                "voice_style": voice_style,
                "language": language,
                "accessibility": {
                    "speed_adjustable": True,
                    "pitch_adjustable": True,
                    "volume_control": True
                }
            }
            
            return voice_response
            
        except Exception as e:
            self.logger.error(f"Erreur génération réponse vocale: {str(e)}")
            return {"error": str(e)}
    
    async def get_accessibility_features_safe(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Obtenir les fonctionnalités d'accessibilité disponibles"""
        try:
            user_id = state.get("user_id")
            accessibility_needs = state.get("accessibility_needs", [])
            
            # Fonctionnalités d'accessibilité disponibles
            accessibility_features = {
                "voice_commands": {
                    "enabled": True,
                    "languages": ["français", "anglais", "espagnol"],
                    "commands": ["rechercher", "naviguer", "commander", "aider"]
                },
                "text_to_speech": {
                    "enabled": True,
                    "voices": ["homme", "femme", "enfant"],
                    "speed": ["lent", "normal", "rapide"]
                },
                "screen_reader": {
                    "enabled": True,
                    "compatibility": ["NVDA", "JAWS", "VoiceOver", "TalkBack"],
                    "features": ["navigation", "description", "contraste"]
                },
                "visual_aids": {
                    "high_contrast": True,
                    "large_text": True,
                    "color_blind_friendly": True,
                    "font_options": ["Arial", "Verdana", "OpenDyslexic"]
                },
                "navigation_assistance": {
                    "keyboard_only": True,
                    "voice_navigation": True,
                    "gesture_support": True,
                    "simplified_interface": True
                }
            }
            
            # Personnaliser selon les besoins
            if "visual_impairment" in accessibility_needs:
                accessibility_features["voice_commands"]["priority"] = "high"
                accessibility_features["text_to_speech"]["priority"] = "high"
            
            if "motor_impairment" in accessibility_needs:
                accessibility_features["voice_commands"]["priority"] = "high"
                accessibility_features["navigation_assistance"]["keyboard_only"] = True
            
            if "hearing_impairment" in accessibility_needs:
                accessibility_features["visual_aids"]["priority"] = "high"
                accessibility_features["text_to_speech"]["enabled"] = False
            
            return {
                "accessibility_features": accessibility_features,
                "personalized": len(accessibility_needs) > 0,
                "compliance": "WCAG 2.1 AA",
                "support_contact": "accessibilite@fidelobot.com"
            }
            
        except Exception as e:
            self.logger.error(f"Erreur fonctionnalités accessibilité: {str(e)}")
            return {"error": str(e)}


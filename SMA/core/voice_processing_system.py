"""
Système de traitement vocal pour le SMA
Gère la reconnaissance vocale, synthèse vocale et extraction d'intention
"""

import asyncio
import base64
import json
import logging
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, List
import time

# Imports pour la reconnaissance vocale
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    logging.warning("speech_recognition non disponible")

# Imports pour la synthèse vocale
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    logging.warning("gTTS non disponible")

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False
    logging.warning("pyttsx3 non disponible")

logger = logging.getLogger(__name__)

class VoiceProcessingSystem:
    """Système de traitement vocal complet"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer() if SPEECH_RECOGNITION_AVAILABLE else None
        self.ffmpeg_available = self._check_ffmpeg()
        self.temp_dir = Path(tempfile.gettempdir()) / "fidelo_audio"
        self.temp_dir.mkdir(exist_ok=True)
        
        # Configuration des langues supportées
        self.supported_languages = {
            "fr": "fr-FR",
            "en": "en-US", 
            "ar": "ar-SA"
        }
        
        # Patterns d'intention pour l'extraction
        self.intent_patterns = {
            "product_search": [
                "cherche", "recherche", "trouve", "montre", "affiche",
                "search", "find", "show", "display",
                "ابحث", "اعثر", "أظهر", "عرض"
            ],
            "add_to_cart": [
                "ajoute", "mets", "ajouter", "panier", "cart",
                "add", "put", "cart", "basket",
                "أضف", "ضع", "سلة", "عربة"
            ],
            "order_status": [
                "commande", "statut", "livraison", "suivi",
                "order", "status", "delivery", "tracking",
                "طلب", "حالة", "توصيل", "تتبع"
            ],
            "help": [
                "aide", "help", "support", "assistance",
                "help", "support", "assist",
                "مساعدة", "دعم", "مساعدة"
            ]
        }
        
        logger.info("VoiceProcessingSystem initialisé")
    
    def _check_ffmpeg(self) -> bool:
        """Vérifier si FFmpeg est disponible"""
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Retourner les capacités du système"""
        return {
            "system": "VoiceProcessingSystem",
            "capabilities": [
                "speech_to_text",
                "text_to_speech", 
                "intent_extraction",
                "audio_conversion",
                "multilingual_support"
            ],
            "ffmpeg_available": self.ffmpeg_available,
            "speech_recognition_available": SPEECH_RECOGNITION_AVAILABLE,
            "gtts_available": GTTS_AVAILABLE,
            "pyttsx3_available": PYTTSX3_AVAILABLE,
            "languages": list(self.supported_languages.keys())
        }
    
    def get_supported_languages(self) -> List[str]:
        """Retourner les langues supportées"""
        return list(self.supported_languages.keys())
    
    def validate_audio_file(self, audio_data: bytes, format: str) -> bool:
        """Valider un fichier audio"""
        if not audio_data:
            return False
        
        # Vérifier la taille (max 10MB)
        if len(audio_data) > 10 * 1024 * 1024:
            return False
        
        # Vérifier le format
        supported_formats = ['webm', 'mp3', 'wav', 'm4a', 'ogg']
        if format.lower() not in supported_formats:
            return False
        
        return True
    
    async def _convert_to_wav(self, audio_data: bytes, source_format: str) -> Optional[bytes]:
        """Convertir l'audio vers WAV avec FFmpeg"""
        if not self.ffmpeg_available:
            logger.warning("FFmpeg non disponible pour la conversion")
            return None
        
        try:
            # Créer des fichiers temporaires
            input_file = self.temp_dir / f"input.{source_format}"
            output_file = self.temp_dir / "output.wav"
            
            # Écrire les données audio
            with open(input_file, "wb") as f:
                f.write(audio_data)
            
            # Convertir avec FFmpeg
            cmd = [
                "ffmpeg", "-i", str(input_file),
                "-acodec", "pcm_s16le",
                "-ar", "16000",
                "-ac", "1",
                "-y", str(output_file)
            ]
            
            result = subprocess.run(cmd, capture_output=True, check=True)
            
            # Lire le fichier converti
            with open(output_file, "rb") as f:
                wav_data = f.read()
            
            # Nettoyer les fichiers temporaires
            input_file.unlink(missing_ok=True)
            output_file.unlink(missing_ok=True)
            
            return wav_data
            
        except Exception as e:
            logger.error(f"Erreur conversion audio: {e}")
            return None
    
    async def transcribe_audio(self, audio_data: bytes, audio_format: str = "wav", language: str = "fr") -> Dict[str, Any]:
        """Transcrire l'audio en texte"""
        start_time = time.time()
        
        try:
            if not SPEECH_RECOGNITION_AVAILABLE:
                return {
                    "success": False,
                    "error": "Speech recognition non disponible",
                    "transcribed_text": "",
                    "confidence": 0.0
                }
            
            # Valider l'audio
            if not self.validate_audio_file(audio_data, audio_format):
                return {
                    "success": False,
                    "error": "Fichier audio invalide",
                    "transcribed_text": "",
                    "confidence": 0.0
                }
            
            # Convertir vers WAV si nécessaire
            if audio_format.lower() != "wav":
                wav_data = await self._convert_to_wav(audio_data, audio_format)
                if wav_data is None:
                    return {
                        "success": False,
                        "error": "Impossible de convertir l'audio",
                        "transcribed_text": "",
                        "confidence": 0.0
                    }
                audio_data = wav_data
            
            # Créer un fichier temporaire pour la reconnaissance
            temp_file = self.temp_dir / "temp_audio.wav"
            with open(temp_file, "wb") as f:
                f.write(audio_data)
            
            # Transcrire avec Google Speech Recognition
            with sr.AudioFile(str(temp_file)) as source:
                audio = self.recognizer.record(source)
                
                # Obtenir la langue pour la reconnaissance
                lang_code = self.supported_languages.get(language, "fr-FR")
                
                result = self.recognizer.recognize_google(
                    audio,
                    language=lang_code,
                    show_all=True
                )
            
            # Nettoyer le fichier temporaire
            temp_file.unlink(missing_ok=True)
            
            if result and 'alternative' in result:
                # Prendre la première alternative (la plus probable)
                transcribed_text = result['alternative'][0]['transcript']
                confidence = result['alternative'][0].get('confidence', 0.8)
                
                return {
                    "success": True,
                    "transcribed_text": transcribed_text,
                    "confidence": confidence,
                    "language": language,
                    "processing_time": time.time() - start_time
                }
            else:
                return {
                    "success": False,
                    "error": "Aucun texte reconnu",
                    "transcribed_text": "",
                    "confidence": 0.0,
                    "processing_time": time.time() - start_time
                }
                
        except sr.UnknownValueError:
            return {
                "success": False,
                "error": "Audio non reconnu ou trop silencieux",
                "transcribed_text": "",
                "confidence": 0.0,
                "processing_time": time.time() - start_time
            }
        except sr.RequestError as e:
            return {
                "success": False,
                "error": f"Erreur service reconnaissance: {e}",
                "transcribed_text": "",
                "confidence": 0.0,
                "processing_time": time.time() - start_time
            }
        except Exception as e:
            logger.error(f"Erreur transcription: {e}")
            return {
                "success": False,
                "error": str(e),
                "transcribed_text": "",
                "confidence": 0.0,
                "processing_time": time.time() - start_time
            }
    
    async def generate_speech(self, text: str, language: str = "fr", output_format: str = "wav") -> Dict[str, Any]:
        """Générer de la parole à partir de texte"""
        start_time = time.time()
        
        try:
            if not text.strip():
                return {
                    "success": False,
                    "error": "Texte vide",
                    "audio_data": None,
                    "audio_format": output_format
                }
            
            # Essayer d'abord avec gTTS
            if GTTS_AVAILABLE:
                try:
                    tts = gTTS(text=text, lang=language, slow=False)
                    
                    # Créer un fichier temporaire
                    temp_file = self.temp_dir / f"temp_speech.{output_format}"
                    tts.save(str(temp_file))
                    
                    # Lire le fichier généré
                    with open(temp_file, "rb") as f:
                        audio_data = f.read()
                    
                    # Nettoyer
                    temp_file.unlink(missing_ok=True)
                    
                    return {
                        "success": True,
                        "audio_data": base64.b64encode(audio_data).decode(),
                        "audio_format": output_format,
                        "text_length": len(text),
                        "language": language,
                        "processing_time": time.time() - start_time
                    }
                    
                except Exception as e:
                    logger.warning(f"gTTS échoué: {e}")
            
            # Fallback avec pyttsx3
            if PYTTSX3_AVAILABLE:
                try:
                    engine = pyttsx3.init()
                    
                    # Configurer la voix selon la langue
                    voices = engine.getProperty('voices')
                    for voice in voices:
                        if language in voice.languages[0].lower():
                            engine.setProperty('voice', voice.id)
                            break
                    
                    # Créer un fichier temporaire
                    temp_file = self.temp_dir / f"temp_speech.{output_format}"
                    engine.save_to_file(text, str(temp_file))
                    engine.runAndWait()
                    
                    # Lire le fichier généré
                    with open(temp_file, "rb") as f:
                        audio_data = f.read()
                    
                    # Nettoyer
                    temp_file.unlink(missing_ok=True)
                    
                    return {
                        "success": True,
                        "audio_data": base64.b64encode(audio_data).decode(),
                        "audio_format": output_format,
                        "text_length": len(text),
                        "language": language,
                        "processing_time": time.time() - start_time
                    }
                    
                except Exception as e:
                    logger.warning(f"pyttsx3 échoué: {e}")
            
            return {
                "success": False,
                "error": "Aucun service de synthèse vocale disponible",
                "audio_data": None,
                "audio_format": output_format,
                "processing_time": time.time() - start_time
            }
            
        except Exception as e:
            logger.error(f"Erreur synthèse vocale: {e}")
            return {
                "success": False,
                "error": str(e),
                "audio_data": None,
                "audio_format": output_format,
                "processing_time": time.time() - start_time
            }
    
    def _extract_intent(self, text: str, language: str = "fr") -> Dict[str, Any]:
        """Extraire l'intention d'un texte"""
        try:
            text_lower = text.lower().strip()
            
            # Chercher des patterns d'intention
            for intent, patterns in self.intent_patterns.items():
                for pattern in patterns:
                    if pattern.lower() in text_lower:
                        # Calculer un score de confiance basique
                        confidence = min(0.9, 0.5 + (len(pattern) / len(text)) * 0.4)
                        
                        # Extraire des entités basiques
                        entities = []
                        words = text_lower.split()
                        for word in words:
                            if len(word) > 3 and word not in patterns:
                                entities.append(word)
                        
                        return {
                            "intent": intent,
                            "confidence": confidence,
                            "entities": entities[:5],  # Limiter à 5 entités
                            "language": language
                        }
            
            # Intention par défaut
            return {
                "intent": "general_inquiry",
                "confidence": 0.3,
                "entities": [],
                "language": language
            }
            
        except Exception as e:
            logger.error(f"Erreur extraction intention: {e}")
            return {
                "intent": "unknown",
                "confidence": 0.0,
                "entities": [],
                "language": language
            }
    
    async def process_voice_message(self, audio_data: bytes, audio_format: str = "webm", source_language: str = "fr") -> Dict[str, Any]:
        """Traiter un message vocal complet (transcription + intention)"""
        start_time = time.time()
        
        try:
            # Transcrire l'audio
            transcription_result = await self.transcribe_audio(
                audio_data=audio_data,
                audio_format=audio_format,
                language=source_language
            )
            
            if not transcription_result["success"]:
                return {
                    "success": False,
                    "error": transcription_result["error"],
                    "transcribed_text": "",
                    "confidence": 0.0,
                    "language": source_language,
                    "intent": "unknown",
                    "entities": [],
                    "processing_time": time.time() - start_time
                }
            
            # Extraire l'intention du texte transcrit
            intent_result = self._extract_intent(
                transcription_result["transcribed_text"],
                source_language
            )
            
            return {
                "success": True,
                "transcribed_text": transcription_result["transcribed_text"],
                "confidence": transcription_result["confidence"],
                "language": transcription_result["language"],
                "intent": intent_result["intent"],
                "entities": intent_result["entities"],
                "processing_time": time.time() - start_time
            }
            
        except Exception as e:
            logger.error(f"Erreur traitement message vocal: {e}")
            return {
                "success": False,
                "error": str(e),
                "transcribed_text": "",
                "confidence": 0.0,
                "language": source_language,
                "intent": "unknown",
                "entities": [],
                "processing_time": time.time() - start_time
            }

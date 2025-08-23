"""
Système de traitement vocal complet pour Fidelo
- Speech-to-Text avec Google Speech Recognition
- Text-to-Speech avec gTTS
- Support français/anglais/arabe
- Conversion WebM→WAV avec ffmpeg
- Extraction d'intention basique
"""

import asyncio
import json
import logging
import tempfile
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
import base64
import io

# Speech Recognition
import speech_recognition as sr

# Text-to-Speech
from gtts import gTTS
from gtts.lang import tts_langs

# Audio processing
from pydub import AudioSegment
from pydub.playback import play

# Fallback TTS
import pyttsx3

logger = logging.getLogger(__name__)

class VoiceProcessingSystem:
    """
    Système complet de traitement vocal avec support multilingue
    """
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.supported_languages = {
            'fr': 'french',
            'en': 'english', 
            'ar': 'arabic'
        }
        
        # Configuration des langues gTTS
        self.tts_languages = {
            'fr': 'fr',
            'en': 'en',
            'ar': 'ar'
        }
        
        # Fallback TTS engine
        self.fallback_tts = pyttsx3.init()
        self.fallback_tts.setProperty('rate', 150)
        
        # Vérifier ffmpeg
        self.ffmpeg_available = self._check_ffmpeg()
        if not self.ffmpeg_available:
            logger.warning("FFmpeg non disponible. Certaines fonctionnalités audio peuvent ne pas fonctionner.")
        
        # Dossier temporaire pour les fichiers audio
        self.temp_dir = Path(tempfile.gettempdir()) / "fidelo_voice"
        self.temp_dir.mkdir(exist_ok=True)
        
        logger.info("Système de traitement vocal initialisé")
    
    def _check_ffmpeg(self) -> bool:
        """Vérifier si ffmpeg est installé"""
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            return False
    
    async def process_voice_message(self, audio_data: bytes, audio_format: str = "webm", 
                                  source_language: str = "fr") -> Dict[str, Any]:
        """
        Traiter un message vocal complet : transcription + extraction d'intention
        
        Args:
            audio_data: Données audio brutes
            audio_format: Format de l'audio (webm, mp3, wav, etc.)
            source_language: Langue source pour la transcription
            
        Returns:
            Dict avec transcription, intention, et métadonnées
        """
        try:
            # Valider le fichier audio
            if not self.validate_audio_file(audio_data, audio_format):
                return {
                    "success": False,
                    "error": "Fichier audio invalide",
                    "transcribed_text": "",
                    "intent": None,
                    "confidence": 0.0
                }
            
            # Transcrire l'audio
            transcription_result = await self.transcribe_audio(audio_data, audio_format, source_language)
            
            if not transcription_result["success"]:
                return transcription_result
            
            transcribed_text = transcription_result["transcribed_text"]
            
            # Extraire l'intention
            intent_result = self._extract_intent(transcribed_text, source_language)
            
            return {
                "success": True,
                "transcribed_text": transcribed_text,
                "intent": intent_result["intent"],
                "confidence": transcription_result["confidence"],
                "language": transcription_result["language"],
                "entities": intent_result["entities"],
                "processing_time": transcription_result.get("processing_time", 0)
            }
            
        except Exception as e:
            logger.error(f"Erreur lors du traitement vocal: {e}")
            return {
                "success": False,
                "error": str(e),
                "transcribed_text": "",
                "intent": None,
                "confidence": 0.0
            }
    
    async def transcribe_audio(self, audio_data: bytes, audio_format: str = "webm", 
                             language: str = "fr") -> Dict[str, Any]:
        """
        Transcrire l'audio en texte avec Google Speech Recognition
        
        Args:
            audio_data: Données audio brutes
            audio_format: Format de l'audio
            language: Langue pour la transcription
            
        Returns:
            Dict avec le texte transcrit et métadonnées
        """
        try:
            import time
            start_time = time.time()
            
            # Convertir l'audio en WAV si nécessaire
            wav_data = await self._convert_to_wav(audio_data, audio_format)
            
            if not wav_data:
                return {
                    "success": False,
                    "error": "Impossible de convertir l'audio en WAV",
                    "transcribed_text": "",
                    "confidence": 0.0
                }
            
            # Créer un fichier audio temporaire
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(wav_data)
                temp_file_path = temp_file.name
            
            try:
                # Charger l'audio avec speech_recognition
                with sr.AudioFile(temp_file_path) as source:
                    audio = self.recognizer.record(source)
                
                # Configurer la reconnaissance selon la langue
                language_code = self.supported_languages.get(language, 'fr-FR')
                
                # Transcrire avec Google Speech Recognition
                text = self.recognizer.recognize_google(
                    audio, 
                    language=language_code,
                    show_all=False
                )
                
                processing_time = time.time() - start_time
                
                return {
                    "success": True,
                    "transcribed_text": text.strip(),
                    "confidence": 0.9,  # Google ne retourne pas de confidence
                    "language": language,
                    "processing_time": processing_time
                }
                
            finally:
                # Nettoyer le fichier temporaire
                Path(temp_file_path).unlink(mode='ignore_errors')
                
        except sr.UnknownValueError:
            return {
                "success": False,
                "error": "Audio non reconnu ou trop silencieux",
                "transcribed_text": "",
                "confidence": 0.0
            }
        except sr.RequestError as e:
            return {
                "success": False,
                "error": f"Erreur de service de reconnaissance: {e}",
                "transcribed_text": "",
                "confidence": 0.0
            }
        except Exception as e:
            logger.error(f"Erreur lors de la transcription: {e}")
            return {
                "success": False,
                "error": str(e),
                "transcribed_text": "",
                "confidence": 0.0
            }
    
    async def generate_speech(self, text: str, language: str = "fr", 
                            output_format: str = "wav") -> Dict[str, Any]:
        """
        Générer de la parole à partir de texte avec gTTS
        
        Args:
            text: Texte à convertir en parole
            language: Langue pour la synthèse vocale
            output_format: Format de sortie (wav, mp3)
            
        Returns:
            Dict avec les données audio et métadonnées
        """
        try:
            # Valider la langue
            if language not in self.tts_languages:
                language = "fr"  # Fallback
            
            tts_lang = self.tts_languages[language]
            
            # Créer un fichier temporaire pour gTTS
            with tempfile.NamedTemporaryFile(suffix=f".{output_format}", delete=False) as temp_file:
                temp_file_path = temp_file.name
            
            try:
                # Générer la parole avec gTTS
                tts = gTTS(text=text, lang=tts_lang, slow=False)
                tts.save(temp_file_path)
                
                # Lire le fichier généré
                with open(temp_file_path, 'rb') as f:
                    audio_data = f.read()
                
                # Convertir en base64 si nécessaire
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                
                return {
                    "success": True,
                    "audio_data": audio_base64,
                    "audio_format": output_format,
                    "text_length": len(text),
                    "language": language
                }
                
            finally:
                # Nettoyer le fichier temporaire
                Path(temp_file_path).unlink(mode='ignore_errors')
                
        except Exception as e:
            logger.error(f"Erreur lors de la génération vocale: {e}")
            
            # Fallback avec pyttsx3
            try:
                return await self._fallback_tts(text, language, output_format)
            except Exception as fallback_error:
                logger.error(f"Erreur fallback TTS: {fallback_error}")
                return {
                    "success": False,
                    "error": str(e),
                    "audio_data": None,
                    "audio_format": output_format
                }
    
    async def _fallback_tts(self, text: str, language: str, output_format: str) -> Dict[str, Any]:
        """Fallback TTS avec pyttsx3"""
        try:
            # Configurer la voix selon la langue
            voices = self.fallback_tts.getProperty('voices')
            
            # Chercher une voix appropriée
            for voice in voices:
                if language in voice.languages[0].lower() if voice.languages else "":
                    self.fallback_tts.setProperty('voice', voice.id)
                    break
            
            # Créer un fichier temporaire
            with tempfile.NamedTemporaryFile(suffix=f".{output_format}", delete=False) as temp_file:
                temp_file_path = temp_file.name
            
            try:
                # Sauvegarder l'audio
                self.fallback_tts.save_to_file(text, temp_file_path)
                self.fallback_tts.runAndWait()
                
                # Lire le fichier
                with open(temp_file_path, 'rb') as f:
                    audio_data = f.read()
                
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                
                return {
                    "success": True,
                    "audio_data": audio_base64,
                    "audio_format": output_format,
                    "text_length": len(text),
                    "language": language,
                    "method": "fallback_tts"
                }
                
            finally:
                Path(temp_file_path).unlink(mode='ignore_errors')
                
        except Exception as e:
            logger.error(f"Erreur fallback TTS: {e}")
            return {
                "success": False,
                "error": str(e),
                "audio_data": None,
                "audio_format": output_format
            }
    
    def validate_audio_file(self, audio_data: bytes, audio_format: str) -> bool:
        """
        Valider un fichier audio
        
        Args:
            audio_data: Données audio
            audio_format: Format de l'audio
            
        Returns:
            True si le fichier est valide
        """
        try:
            # Vérifier la taille minimale (100 bytes)
            if len(audio_data) < 100:
                return False
            
            # Vérifier le format supporté
            supported_formats = ['webm', 'mp3', 'wav', 'm4a', 'ogg']
            if audio_format.lower() not in supported_formats:
                return False
            
            # Vérifier les headers de fichier
            if audio_format.lower() == 'webm':
                return audio_data.startswith(b'\x1a\x45\xdf\xa3')
            elif audio_format.lower() == 'mp3':
                return audio_data.startswith(b'\xff\xfb') or audio_data.startswith(b'ID3')
            elif audio_format.lower() == 'wav':
                return audio_data.startswith(b'RIFF')
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur validation audio: {e}")
            return False
    
    async def _convert_to_wav(self, audio_data: bytes, source_format: str) -> Optional[bytes]:
        """
        Convertir l'audio en format WAV avec ffmpeg
        
        Args:
            audio_data: Données audio source
            source_format: Format source
            
        Returns:
            Données audio en WAV ou None si erreur
        """
        try:
            if not self.ffmpeg_available:
                # Fallback avec pydub si possible
                return await self._convert_with_pydub(audio_data, source_format)
            
            # Créer des fichiers temporaires
            with tempfile.NamedTemporaryFile(suffix=f".{source_format}", delete=False) as input_file:
                input_file.write(audio_data)
                input_path = input_file.name
            
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as output_file:
                output_path = output_file.name
            
            try:
                # Commande ffmpeg
                cmd = [
                    'ffmpeg',
                    '-i', input_path,
                    '-acodec', 'pcm_s16le',
                    '-ar', '16000',
                    '-ac', '1',
                    '-y',  # Écraser le fichier de sortie
                    output_path
                ]
                
                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                stdout, stderr = await process.communicate()
                
                if process.returncode == 0:
                    # Lire le fichier WAV généré
                    with open(output_path, 'rb') as f:
                        wav_data = f.read()
                    return wav_data
                else:
                    logger.error(f"Erreur ffmpeg: {stderr.decode()}")
                    return None
                    
            finally:
                # Nettoyer les fichiers temporaires
                Path(input_path).unlink(mode='ignore_errors')
                Path(output_path).unlink(mode='ignore_errors')
                
        except Exception as e:
            logger.error(f"Erreur conversion audio: {e}")
            return None
    
    async def _convert_with_pydub(self, audio_data: bytes, source_format: str) -> Optional[bytes]:
        """Conversion avec pydub comme fallback"""
        try:
            # Créer un buffer audio
            audio_buffer = io.BytesIO(audio_data)
            
            # Charger l'audio avec pydub
            if source_format.lower() == 'webm':
                audio = AudioSegment.from_file(audio_buffer, format="webm")
            elif source_format.lower() == 'mp3':
                audio = AudioSegment.from_file(audio_buffer, format="mp3")
            else:
                audio = AudioSegment.from_file(audio_buffer, format=source_format)
            
            # Convertir en WAV
            wav_buffer = io.BytesIO()
            audio.export(wav_buffer, format="wav", parameters=["-ar", "16000", "-ac", "1"])
            
            return wav_buffer.getvalue()
            
        except Exception as e:
            logger.error(f"Erreur conversion pydub: {e}")
            return None
    
    def _extract_intent(self, text: str, language: str = "fr") -> Dict[str, Any]:
        """
        Extraire l'intention basique du texte
        
        Args:
            text: Texte à analyser
            language: Langue du texte
            
        Returns:
            Dict avec intention et entités
        """
        try:
            text_lower = text.lower().strip()
            
            # Intentions basiques en français
            if language == "fr":
                intents = {
                    "recherche_produit": ["cherche", "trouve", "recherche", "veux", "je veux", "j'ai besoin"],
                    "ajouter_panier": ["ajoute", "ajouter", "mets", "mettez", "commande"],
                    "voir_panier": ["panier", "mon panier", "voir panier", "affiche panier"],
                    "supprimer_produit": ["supprime", "enlève", "retire", "annule"],
                    "prix": ["prix", "coût", "combien", "tarif"],
                    "aide": ["aide", "help", "assistance", "comment"],
                    "salutation": ["bonjour", "salut", "hello", "bonsoir"],
                    "au_revoir": ["au revoir", "bye", "à bientôt", "merci"]
                }
            elif language == "en":
                intents = {
                    "search_product": ["search", "find", "look for", "want", "need"],
                    "add_cart": ["add", "put", "order", "buy"],
                    "view_cart": ["cart", "my cart", "show cart", "basket"],
                    "remove_product": ["remove", "delete", "cancel"],
                    "price": ["price", "cost", "how much", "cost"],
                    "help": ["help", "assistance", "how"],
                    "greeting": ["hello", "hi", "good morning", "good evening"],
                    "goodbye": ["goodbye", "bye", "see you", "thank you"]
                }
            elif language == "ar":
                intents = {
                    "search_product": ["ابحث", "أريد", "أحتاج", "ابحث عن"],
                    "add_cart": ["أضف", "اشتر", "اطلب"],
                    "view_cart": ["سلة", "عربة", "مشترياتي"],
                    "help": ["مساعدة", "كيف", "ساعدني"],
                    "greeting": ["مرحبا", "أهلا", "صباح الخير"],
                    "goodbye": ["وداعا", "مع السلامة", "شكرا"]
                }
            else:
                intents = {}
            
            # Détecter l'intention
            detected_intent = "unknown"
            confidence = 0.0
            entities = []
            
            for intent, keywords in intents.items():
                for keyword in keywords:
                    if keyword in text_lower:
                        detected_intent = intent
                        confidence = 0.8
                        break
                if detected_intent != "unknown":
                    break
            
            # Extraction d'entités basique (mots après les mots-clés)
            for intent, keywords in intents.items():
                for keyword in keywords:
                    if keyword in text_lower:
                        # Extraire le texte après le mot-clé
                        parts = text_lower.split(keyword, 1)
                        if len(parts) > 1:
                            entity_text = parts[1].strip()
                            if entity_text:
                                entities.append({
                                    "type": "product_name",
                                    "value": entity_text,
                                    "confidence": 0.7
                                })
                        break
            
            return {
                "intent": detected_intent,
                "confidence": confidence,
                "entities": entities,
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
    
    def get_supported_languages(self) -> Dict[str, Any]:
        """Retourner les langues supportées"""
        return {
            "speech_recognition": list(self.supported_languages.keys()),
            "text_to_speech": list(self.tts_languages.keys()),
            "intent_extraction": ["fr", "en", "ar"]
        }
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Retourner les capacités du système"""
        return {
            "system": "voice_processing",
            "capabilities": [
                "speech_to_text",
                "text_to_speech", 
                "intent_extraction",
                "audio_conversion",
                "multilingual_support"
            ],
            "supported_formats": ["webm", "mp3", "wav", "m4a", "ogg"],
            "ffmpeg_available": self.ffmpeg_available,
            "languages": self.get_supported_languages()
        }

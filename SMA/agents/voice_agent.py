"""
Agent de traitement vocal pour le SMA
Gère la réception d'audio, conversion ffmpeg, et transcription voix->texte
Utilise le nouveau système de traitement vocal avec Google Speech Recognition
"""

import asyncio
import json
import logging
import os
import tempfile
import subprocess
from typing import Dict, Any, Optional
from pathlib import Path
import base64

from .base_agent import BaseAgent
from ..core.voice_processing_system import VoiceProcessingSystem

logger = logging.getLogger(__name__)

class VoiceAgent(BaseAgent):
    """Agent spécialisé dans le traitement vocal et la transcription audio"""
    
    def __init__(self):
        super().__init__("voice_agent", "Agent de traitement vocal et transcription audio")
        
        # Initialiser le système de traitement vocal
        self.voice_system = VoiceProcessingSystem()
        
        # Capacités de l'agent
        self.supported_formats = ['.webm', '.mp3', '.wav', '.m4a', '.ogg']
        self.temp_dir = Path(tempfile.gettempdir()) / "fidelo_audio"
        self.temp_dir.mkdir(exist_ok=True)
        
        logger.info("VoiceAgent initialisé avec le système de traitement vocal")
    
    def get_system_prompt(self) -> str:
        """Retourne le prompt système pour l'agent voix"""
        return """Tu es un agent spécialisé dans le traitement vocal et la transcription audio.
Tu utilises Google Speech Recognition pour la transcription et gTTS pour la synthèse vocale.
Tu supportes le français, l'anglais et l'arabe.
Tu extrais aussi les intentions basiques des messages vocaux."""
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Exécute la logique principale de l'agent voix"""
        try:
            # Vérifier si on a des données audio
            audio_data = state.get("audio_data")
            audio_format = state.get("audio_format", "webm")
            source_language = state.get("source_language", "fr")
            
            if not audio_data:
                return {
                    "success": False,
                    "error": "Aucune donnée audio fournie",
                    "transcribed_text": ""
                }
            
            # Traiter l'audio avec le nouveau système
            result = await self.voice_system.process_voice_message(
                audio_data=audio_data,
                audio_format=audio_format,
                source_language=source_language
            )
            
            return {
                "success": result["success"],
                "transcribed_text": result.get("transcribed_text", ""),
                "confidence": result.get("confidence", 0.0),
                "language": result.get("language", source_language),
                "intent": result.get("intent"),
                "entities": result.get("entities", []),
                "error": result.get("error", "")
            }
            
        except Exception as e:
            logger.error(f"Erreur dans execute: {e}")
            return {
                "success": False,
                "error": str(e),
                "transcribed_text": ""
            }
    
    async def process_audio(self, audio_data: bytes, format: str = "webm") -> Dict[str, Any]:
        """
        Traiter l'audio reçu et le convertir en texte
        Utilise le nouveau système de traitement vocal
        
        Args:
            audio_data: Données audio brutes
            format: Format de l'audio (webm, mp3, etc.)
            
        Returns:
            Dict contenant le texte transcrit et les métadonnées
        """
        try:
            # Utiliser le système de traitement vocal
            result = await self.voice_system.process_voice_message(
                audio_data=audio_data,
                audio_format=format,
                source_language="fr"  # Langue par défaut
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Erreur lors du traitement audio: {e}")
            return {
                "success": False,
                "error": str(e),
                "transcribed_text": ""
            }
    
    async def transcribe_audio(self, audio_data: bytes, format: str = "webm", language: str = "fr") -> Dict[str, Any]:
        """
        Transcrire l'audio en texte avec Google Speech Recognition
        
        Args:
            audio_data: Données audio brutes
            format: Format de l'audio
            language: Langue pour la transcription
            
        Returns:
            Dict avec le texte transcrit et métadonnées
        """
        try:
            return await self.voice_system.transcribe_audio(
                audio_data=audio_data,
                audio_format=format,
                language=language
            )
            
        except Exception as e:
            logger.error(f"Erreur lors de la transcription: {e}")
            return {
                "success": False,
                "error": str(e),
                "transcribed_text": "",
                "confidence": 0.0
            }
    
    async def generate_speech(self, text: str, language: str = "fr", output_format: str = "wav") -> Dict[str, Any]:
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
            return await self.voice_system.generate_speech(
                text=text,
                language=language,
                output_format=output_format
            )
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération vocale: {e}")
            return {
                "success": False,
                "error": str(e),
                "audio_data": None,
                "audio_format": output_format
            }
    
    def extract_intent(self, text: str, language: str = "fr") -> Dict[str, Any]:
        """
        Extraire l'intention d'un texte
        
        Args:
            text: Texte à analyser
            language: Langue du texte
            
        Returns:
            Dict avec intention et entités
        """
        try:
            return self.voice_system._extract_intent(text, language)
            
        except Exception as e:
            logger.error(f"Erreur extraction intention: {e}")
            return {
                "intent": "unknown",
                "confidence": 0.0,
                "entities": [],
                "language": language
            }
    
    async def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gérer les messages audio reçus
        """
        try:
            if message.get("type") == "audio":
                # Extraire les données audio
                audio_data = message.get("audio_data")
                format = message.get("format", "webm")
                language = message.get("language", "fr")
                
                if not audio_data:
                    return {
                        "success": False,
                        "error": "Données audio manquantes",
                        "transcribed_text": ""
                    }
                
                # Décoder les données base64 si nécessaire
                if isinstance(audio_data, str):
                    try:
                        audio_bytes = base64.b64decode(audio_data)
                    except Exception:
                        return {
                            "success": False,
                            "error": "Format de données audio invalide",
                            "transcribed_text": ""
                        }
                else:
                    audio_bytes = audio_data
                
                # Traiter l'audio avec le nouveau système
                result = await self.voice_system.process_voice_message(
                    audio_data=audio_bytes,
                    audio_format=format,
                    source_language=language
                )
                
                return {
                    "agent": "voice_agent",
                    "success": result["success"],
                    "transcribed_text": result.get("transcribed_text", ""),
                    "confidence": result.get("confidence", 0.0),
                    "language": result.get("language", language),
                    "intent": result.get("intent"),
                    "entities": result.get("entities", []),
                    "error": result.get("error", "")
                }
            
            return {
                "agent": "voice_agent",
                "success": False,
                "error": "Type de message non supporté",
                "transcribed_text": ""
            }
            
        except Exception as e:
            logger.error(f"Erreur dans voice_agent: {e}")
            return {
                "agent": "voice_agent",
                "success": False,
                "error": str(e),
                "transcribed_text": ""
            }
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Retourner les capacités de l'agent"""
        voice_capabilities = self.voice_system.get_capabilities()
        
        return {
            "agent_name": "voice_agent",
            "capabilities": [
                "audio_processing",
                "voice_to_text",
                "text_to_speech",
                "audio_conversion",
                "intent_extraction",
                "multilingual_support"
            ],
            "supported_formats": self.supported_formats,
            "voice_system_capabilities": voice_capabilities,
            "supported_languages": self.voice_system.get_supported_languages()
        }

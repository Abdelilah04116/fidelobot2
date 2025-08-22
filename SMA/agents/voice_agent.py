"""
Agent de traitement vocal pour le SMA
Gère la réception d'audio, conversion ffmpeg, et transcription voix->texte
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

# Pour la transcription (Whisper ou alternative)
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    logging.warning("Whisper non disponible. Utilisation d'un service de transcription alternatif.")

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class VoiceAgent(BaseAgent):
    """Agent spécialisé dans le traitement vocal et la transcription audio"""
    
    def __init__(self):
        super().__init__("voice_agent", "Agent de traitement vocal et transcription audio")
        self.supported_formats = ['.webm', '.mp3', '.wav', '.m4a', '.ogg']
        self.temp_dir = Path(tempfile.gettempdir()) / "fidelo_audio"
        self.temp_dir.mkdir(exist_ok=True)
        
        # Vérifier ffmpeg
        self.ffmpeg_available = self._check_ffmpeg()
        if not self.ffmpeg_available:
            logger.error("FFmpeg non disponible. L'agent voix ne peut pas fonctionner.")
        
        # Initialiser Whisper si disponible
        if WHISPER_AVAILABLE:
            try:
                self.whisper_model = whisper.load_model("base")
                logger.info("Modèle Whisper chargé avec succès")
            except Exception as e:
                logger.error(f"Erreur lors du chargement de Whisper: {e}")
                self.whisper_model = None
        else:
            self.whisper_model = None
    
    def get_system_prompt(self) -> str:
        """Retourne le prompt système pour l'agent voix"""
        return """Tu es un agent spécialisé dans le traitement vocal et la transcription audio.
Tu utilises ffmpeg pour convertir l'audio et Whisper pour la transcription.
Tu ne génères pas de réponses textuelles, tu traites uniquement l'audio."""
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Exécute la logique principale de l'agent voix"""
        try:
            # Vérifier si on a des données audio
            audio_data = state.get("audio_data")
            audio_format = state.get("audio_format", "webm")
            
            if not audio_data:
                return {
                    "success": False,
                    "error": "Aucune donnée audio fournie",
                    "transcribed_text": ""
                }
            
            # Traiter l'audio
            result = await self.process_audio(audio_data, audio_format)
            
            return {
                "success": result["success"],
                "transcribed_text": result.get("transcribed_text", ""),
                "confidence": result.get("confidence", 0.0),
                "language": result.get("language", "unknown"),
                "error": result.get("error", "")
            }
            
        except Exception as e:
            logger.error(f"Erreur dans execute: {e}")
            return {
                "success": False,
                "error": str(e),
                "transcribed_text": ""
            }
    
    def _check_ffmpeg(self) -> bool:
        """Vérifier si ffmpeg est installé et accessible"""
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            return False
    
    async def process_audio(self, audio_data: bytes, format: str = "webm") -> Dict[str, Any]:
        """
        Traiter l'audio reçu et le convertir en texte
        
        Args:
            audio_data: Données audio brutes
            format: Format de l'audio (webm, mp3, etc.)
            
        Returns:
            Dict contenant le texte transcrit et les métadonnées
        """
        try:
            if not self.ffmpeg_available:
                return {
                    "success": False,
                    "error": "FFmpeg non disponible",
                    "transcribed_text": ""
                }
            
            # Créer un fichier temporaire pour l'audio
            temp_audio = self.temp_dir / f"input_{self._generate_id()}.{format}"
            temp_wav = self.temp_dir / f"converted_{self._generate_id()}.wav"
            
            # Sauvegarder l'audio reçu
            with open(temp_audio, 'wb') as f:
                f.write(audio_data)
            
            # Convertir avec ffmpeg
            conversion_success = await self._convert_audio(temp_audio, temp_wav)
            
            if not conversion_success:
                return {
                    "success": False,
                    "error": "Erreur lors de la conversion audio",
                    "transcribed_text": ""
                }
            
            # Transcrire l'audio
            transcription_result = await self._transcribe_audio(temp_wav)
            
            # Nettoyer les fichiers temporaires
            self._cleanup_files([temp_audio, temp_wav])
            
            return transcription_result
            
        except Exception as e:
            logger.error(f"Erreur lors du traitement audio: {e}")
            return {
                "success": False,
                "error": str(e),
                "transcribed_text": ""
            }
    
    async def _convert_audio(self, input_file: Path, output_file: Path) -> bool:
        """
        Convertir l'audio en format WAV avec ffmpeg
        """
        try:
            cmd = [
                'ffmpeg',
                '-i', str(input_file),
                '-acodec', 'pcm_s16le',
                '-ar', '16000',
                '-ac', '1',
                '-y',  # Écraser le fichier de sortie
                str(output_file)
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                logger.info(f"Conversion audio réussie: {input_file} -> {output_file}")
                return True
            else:
                logger.error(f"Erreur conversion ffmpeg: {stderr.decode()}")
                return False
                
        except Exception as e:
            logger.error(f"Erreur lors de la conversion audio: {e}")
            return False
    
    async def _transcribe_audio(self, audio_file: Path) -> Dict[str, Any]:
        """
        Transcrire l'audio en texte
        """
        try:
            if self.whisper_model:
                # Utiliser Whisper local
                result = self.whisper_model.transcribe(str(audio_file))
                transcribed_text = result["text"].strip()
                
                return {
                    "success": True,
                    "transcribed_text": transcribed_text,
                    "confidence": result.get("confidence", 0.0),
                    "language": result.get("language", "unknown"),
                    "method": "whisper_local"
                }
            else:
                # Fallback: simulation de transcription
                # En production, utiliser un service comme Google Speech-to-Text, Azure, etc.
                await asyncio.sleep(1)  # Simuler le temps de traitement
                
                return {
                    "success": True,
                    "transcribed_text": "[Texte transcrit simulé - configurez Whisper ou un service de transcription]",
                    "confidence": 0.8,
                    "language": "fr",
                    "method": "simulation"
                }
                
        except Exception as e:
            logger.error(f"Erreur lors de la transcription: {e}")
            return {
                "success": False,
                "error": str(e),
                "transcribed_text": ""
            }
    
    def _generate_id(self) -> str:
        """Générer un ID unique pour les fichiers temporaires"""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def _cleanup_files(self, files: list):
        """Nettoyer les fichiers temporaires"""
        for file_path in files:
            try:
                if file_path.exists():
                    file_path.unlink()
            except Exception as e:
                logger.warning(f"Impossible de supprimer {file_path}: {e}")
    
    async def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gérer les messages audio reçus
        """
        try:
            if message.get("type") == "audio":
                # Extraire les données audio
                audio_data = message.get("audio_data")
                format = message.get("format", "webm")
                
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
                
                # Traiter l'audio
                result = await self.process_audio(audio_bytes, format)
                
                return {
                    "agent": "voice_agent",
                    "success": result["success"],
                    "transcribed_text": result.get("transcribed_text", ""),
                    "confidence": result.get("confidence", 0.0),
                    "language": result.get("language", "unknown"),
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
        return {
            "agent_name": "voice_agent",
            "capabilities": [
                "audio_processing",
                "voice_to_text",
                "audio_conversion"
            ],
            "supported_formats": self.supported_formats,
            "ffmpeg_available": self.ffmpeg_available,
            "whisper_available": WHISPER_AVAILABLE and self.whisper_model is not None
        }

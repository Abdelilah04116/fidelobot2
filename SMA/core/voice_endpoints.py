"""
Endpoints FastAPI pour le traitement vocal
- /voice-chat : Traitement complet vocal
- /voice/transcribe : Transcription audio
- /voice/synthesize : Synthèse vocale
- /voice/intent : Extraction d'intention
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import base64
import logging

from .voice_processing_system import VoiceProcessingSystem

logger = logging.getLogger(__name__)

# Initialiser le système de traitement vocal
voice_system = VoiceProcessingSystem()

# Router pour les endpoints vocaux
voice_router = APIRouter(prefix="/voice", tags=["voice"])

# Modèles Pydantic
class VoiceChatRequest(BaseModel):
    """Requête pour le chat vocal"""
    audio_data: str  # Base64 encoded audio
    audio_format: str = "webm"
    source_language: str = "fr"
    target_language: Optional[str] = None

class VoiceChatResponse(BaseModel):
    """Réponse du chat vocal"""
    success: bool
    transcribed_text: str
    intent: Optional[str] = None
    confidence: float
    language: str
    entities: list = []
    processing_time: float = 0.0
    error: Optional[str] = None

class TranscribeRequest(BaseModel):
    """Requête de transcription"""
    audio_data: str  # Base64 encoded audio
    audio_format: str = "webm"
    language: str = "fr"

class TranscribeResponse(BaseModel):
    """Réponse de transcription"""
    success: bool
    transcribed_text: str
    confidence: float
    language: str
    processing_time: float = 0.0
    error: Optional[str] = None

class SynthesizeRequest(BaseModel):
    """Requête de synthèse vocale"""
    text: str
    language: str = "fr"
    output_format: str = "wav"

class SynthesizeResponse(BaseModel):
    """Réponse de synthèse vocale"""
    success: bool
    audio_data: Optional[str] = None  # Base64 encoded audio
    audio_format: str
    text_length: int = 0
    language: str
    error: Optional[str] = None

class IntentRequest(BaseModel):
    """Requête d'extraction d'intention"""
    text: str
    language: str = "fr"

class IntentResponse(BaseModel):
    """Réponse d'extraction d'intention"""
    success: bool
    intent: str
    confidence: float
    entities: list = []
    language: str
    error: Optional[str] = None

@voice_router.post("/chat", response_model=VoiceChatResponse)
async def voice_chat(request: VoiceChatRequest):
    """
    Endpoint principal pour le chat vocal
    Traite l'audio, transcrit, extrait l'intention et génère une réponse
    """
    try:
        # Décoder l'audio base64
        try:
            audio_bytes = base64.b64decode(request.audio_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Format audio invalide: {e}")
        
        # Traiter le message vocal
        result = await voice_system.process_voice_message(
            audio_data=audio_bytes,
            audio_format=request.audio_format,
            source_language=request.source_language
        )
        
        if not result["success"]:
            return VoiceChatResponse(
                success=False,
                transcribed_text="",
                intent=None,
                confidence=0.0,
                language=request.source_language,
                entities=[],
                processing_time=0.0,
                error=result.get("error", "Erreur inconnue")
            )
        
        return VoiceChatResponse(
            success=True,
            transcribed_text=result["transcribed_text"],
            intent=result.get("intent"),
            confidence=result.get("confidence", 0.0),
            language=result.get("language", request.source_language),
            entities=result.get("entities", []),
            processing_time=result.get("processing_time", 0.0)
        )
        
    except Exception as e:
        logger.error(f"Erreur dans voice_chat: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")

@voice_router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe_audio(request: TranscribeRequest):
    """
    Transcrire l'audio en texte
    """
    try:
        # Décoder l'audio base64
        try:
            audio_bytes = base64.b64decode(request.audio_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Format audio invalide: {e}")
        
        # Transcrire l'audio
        result = await voice_system.transcribe_audio(
            audio_data=audio_bytes,
            audio_format=request.audio_format,
            language=request.language
        )
        
        if not result["success"]:
            return TranscribeResponse(
                success=False,
                transcribed_text="",
                confidence=0.0,
                language=request.language,
                processing_time=0.0,
                error=result.get("error", "Erreur inconnue")
            )
        
        return TranscribeResponse(
            success=True,
            transcribed_text=result["transcribed_text"],
            confidence=result.get("confidence", 0.0),
            language=result.get("language", request.language),
            processing_time=result.get("processing_time", 0.0)
        )
        
    except Exception as e:
        logger.error(f"Erreur dans transcribe_audio: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")

@voice_router.post("/synthesize", response_model=SynthesizeResponse)
async def synthesize_speech(request: SynthesizeRequest):
    """
    Générer de la parole à partir de texte
    """
    try:
        # Générer la parole
        result = await voice_system.generate_speech(
            text=request.text,
            language=request.language,
            output_format=request.output_format
        )
        
        if not result["success"]:
            return SynthesizeResponse(
                success=False,
                audio_data=None,
                audio_format=request.output_format,
                text_length=len(request.text),
                language=request.language,
                error=result.get("error", "Erreur inconnue")
            )
        
        return SynthesizeResponse(
            success=True,
            audio_data=result["audio_data"],
            audio_format=result.get("audio_format", request.output_format),
            text_length=result.get("text_length", len(request.text)),
            language=result.get("language", request.language)
        )
        
    except Exception as e:
        logger.error(f"Erreur dans synthesize_speech: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")

@voice_router.post("/intent", response_model=IntentResponse)
async def extract_intent(request: IntentRequest):
    """
    Extraire l'intention d'un texte
    """
    try:
        # Extraire l'intention
        result = voice_system._extract_intent(
            text=request.text,
            language=request.language
        )
        
        return IntentResponse(
            success=True,
            intent=result["intent"],
            confidence=result.get("confidence", 0.0),
            entities=result.get("entities", []),
            language=result.get("language", request.language)
        )
        
    except Exception as e:
        logger.error(f"Erreur dans extract_intent: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")

@voice_router.post("/upload", response_model=TranscribeResponse)
async def upload_and_transcribe(
    file: UploadFile = File(...),
    language: str = Form("fr"),
    audio_format: Optional[str] = Form(None)
):
    """
    Uploader un fichier audio et le transcrire
    """
    try:
        # Lire le fichier uploadé
        audio_data = await file.read()
        
        # Déterminer le format
        if audio_format:
            detected_format = audio_format
        else:
            detected_format = file.filename.split('.')[-1] if file.filename else "webm"
        
        # Valider le fichier
        if not voice_system.validate_audio_file(audio_data, detected_format):
            raise HTTPException(status_code=400, detail="Fichier audio invalide")
        
        # Transcrire
        result = await voice_system.transcribe_audio(
            audio_data=audio_data,
            audio_format=detected_format,
            language=language
        )
        
        if not result["success"]:
            return TranscribeResponse(
                success=False,
                transcribed_text="",
                confidence=0.0,
                language=language,
                processing_time=0.0,
                error=result.get("error", "Erreur inconnue")
            )
        
        return TranscribeResponse(
            success=True,
            transcribed_text=result["transcribed_text"],
            confidence=result.get("confidence", 0.0),
            language=result.get("language", language),
            processing_time=result.get("processing_time", 0.0)
        )
        
    except Exception as e:
        logger.error(f"Erreur dans upload_and_transcribe: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")

@voice_router.get("/capabilities")
async def get_voice_capabilities():
    """
    Obtenir les capacités du système vocal
    """
    try:
        capabilities = voice_system.get_capabilities()
        return JSONResponse(content=capabilities)
    except Exception as e:
        logger.error(f"Erreur dans get_voice_capabilities: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")

@voice_router.get("/languages")
async def get_supported_languages():
    """
    Obtenir les langues supportées
    """
    try:
        languages = voice_system.get_supported_languages()
        return JSONResponse(content=languages)
    except Exception as e:
        logger.error(f"Erreur dans get_supported_languages: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")

@voice_router.get("/health")
async def voice_health_check():
    """
    Vérifier la santé du système vocal
    """
    try:
        health_status = {
            "status": "healthy",
            "ffmpeg_available": voice_system.ffmpeg_available,
            "supported_languages": list(voice_system.supported_languages.keys()),
            "tts_languages": list(voice_system.tts_languages.keys())
        }
        return JSONResponse(content=health_status)
    except Exception as e:
        logger.error(f"Erreur dans voice_health_check: {e}")
        return JSONResponse(
            content={"status": "unhealthy", "error": str(e)},
            status_code=500
        )



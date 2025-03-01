"""
Voice API Module

This module provides API endpoints for voice-related functionality, including:
- Speech-to-Text (STT): Converting audio to text
- Text-to-Speech (TTS): Converting text to audio

It supports multiple service providers through a factory pattern, with
configuration controlled via environment variables.
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import Response
from typing import Optional
from pydantic import BaseModel
import os
from app.services.voice.voice_service import VoiceServiceFactory

router = APIRouter()


# Response models
class STTResponse(BaseModel):
    """
    Speech-to-Text response model.

    Attributes:
        text (str): The transcribed text from the audio input
    """

    text: str


class TTSRequest(BaseModel):
    """
    Text-to-Speech request model.

    Attributes:
        text (str): The text to convert to speech
        voice_id (Optional[str]): Optional voice identifier for the TTS service
    """

    text: str
    voice_id: Optional[str] = None


def get_stt_service():
    """
    Factory function to create a Speech-to-Text service.

    Creates an STT service based on environment variables:
    - STT_PROVIDER: The provider to use (default: "whisper")
    - WHISPER_MODEL: The model to use with Whisper (default: "base")

    Returns:
        An instance of the configured STT service
    """
    provider = os.getenv("STT_PROVIDER", "whisper")
    config = {"model": os.getenv("WHISPER_MODEL", "base")}
    return VoiceServiceFactory.create_stt_service(provider, config)


def get_tts_service():
    """
    Factory function to create a Text-to-Speech service.

    Creates a TTS service based on environment variables:
    - TTS_PROVIDER: The provider to use (default: "elevenlabs")
    - ELEVENLABS_API_KEY: API key for ElevenLabs

    Returns:
        An instance of the configured TTS service
    """
    provider = os.getenv("TTS_PROVIDER", "elevenlabs")
    config = {"api_key": os.getenv("ELEVENLABS_API_KEY")}
    return VoiceServiceFactory.create_tts_service(provider, config)


@router.post("/stt", response_model=STTResponse)
async def speech_to_text(
    audio_file: UploadFile = File(...),
    stt_service=Depends(get_stt_service)
):
    """
    Convert speech to text.

    This endpoint accepts an audio file and transcribes it to text using
    the configured Speech-to-Text service.

    Args:
        audio_file (UploadFile): The audio file to transcribe
        stt_service: The STT service dependency

    Returns:
        STTResponse: The transcribed text

    Raises:
        HTTPException: If the file type is invalid or transcription fails
    """
    # Validate file type
    if not audio_file.content_type.startswith("audio/"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload an audio file."
        )

    try:
        # Process the audio file
        text = stt_service.speech_to_text(audio_file.file)

        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")


@router.post("/tts")
async def text_to_speech(
    request: TTSRequest,
    tts_service=Depends(get_tts_service)
):
    """
    Convert text to speech.

    This endpoint accepts text and converts it to an audio file using
    the configured Text-to-Speech service.

    Args:
        request (TTSRequest): The text to convert and optional voice ID
        tts_service: The TTS service dependency

    Returns:
        Response: Audio file with appropriate content type

    Raises:
        HTTPException: If text-to-speech conversion fails
    """
    try:
        # Generate audio from text
        audio_content = tts_service.text_to_speech(request.text, request.voice_id)

        # Return audio file
        return Response(content=audio_content, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating speech: {str(e)}"
        )

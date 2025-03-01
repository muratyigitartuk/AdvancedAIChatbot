"""
Voice Service Module.

This module provides voice processing services for the application, including:
- Speech-to-Text (STT): Converting audio to text
- Text-to-Speech (TTS): Converting text to audio

It implements an abstract base class and concrete implementations for different
service providers, using a factory pattern for service creation.
"""

import os
import logging
from abc import ABC, abstractmethod
from typing import BinaryIO, Optional, Dict, Tuple
import tempfile
import requests


class VoiceService(ABC):
    """
    Abstract base class for voice services.

    This class defines the interface for voice services, including
    speech-to-text and text-to-speech functionality.
    """

    @abstractmethod
    def speech_to_text(self, audio_file: BinaryIO) -> str:
        """
        Convert speech audio to text.

        Args:
            audio_file (BinaryIO): Binary audio file content

        Returns:
            str: Transcribed text from the audio
        """
        pass

    @abstractmethod
    def transcribe(self, audio_file: BinaryIO) -> str:
        """
        Convert speech audio to text (alias for speech_to_text).

        Args:
            audio_file (BinaryIO): Binary audio file content

        Returns:
            str: Transcribed text from the audio
        """
        pass

    @abstractmethod
    def synthesize(self, text: str, voice_id: Optional[str] = None) -> bytes:
        """
        Convert text to speech audio.

        Args:
            text (str): Text to convert to speech
            voice_id (Optional[str], optional): Voice identifier. Defaults to None.

        Returns:
            bytes: Binary audio data
        """
        pass

    @abstractmethod
    def text_to_speech(self, text: str, voice_id: Optional[str] = None) -> bytes:
        """
        Convert text to speech audio (alias for synthesize).

        Args:
            text (str): Text to convert to speech
            voice_id (Optional[str], optional): Voice identifier. Defaults to None.

        Returns:
            bytes: Binary audio data
        """
        pass


class WhisperSTTService(VoiceService):
    """
    Speech-to-Text service using OpenAI's Whisper model.

    This service uses the Whisper model to transcribe audio to text.
    It requires the 'whisper' package to be installed.

    Attributes:
        model: Loaded Whisper model
    """

    def __init__(self, model_name: str = "base"):
        """
        Initialize the Whisper STT service.

        Args:
            model_name (str, optional): Whisper model name. Defaults to "base".

        Raises:
            ImportError: If the whisper package is not installed
        """
        try:
            import whisper

            self.model = whisper.load_model(model_name)
        except ImportError:
            raise ImportError("Whisper package is not installed. Please install it with 'pip install openai-whisper'.")

    def speech_to_text(self, audio_file: BinaryIO) -> str:
        """
        Convert speech audio to text using Whisper.

        Args:
            audio_file (BinaryIO): Binary audio file content

        Returns:
            str: Transcribed text from the audio
        """
        # Save temporary file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp:
            temp_path = temp.name
            temp.write(audio_file.read())

        try:
            # Transcribe audio
            result = self.model.transcribe(temp_path)
            return result["text"].strip()
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)

    # Alias for compatibility with tests
    transcribe = speech_to_text

    def synthesize(self, text: str, voice_id: Optional[str] = None) -> bytes:
        """
        Not implemented for Whisper service.

        Raises:
            NotImplementedError: This service only supports speech-to-text
        """
        raise NotImplementedError("Whisper service only supports speech-to-text")

    def text_to_speech(self, text: str, voice_id: Optional[str] = None) -> bytes:
        """
        Not implemented for Whisper service.

        Raises:
            NotImplementedError: This service only supports speech-to-text
        """
        return self.synthesize(text, voice_id)


class ElevenLabsTTSService(VoiceService):
    """
    Text-to-Speech service using ElevenLabs API.

    This service uses the ElevenLabs API to convert text to speech.
    It requires an API key from ElevenLabs.

    Attributes:
        api_key (str): ElevenLabs API key
    """

    def __init__(self, api_key: str):
        """
        Initialize the ElevenLabs TTS service.

        Args:
            api_key (str): ElevenLabs API key
        """
        self.api_key = api_key

    def synthesize(self, text: str, voice_id: Optional[str] = None) -> bytes:
        """
        Convert text to speech using ElevenLabs API.

        Args:
            text (str): Text to convert to speech
            voice_id (Optional[str], optional): Voice identifier. Defaults to "21m00Tcm4TlvDq8ikWAM".

        Returns:
            bytes: Binary audio data

        Raises:
            Exception: If the API request fails
        """
        import requests

        # Default voice if not specified
        if not voice_id:
            voice_id = "21m00Tcm4TlvDq8ikWAM"  # Default ElevenLabs voice

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key,
        }

        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
        }

        response = requests.post(url, json=data, headers=headers, timeout=10)

        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"ElevenLabs API error: {response.text}")

    # Alias for backward compatibility
    text_to_speech = synthesize

    def speech_to_text(self, audio_file: BinaryIO) -> str:
        """
        Not implemented for ElevenLabs service.

        Raises:
            NotImplementedError: This service only supports text-to-speech
        """
        raise NotImplementedError("ElevenLabs service only supports text-to-speech")

    def transcribe(self, audio_file: BinaryIO) -> str:
        """
        Not implemented for ElevenLabs service.

        Raises:
            NotImplementedError: This service only supports text-to-speech
        """
        raise NotImplementedError("ElevenLabs service only supports text-to-speech")


class VoiceServiceFactory:
    """
    Factory class for creating voice service instances.

    This class provides static methods to create STT and TTS service instances
    based on the specified provider and configuration.
    """

    @staticmethod
    def create_stt_service(provider: str = "whisper", config: Dict = None) -> VoiceService:
        """
        Create a Speech-to-Text service instance.

        Args:
            provider (str, optional): Service provider name. Defaults to "whisper".
            config (Dict, optional): Configuration for the service. Defaults to None.

        Returns:
            VoiceService: An instance of the specified STT service

        Raises:
            ValueError: If the provider is not supported
        """
        if config is None:
            config = {}

        if provider.lower() == "whisper":
            return WhisperSTTService(model_name=config.get("model", "base"))
        else:
            raise ValueError(f"Unsupported STT provider: {provider}")

    @staticmethod
    def create_tts_service(provider: str = "elevenlabs", config: Dict = None) -> VoiceService:
        """
        Create a Text-to-Speech service instance.

        Args:
            provider (str, optional): Service provider name. Defaults to "elevenlabs".
            config (Dict, optional): Configuration for the service. Defaults to None.

        Returns:
            VoiceService: An instance of the specified TTS service

        Raises:
            ValueError: If the provider is not supported
        """
        if config is None:
            config = {}

        if provider.lower() == "elevenlabs":
            api_key = config.get("api_key")
            if not api_key:
                raise ValueError("ElevenLabs API key is required")
            return ElevenLabsTTSService(api_key=api_key)
        else:
            raise ValueError(f"Unsupported TTS provider: {provider}")

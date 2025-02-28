"""
Voice Service Tests Module

This module contains tests for the voice processing functionality of the advanced
AI chatbot application. It tests various voice-related features including:

1. Speech-to-Text (STT)
   - Converting audio files to text transcriptions
   - Handling invalid file types and formats
   - Error handling for STT service failures

2. Text-to-Speech (TTS)
   - Converting text to audio output
   - Customizing voice parameters
   - Error handling for TTS service failures

These tests use mocked voice services to simulate the behavior of external speech
processing APIs, ensuring that the application correctly handles voice data
conversion and related error cases. The tests validate both successful conversions
and proper error handling for various scenarios.
"""

import io
import pytest
from unittest.mock import patch, MagicMock
from fastapi import status
from app.services.voice.voice_service import VoiceService


@patch("app.api.voice.VoiceServiceFactory")
def test_speech_to_text(mock_factory, client, test_user_token):
    """Test speech to text endpoint."""
    # Create a mock STT service
    mock_stt_service = MagicMock()
    mock_stt_service.speech_to_text.return_value = "This is the transcribed text."

    # Configure the factory to return our mock
    mock_factory.create_stt_service.return_value = mock_stt_service

    # Create a fake audio file
    audio_content = io.BytesIO(b"fake audio data")
    audio_content.name = "test_audio.wav"

    # Test the STT endpoint
    response = client.post(
        "/api/voice/stt",
        files={"audio_file": ("test_audio.wav", audio_content, "audio/wav")},
        headers={"Authorization": f"Bearer {test_user_token}"}
    )

    if response.status_code != status.HTTP_200_OK:
        raise AssertionError("Expected status code 200 OK")

    data = response.json()

    if "text" not in data:
        raise AssertionError("Text field missing in response")

    if data["text"] != "This is the transcribed text.":
        raise AssertionError("Transcribed text does not match expected text")


@patch("app.api.voice.VoiceServiceFactory")
def test_text_to_speech(mock_factory, client, test_user_token):
    """Test text to speech endpoint."""
    # Create a mock TTS service
    mock_tts_service = MagicMock()
    mock_tts_service.text_to_speech.return_value = b"fake audio data"

    # Configure the factory to return our mock
    mock_factory.create_tts_service.return_value = mock_tts_service

    # Test the TTS endpoint
    response = client.post(
        "/api/voice/tts",
        json={"text": "Convert this text to speech", "voice_id": "test_voice"},
        headers={"Authorization": f"Bearer {test_user_token}"}
    )

    if response.status_code != status.HTTP_200_OK:
        raise AssertionError("Expected status code 200 OK")

    if response.content != b"fake audio data":
        raise AssertionError("Audio content does not match expected data")

    if response.headers["content-type"] != "audio/mpeg":
        raise AssertionError("Incorrect content type for audio")


@patch("app.api.voice.VoiceServiceFactory")
def test_stt_invalid_file_type(mock_factory, client, test_user_token):
    """Test STT with invalid file type."""
    # Create a fake text file instead of audio
    text_content = io.BytesIO(b"This is not audio data")
    text_content.name = "test.txt"

    # Test the STT endpoint with invalid file
    response = client.post(
        "/api/voice/stt",
        files={"audio_file": ("test.txt", text_content, "text/plain")},
        headers={"Authorization": f"Bearer {test_user_token}"}
    )

    if response.status_code != status.HTTP_400_BAD_REQUEST:
        raise AssertionError("Expected status code 400 Bad Request")

    data = response.json()

    if "Invalid file type" not in data["detail"]:
        raise AssertionError("Expected 'Invalid file type' in error detail")


@patch("app.api.voice.VoiceServiceFactory")
def test_tts_error_handling(mock_factory, client, test_user_token):
    """Test TTS error handling."""
    # Create a mock TTS service that raises an exception
    mock_tts_service = MagicMock()
    mock_tts_service.text_to_speech.side_effect = Exception("TTS service error")

    # Configure the factory to return our mock
    mock_factory.create_tts_service.return_value = mock_tts_service

    # Test the TTS endpoint with service error
    response = client.post(
        "/api/voice/tts",
        json={"text": "This will fail"},
        headers={"Authorization": f"Bearer {test_user_token}"}
    )

    if response.status_code != status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise AssertionError("Expected status code 500 Internal Server Error")

    data = response.json()

    if "Error generating speech" not in data["detail"]:
        raise AssertionError("Expected 'Error generating speech' in error detail")

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
from unittest.mock import patch, MagicMock
from fastapi import status


@patch("app.api.voice.VoiceServiceFactory")
def test_speech_to_text(mock_factory, client, test_user_token):
    """Test speech to text endpoint."""
    # Create a mock STT service
    mock_stt = MagicMock()
    mock_stt.transcribe.return_value = "This is the transcribed text."

    # Configure the factory to return our mock
    mock_factory.create_stt_service.return_value = mock_stt

    # Create a test audio file
    test_file = io.BytesIO(b"test audio content")

    # Make the request
    response = client.post(
        "/api/voice/stt",
        files={"audio_file": ("test.wav", test_file, "audio/wav")},
        headers={"Authorization": f"Bearer {test_user_token}"},
    )

    # Verify the response
    if response.status_code != status.HTTP_200_OK:
        raise AssertionError("Expected status code 200 OK")

    # Check that our mock was called
    mock_stt.transcribe.assert_called_once()

    # Verify the response data
    data = response.json()
    if "text" not in data:
        raise AssertionError("Expected 'text' in response")

    if data["text"] != "This is the transcribed text.":
        raise AssertionError("Transcribed text does not match expected text")


@patch("app.api.voice.VoiceServiceFactory")
def test_text_to_speech(mock_factory, client, test_user_token):
    """Test text to speech endpoint."""
    # Create a mock TTS service
    mock_tts = MagicMock()
    mock_tts.synthesize.return_value = b"fake audio data"

    # Configure the factory to return our mock
    mock_factory.create_tts_service.return_value = mock_tts

    # Make the request
    response = client.post(
        "/api/voice/tts",
        json={"text": "Convert this text to speech", "voice_id": "en-US-1"},
        headers={"Authorization": f"Bearer {test_user_token}"},
    )

    # Verify the response
    if response.status_code != status.HTTP_200_OK:
        raise AssertionError("Expected status code 200 OK")

    # Check that our mock was called with the right parameters
    mock_tts.synthesize.assert_called_once_with("Convert this text to speech", "en-US-1")

    # Verify the response content
    if response.content != b"fake audio data":
        raise AssertionError("Response content does not match expected audio data")

    if response.headers["content-type"] != "audio/mpeg":
        raise AssertionError("Incorrect content type for audio")


@patch("app.api.voice.VoiceServiceFactory")
def test_stt_invalid_file_type(mock_factory, client, test_user_token):
    """Test STT with invalid file type."""
    # Create a mock STT service
    mock_stt = MagicMock()
    mock_factory_instance = MagicMock()
    mock_factory_instance.get_stt_service.return_value = mock_stt
    mock_factory.return_value = mock_factory_instance

    # Create a test file with invalid type
    test_file = io.BytesIO(b"not an audio file")

    # Make the request with invalid file type
    response = client.post(
        "/api/voice/stt",
        files={"audio_file": ("test.txt", test_file, "text/plain")},
        headers={"Authorization": f"Bearer {test_user_token}"},
    )

    # Verify the response
    if response.status_code != status.HTTP_400_BAD_REQUEST:
        raise AssertionError("Expected status code 400 Bad Request")

    # Our mock should not be called for invalid file
    mock_stt.transcribe.assert_not_called()

    # Verify the error message
    data = response.json()
    if "detail" not in data:
        raise AssertionError("Expected 'detail' in error response")

    if "Invalid file type" not in data["detail"]:
        raise AssertionError("Expected 'Invalid file type' in error detail")


@patch("app.api.voice.VoiceServiceFactory")
def test_tts_error_handling(mock_factory, client, test_user_token):
    """Test error handling in text to speech endpoint."""
    # Create a mock TTS service that raises an exception
    mock_tts = MagicMock()
    mock_tts.synthesize.side_effect = Exception("TTS service error")

    # Configure the factory to return our mock
    mock_factory.create_tts_service.return_value = mock_tts

    # Make the request
    response = client.post(
        "/api/voice/tts",
        json={"text": "Convert this text to speech"},
        headers={"Authorization": f"Bearer {test_user_token}"},
    )

    # Verify we get an error response
    if response.status_code != status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise AssertionError("Expected status code 500 Internal Server Error")

    # Verify the error message
    data = response.json()
    if "detail" not in data:
        raise AssertionError("Expected 'detail' in error response")

    if "Error generating speech" not in data["detail"]:
        raise AssertionError("Error message does not contain expected text")

import httpx
import base64
from app.core.config import settings
import logging
import os
import wave
import struct

logger = logging.getLogger(__name__)


class TTSService:
    """Service for Text-to-Speech using Cartesia AI"""

    def __init__(self):
        """Initialize Cartesia TTS client"""
        self.api_key = settings.CARTESIA_API_KEY
        self.model_id = settings.CARTESIA_MODEL_ID
        self.voice_id = settings.CARTESIA_VOICE_ID
        self.base_url = "https://api.cartesia.ai"
        self.api_version = "2024-06-10"

    async def generate_speech(
        self,
        story_text: str,
        output_path: str,
        voice_id: str = None,
        speed: float = 1.0,
        emotion: str = "happy"
    ) -> str:
        """
        Generate speech audio from story text using Cartesia TTS

        Args:
            story_text: The story text to convert to speech
            output_path: Path where to save the audio file
            voice_id: Optional voice ID override
            speed: Speech speed (0.6-1.5)
            emotion: Emotion for the voice (neutral, happy, sad, angry, etc.)

        Returns:
            Path to the generated audio file
        """
        try:
            logger.info(f"Generating speech for text ({len(story_text)} characters) using Cartesia")

            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Use provided voice or default
            voice = voice_id or self.voice_id

            # Prepare request payload
            payload = {
                "model_id": self.model_id,
                "transcript": story_text,
                "voice": {
                    "mode": "id",
                    "id": voice
                },
                "output_format": {
                    "container": "raw",
                    "encoding": "pcm_s16le",
                    "sample_rate": 44100
                },
                "language": "en"
            }

            # Add generation config for Sonic-3 models
            if "sonic" in self.model_id.lower():
                payload["generation_config"] = {
                    "speed": speed,
                    "emotion": emotion
                }

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Cartesia-Version": self.api_version,
                "Content-Type": "application/json"
            }

            # Make API request
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/tts/bytes",
                    json=payload,
                    headers=headers
                )

                if response.status_code != 200:
                    error_msg = f"Cartesia API error: {response.status_code} - {response.text}"
                    logger.error(error_msg)
                    raise Exception(error_msg)

                # Get audio data
                audio_data = response.content

                # Convert raw PCM to WAV format
                self._save_as_wav(audio_data, output_path, sample_rate=44100, channels=1)

                logger.info(f"Speech generated successfully: {output_path}")
                return output_path

        except Exception as e:
            logger.error(f"Error generating speech: {str(e)}")
            raise Exception(f"Failed to generate speech: {str(e)}")

    def _save_as_wav(self, pcm_data: bytes, output_path: str, sample_rate: int = 44100, channels: int = 1):
        """
        Save raw PCM data as WAV file

        Args:
            pcm_data: Raw PCM audio data
            output_path: Output file path
            sample_rate: Sample rate in Hz
            channels: Number of audio channels
        """
        with wave.open(output_path, 'wb') as wav_file:
            wav_file.setnchannels(channels)
            wav_file.setsampwidth(2)  # 16-bit = 2 bytes
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(pcm_data)

    def get_available_voices(self) -> dict:
        """Get list of available child-friendly Cartesia voices"""
        # Cartesia voice IDs suitable for children's stories
        child_friendly_voices = {
            "694f9389-aac1-45b6-b726-9d9369183238": "Friendly Female Voice (Default)",
            "a0e99841-438c-4a64-b679-ae501e7d6091": "Expressive Female Voice",
            "79a125e8-cd45-4c13-8a67-188112f4dd22": "Calm Male Voice",
            "2ee87190-8f84-4925-97da-e52547f9462c": "Energetic Child Voice",
        }
        return child_friendly_voices

    async def get_emotion_for_story(self, story_text: str) -> str:
        """
        Analyze story text to determine appropriate emotion

        Args:
            story_text: The story text to analyze

        Returns:
            Emotion string for voice generation
        """
        story_lower = story_text.lower()

        # Simple keyword-based emotion detection
        if any(word in story_lower for word in ["happy", "joy", "laugh", "fun", "play"]):
            return "happy"
        elif any(word in story_lower for word in ["sad", "cry", "lost"]):
            return "sad"
        elif any(word in story_lower for word in ["exciting", "adventure", "brave"]):
            return "excited"
        elif any(word in story_lower for word in ["calm", "peaceful", "gentle", "quiet"]):
            return "calm"
        elif any(word in story_lower for word in ["scary", "afraid", "worried"]):
            return "fearful"
        else:
            return "happy"  # Default emotion for children's stories

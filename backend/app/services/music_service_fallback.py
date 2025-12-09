"""
Fallback Music Service - creates silent audio when music generation fails
"""

import os
import logging
import wave
import struct
from app.core.config import settings

logger = logging.getLogger(__name__)


class MusicServiceFallback:
    """Fallback music service that creates silent audio"""

    def __init__(self):
        """Initialize fallback music service"""
        logger.warning("Using FALLBACK MUSIC service (silent audio). Configure Gemini API for real music.")

    async def generate_music(
        self,
        duration: int,
        mood: str = "calm",
        output_path: str = None
    ) -> str:
        """
        Generate silent audio as fallback when music generation fails

        Args:
            duration: Duration in seconds
            mood: Mood/style (ignored in fallback)
            output_path: Where to save the audio file

        Returns:
            Path to the generated audio file
        """
        try:
            logger.info(f"Generating silent audio ({duration}s) as music fallback")

            if output_path is None:
                output_path = os.path.join(settings.STORIES_DIR, f"music_{duration}s_silent.wav")

            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Create silent WAV file
            sample_rate = 44100  # Standard sample rate
            num_samples = int(duration * sample_rate)

            with wave.open(output_path, 'wb') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)

                # Write silent samples (all zeros)
                silent_data = struct.pack('<' + 'h' * num_samples, *([0] * num_samples))
                wav_file.writeframes(silent_data)

            logger.info(f"Silent audio created: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error creating silent audio: {str(e)}")
            raise Exception(f"Failed to create fallback audio: {str(e)}")

    def get_story_mood(self, story_text: str) -> str:
        """
        Analyze story text to determine appropriate mood

        Args:
            story_text: The story text to analyze

        Returns:
            Mood string
        """
        story_lower = story_text.lower()

        if any(word in story_lower for word in ["sleep", "night", "bedtime", "dream", "quiet"]):
            return "bedtime"
        elif any(word in story_lower for word in ["adventure", "brave", "quest", "journey", "explore"]):
            return "adventure"
        elif any(word in story_lower for word in ["happy", "laugh", "joy", "fun", "play"]):
            return "happy"
        elif any(word in story_lower for word in ["magic", "wonder", "fairy", "enchant", "sparkle"]):
            return "dreamy"
        elif any(word in story_lower for word in ["silly", "funny", "giggle", "bounce"]):
            return "playful"
        else:
            return "calm"

    async def get_royalty_free_music(self, duration: int, mood: str = "calm") -> str:
        """
        Fallback that returns silent audio

        Args:
            duration: Duration needed
            mood: Mood/style

        Returns:
            Path to silent audio file
        """
        return await self.generate_music(duration, mood)

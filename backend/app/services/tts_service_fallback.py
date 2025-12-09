"""
Fallback TTS Service for development/testing without Azure credentials
Uses gTTS (Google Text-to-Speech) as a free alternative
"""

import os
import logging
from gtts import gTTS
from app.core.config import settings

logger = logging.getLogger(__name__)


class TTSServiceFallback:
    """Fallback TTS service using Google Text-to-Speech (free)"""

    def __init__(self):
        """Initialize fallback TTS service"""
        logger.warning("Using FALLBACK TTS service (gTTS). Install Azure credentials for production quality.")

    async def generate_speech(
        self,
        story_text: str,
        output_path: str,
        use_ssml: bool = False  # Not used in gTTS but kept for interface compatibility
    ) -> str:
        """
        Generate speech from text using gTTS (free Google TTS)

        Args:
            story_text: Text to convert to speech (matches Azure TTS interface)
            output_path: Where to save the audio file
            use_ssml: Ignored in gTTS (kept for interface compatibility)

        Returns:
            Path to the generated audio file
        """
        try:
            logger.info(f"Generating speech with gTTS ({len(story_text)} characters)")

            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Generate speech using gTTS
            tts = gTTS(text=story_text, lang='en', slow=False)
            tts.save(output_path)

            logger.info(f"Speech generated and saved: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error generating speech with gTTS: {str(e)}")
            raise Exception(f"Failed to generate speech: {str(e)}")

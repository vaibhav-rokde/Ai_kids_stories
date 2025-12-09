import httpx
from app.core.config import settings
import logging
import os
import asyncio

logger = logging.getLogger(__name__)


class MusicService:
    """Service for generating background music using Mubert API"""

    def __init__(self):
        """Initialize Mubert API client"""
        self.api_key = settings.MUBERT_API_KEY
        self.license = settings.MUBERT_LICENSE
        self.base_url = "https://api-b2b.mubert.com/v2/RecordTrack"

    async def generate_music(
        self,
        duration: int,
        mood: str = "calm",
        output_path: str = None
    ) -> str:
        """
        Generate background music using Mubert API

        Args:
            duration: Duration in seconds
            mood: Mood/style of music (calm, happy, dreamy, playful, etc.)
            output_path: Where to save the music file

        Returns:
            Path to the generated music file
        """
        try:
            logger.info(f"Generating {duration}s background music with mood: {mood}")

            # Map story moods to Mubert tags
            mood_tags = {
                "calm": ["calm", "peaceful", "ambient", "soft"],
                "happy": ["happy", "upbeat", "cheerful", "bright"],
                "dreamy": ["dreamy", "ethereal", "magical", "floating"],
                "playful": ["playful", "fun", "energetic", "bouncy"],
                "adventure": ["adventure", "exciting", "heroic", "epic"],
                "bedtime": ["lullaby", "gentle", "soothing", "sleepy"]
            }

            tags = mood_tags.get(mood, mood_tags["calm"])

            # Prepare request payload
            payload = {
                "method": "RecordTrack",
                "params": {
                    "license": self.license,
                    "format": "mp3",
                    "duration": duration,
                    "tags": ",".join(tags),
                    "mode": "loop"  # Loop for consistent background
                }
            }

            # Make API request
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    self.base_url,
                    json=payload,
                    headers={
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    }
                )

                if response.status_code != 200:
                    raise Exception(f"Mubert API error: {response.status_code} - {response.text}")

                result = response.json()

                if result.get("status") != 1:
                    raise Exception(f"Mubert generation failed: {result.get('error', 'Unknown error')}")

                download_url = result["data"]["tasks"][0]["download_link"]

                # Download the generated music
                logger.info(f"Downloading music from: {download_url}")

                music_response = await client.get(download_url)
                if music_response.status_code != 200:
                    raise Exception(f"Failed to download music: {music_response.status_code}")

                # Save to file
                if output_path is None:
                    output_path = os.path.join(settings.STORIES_DIR, f"music_{duration}s_{mood}.mp3")

                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                with open(output_path, "wb") as f:
                    f.write(music_response.content)

                logger.info(f"Music generated and saved: {output_path}")
                return output_path

        except Exception as e:
            logger.error(f"Error generating music: {str(e)}")
            raise Exception(f"Failed to generate music: {str(e)}")

    def get_story_mood(self, story_text: str) -> str:
        """
        Analyze story text to determine appropriate mood for music

        Args:
            story_text: The story text to analyze

        Returns:
            Mood string for music generation
        """
        # Simple keyword-based mood detection
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
            return "calm"  # Default mood

    async def get_royalty_free_music(self, duration: int, mood: str = "calm") -> str:
        """
        Fallback method using royalty-free music library
        (In case Mubert API is not available)

        Args:
            duration: Duration needed
            mood: Mood/style

        Returns:
            Path to music file from library
        """
        # This would return a path to pre-selected royalty-free music
        # For now, we'll just return a placeholder
        logger.warning("Using fallback royalty-free music (Mubert not available)")

        # In production, this would select from a curated library
        music_library_path = os.path.join(settings.STORIES_DIR, "music_library")
        os.makedirs(music_library_path, exist_ok=True)

        return os.path.join(music_library_path, f"default_{mood}.mp3")

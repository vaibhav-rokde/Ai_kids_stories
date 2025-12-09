import asyncio
from google import genai
from google.genai import types
from app.core.config import settings
import logging
import os
import wave
import struct

logger = logging.getLogger(__name__)


class MusicService:
    """Service for generating background music using Google Gemini Lyria RealTime"""

    def __init__(self):
        """Initialize Gemini Lyria client"""
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
            http_options={'api_version': 'v1alpha'}
        )
        self.model = 'models/lyria-realtime-exp'

    async def generate_music(
        self,
        duration: int,
        mood: str = "calm",
        output_path: str = None
    ) -> str:
        """
        Generate background music using Google Gemini Lyria RealTime

        Args:
            duration: Duration in seconds
            mood: Mood/style of music (calm, happy, dreamy, playful, etc.)
            output_path: Where to save the music file

        Returns:
            Path to the generated music file
        """
        try:
            logger.info(f"Generating {duration}s background music with mood: {mood}")

            # Map story moods to music generation prompts
            mood_prompts = {
                "calm": {
                    "primary": "peaceful ambient background music, soft piano and strings, gentle flowing melodies",
                    "weight": 1.0,
                    "bpm": 70,
                    "temperature": 0.8
                },
                "happy": {
                    "primary": "cheerful upbeat background music, bright acoustic guitar and light percussion, joyful melodies",
                    "weight": 1.0,
                    "bpm": 120,
                    "temperature": 0.9
                },
                "dreamy": {
                    "primary": "ethereal magical background music, soft synths and bells, dreamy floating melodies",
                    "weight": 1.0,
                    "bpm": 60,
                    "temperature": 1.0
                },
                "playful": {
                    "primary": "playful bouncy background music, xylophone and light drums, fun energetic melodies",
                    "weight": 1.0,
                    "bpm": 130,
                    "temperature": 1.1
                },
                "adventure": {
                    "primary": "adventurous epic background music, orchestral strings and brass, heroic uplifting melodies",
                    "weight": 1.0,
                    "bpm": 110,
                    "temperature": 0.9
                },
                "bedtime": {
                    "primary": "soothing lullaby background music, soft music box and gentle humming, sleepy calming melodies",
                    "weight": 1.0,
                    "bpm": 50,
                    "temperature": 0.7
                }
            }

            prompt_config = mood_prompts.get(mood, mood_prompts["calm"])

            # Set default output path
            if output_path is None:
                output_path = os.path.join(settings.STORIES_DIR, f"music_{duration}s_{mood}.wav")

            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Generate music using Lyria RealTime
            audio_chunks = []

            async def receive_audio(session, target_duration):
                """Receive and collect audio chunks until target duration is reached"""
                try:
                    start_time = asyncio.get_event_loop().time()

                    async for message in session.receive():
                        if hasattr(message, 'server_content') and message.server_content:
                            if hasattr(message.server_content, 'audio_chunks'):
                                for audio_chunk in message.server_content.audio_chunks:
                                    if hasattr(audio_chunk, 'data'):
                                        audio_chunks.append(audio_chunk.data)
                                        logger.debug(f"Received audio chunk: {len(audio_chunk.data)} bytes")

                        # Check if we've reached target duration (approximate)
                        elapsed = asyncio.get_event_loop().time() - start_time
                        if elapsed >= target_duration:
                            logger.info(f"Target duration reached: {elapsed:.2f}s")
                            break

                except Exception as e:
                    logger.error(f"Error receiving audio: {str(e)}")

            # Connect to Lyria RealTime and generate music
            async with (
                self.client.aio.live.music.connect(model=self.model) as session,
                asyncio.TaskGroup() as tg,
            ):
                # Set up task to receive audio chunks
                receive_task = tg.create_task(receive_audio(session, duration))

                # Configure music generation
                await session.set_weighted_prompts(
                    prompts=[
                        types.WeightedPrompt(
                            text=prompt_config["primary"],
                            weight=prompt_config["weight"]
                        ),
                    ]
                )

                await session.set_music_generation_config(
                    config=types.LiveMusicGenerationConfig(
                        bpm=prompt_config["bpm"],
                        temperature=prompt_config["temperature"]
                    )
                )

                # Start streaming music
                await session.play()

                # Wait for audio collection to complete
                logger.info("Collecting audio chunks...")
                await receive_task

            # Save collected audio chunks to WAV file
            if not audio_chunks:
                raise Exception("No audio data received from Lyria")

            logger.info(f"Collected {len(audio_chunks)} audio chunks, saving to {output_path}")

            # Combine all audio chunks
            combined_audio = b''.join(audio_chunks)

            # Save as WAV file (Lyria outputs PCM audio at 24kHz, 16-bit, mono)
            sample_rate = 24000  # Lyria's output sample rate
            sample_width = 2     # 16-bit audio = 2 bytes
            channels = 1         # Mono

            with wave.open(output_path, 'wb') as wav_file:
                wav_file.setnchannels(channels)
                wav_file.setsampwidth(sample_width)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(combined_audio)

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
        (In case Lyria is not available)

        Args:
            duration: Duration needed
            mood: Mood/style

        Returns:
            Path to music file from library
        """
        # This would return a path to pre-selected royalty-free music
        # For now, we'll just return a placeholder
        logger.warning("Using fallback royalty-free music (Lyria not available)")

        # In production, this would select from a curated library
        music_library_path = os.path.join(settings.STORIES_DIR, "music_library")
        os.makedirs(music_library_path, exist_ok=True)

        return os.path.join(music_library_path, f"default_{mood}.mp3")

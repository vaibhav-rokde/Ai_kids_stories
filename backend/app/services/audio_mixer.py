from pydub import AudioSegment
from pydub.effects import normalize
import logging
import os

logger = logging.getLogger(__name__)


class AudioMixerService:
    """Service for mixing narration and background music"""

    def __init__(self):
        """Initialize audio mixer"""
        pass

    async def mix_audio(
        self,
        narration_path: str,
        music_path: str,
        output_path: str,
        music_volume_reduction_db: int = 20
    ) -> tuple[str, float]:
        """
        Mix narration with background music

        Args:
            narration_path: Path to narration audio file
            music_path: Path to background music file
            output_path: Path where to save final mixed audio
            music_volume_reduction_db: How much to reduce music volume (dB)

        Returns:
            Tuple of (output_path, duration_seconds)
        """
        try:
            logger.info("Mixing narration with background music")

            # Load audio files
            narration = AudioSegment.from_file(narration_path)
            music = AudioSegment.from_file(music_path)

            # Get narration duration
            narration_duration_ms = len(narration)
            duration_seconds = narration_duration_ms / 1000.0

            logger.info(f"Narration duration: {duration_seconds:.2f} seconds")

            # Adjust music length to match narration
            if len(music) < narration_duration_ms:
                # Loop music if it's shorter than narration
                loops_needed = (narration_duration_ms // len(music)) + 1
                music = music * loops_needed

            # Trim music to match narration length
            music = music[:narration_duration_ms]

            # Reduce music volume to keep it in background
            music = music - music_volume_reduction_db

            # Apply fade in/out to music for smooth transitions
            music = music.fade_in(2000).fade_out(3000)  # 2s fade in, 3s fade out

            # Overlay music under narration
            mixed = narration.overlay(music)

            # Normalize audio to prevent clipping
            mixed = normalize(mixed)

            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Export final mixed audio
            mixed.export(
                output_path,
                format="mp3",
                bitrate="128k",
                parameters=["-q:a", "2"]  # High quality
            )

            logger.info(f"Audio mixed successfully: {output_path}")
            return output_path, duration_seconds

        except Exception as e:
            logger.error(f"Error mixing audio: {str(e)}")
            raise Exception(f"Failed to mix audio: {str(e)}")

    async def add_sound_effects(
        self,
        base_audio_path: str,
        sound_effects: list[dict],
        output_path: str
    ) -> str:
        """
        Add sound effects to audio at specific timestamps

        Args:
            base_audio_path: Path to base audio file
            sound_effects: List of dicts with 'path' and 'timestamp_ms' keys
            output_path: Path where to save audio with effects

        Returns:
            Path to output file
        """
        try:
            logger.info(f"Adding {len(sound_effects)} sound effects")

            # Load base audio
            audio = AudioSegment.from_file(base_audio_path)

            # Add each sound effect
            for effect in sound_effects:
                effect_audio = AudioSegment.from_file(effect['path'])
                # Reduce effect volume
                effect_audio = effect_audio - 10  # 10dB quieter
                # Overlay at specified timestamp
                audio = audio.overlay(effect_audio, position=effect['timestamp_ms'])

            # Normalize
            audio = normalize(audio)

            # Export
            audio.export(output_path, format="mp3", bitrate="128k")

            logger.info(f"Sound effects added: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error adding sound effects: {str(e)}")
            raise Exception(f"Failed to add sound effects: {str(e)}")

    def get_audio_duration(self, audio_path: str) -> float:
        """
        Get duration of audio file in seconds

        Args:
            audio_path: Path to audio file

        Returns:
            Duration in seconds
        """
        try:
            audio = AudioSegment.from_file(audio_path)
            return len(audio) / 1000.0
        except Exception as e:
            logger.error(f"Error getting audio duration: {str(e)}")
            return 0.0

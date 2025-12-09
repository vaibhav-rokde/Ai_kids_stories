import azure.cognitiveservices.speech as speechsdk
from app.core.config import settings
import logging
import os

logger = logging.getLogger(__name__)


class TTSService:
    """Service for Text-to-Speech using Azure Cognitive Services"""

    def __init__(self):
        """Initialize Azure Speech SDK"""
        self.speech_config = speechsdk.SpeechConfig(
            subscription=settings.AZURE_SPEECH_KEY,
            region=settings.AZURE_SPEECH_REGION
        )
        self.speech_config.speech_synthesis_voice_name = settings.AZURE_VOICE_NAME

    def create_ssml(self, text: str, voice_name: str = None) -> str:
        """
        Create SSML (Speech Synthesis Markup Language) for enhanced narration

        Args:
            text: Story text to convert
            voice_name: Optional voice name override

        Returns:
            SSML formatted string
        """
        voice = voice_name or settings.AZURE_VOICE_NAME

        # Add natural pauses and emphasis for better storytelling
        ssml = f"""<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
    <voice name='{voice}'>
        <prosody rate='0.95' pitch='medium'>
            {text}
        </prosody>
    </voice>
</speak>"""
        return ssml

    async def generate_speech(
        self,
        story_text: str,
        output_path: str,
        use_ssml: bool = True
    ) -> str:
        """
        Generate speech audio from story text

        Args:
            story_text: The story text to convert to speech
            output_path: Path where to save the MP3 file
            use_ssml: Whether to use SSML for enhanced narration

        Returns:
            Path to the generated audio file
        """
        try:
            logger.info(f"Generating speech for text ({len(story_text)} characters)")

            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Configure audio output
            audio_config = speechsdk.audio.AudioOutputConfig(filename=output_path)

            # Create synthesizer
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.speech_config,
                audio_config=audio_config
            )

            # Generate speech
            if use_ssml:
                ssml_text = self.create_ssml(story_text)
                result = synthesizer.speak_ssml_async(ssml_text).get()
            else:
                result = synthesizer.speak_text_async(story_text).get()

            # Check result
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                logger.info(f"Speech generated successfully: {output_path}")
                return output_path
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                logger.error(f"Speech synthesis canceled: {cancellation.reason}")
                if cancellation.reason == speechsdk.CancellationReason.Error:
                    logger.error(f"Error details: {cancellation.error_details}")
                raise Exception(f"Speech synthesis failed: {cancellation.error_details}")
            else:
                raise Exception(f"Unexpected result: {result.reason}")

        except Exception as e:
            logger.error(f"Error generating speech: {str(e)}")
            raise Exception(f"Failed to generate speech: {str(e)}")

    def get_available_voices(self) -> list:
        """Get list of available child-friendly voices"""
        # Azure voices suitable for children's stories
        child_friendly_voices = [
            "en-US-JennyNeural",  # Friendly female voice
            "en-US-AriaNeural",   # Expressive female voice
            "en-US-GuyNeural",    # Male voice
            "en-GB-SoniaNeural",  # British female voice
            "en-AU-NatashaNeural" # Australian female voice
        ]
        return child_friendly_voices

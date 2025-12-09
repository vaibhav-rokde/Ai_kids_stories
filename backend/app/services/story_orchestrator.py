from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from app.services.story_generator import StoryGeneratorService
from app.services.tts_service import TTSService
try:
    from app.services.tts_service_fallback import TTSServiceFallback
    FALLBACK_TTS_AVAILABLE = True
except ImportError:
    FALLBACK_TTS_AVAILABLE = False
from app.services.music_service import MusicService
try:
    from app.services.music_service_fallback import MusicServiceFallback
    FALLBACK_MUSIC_AVAILABLE = True
except ImportError:
    FALLBACK_MUSIC_AVAILABLE = False
from app.services.audio_mixer import AudioMixerService
from app.core.config import settings
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)


# Define the state structure
class StoryState(TypedDict):
    """State for story generation workflow"""
    # Input
    story_id: int
    theme: str
    character_name: str | None
    age_group: str

    # Generated content
    story_text: str | None
    story_title: str | None
    word_count: int | None

    # File paths
    narration_path: str | None
    music_path: str | None
    final_audio_path: str | None

    # Metadata
    duration_seconds: float | None
    mood: str | None

    # Status
    current_step: str
    error: str | None


class StoryOrchestrator:
    """
    Orchestrates the entire story generation workflow using LangGraph
    Story → Speech → Music → Final Mix
    """

    def __init__(self):
        """Initialize services"""
        self.story_generator = StoryGeneratorService()

        # Choose TTS service based on configuration or fallback
        if getattr(settings, 'USE_FALLBACK_TTS', False) and FALLBACK_TTS_AVAILABLE:
            logger.warning("Using fallback TTS service (gTTS)")
            self.tts_service = TTSServiceFallback()
            self.use_azure_tts = False
        else:
            self.tts_service = TTSService()
            self.use_azure_tts = True

        self.music_service = MusicService()
        self.audio_mixer = AudioMixerService()
        self.workflow = self._build_workflow()

    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""

        # Create the graph
        workflow = StateGraph(StoryState)

        # Add nodes for each step
        workflow.add_node("generate_story", self.generate_story_node)
        workflow.add_node("generate_speech", self.generate_speech_node)
        workflow.add_node("generate_music", self.generate_music_node)
        workflow.add_node("mix_audio", self.mix_audio_node)

        # Define the flow
        workflow.set_entry_point("generate_story")
        workflow.add_edge("generate_story", "generate_speech")
        workflow.add_edge("generate_speech", "generate_music")
        workflow.add_edge("generate_music", "mix_audio")
        workflow.add_edge("mix_audio", END)

        return workflow.compile()

    async def generate_story_node(self, state: StoryState) -> StoryState:
        """Node: Generate story text"""
        try:
            logger.info(f"[Story {state['story_id']}] Generating story text...")
            state["current_step"] = "generating_text"

            result = await self.story_generator.generate_story(
                theme=state["theme"],
                character_name=state["character_name"],
                age_group=state["age_group"]
            )

            state["story_text"] = result["story_text"]
            state["story_title"] = result["story_title"]
            state["word_count"] = result["word_count"]

            logger.info(f"[Story {state['story_id']}] Story generated: {result['story_title']}")
            return state

        except Exception as e:
            logger.error(f"[Story {state['story_id']}] Error generating story: {str(e)}")
            state["error"] = str(e)
            return state

    async def generate_speech_node(self, state: StoryState) -> StoryState:
        """Node: Generate speech narration"""
        try:
            if state.get("error"):
                return state

            logger.info(f"[Story {state['story_id']}] Generating speech...")
            state["current_step"] = "generating_audio"

            # Create unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            narration_filename = f"story_{state['story_id']}_{timestamp}_narration.mp3"
            narration_path = os.path.join(settings.STORIES_DIR, narration_filename)

            # Generate speech
            await self.tts_service.generate_speech(
                story_text=state["story_text"],
                output_path=narration_path,
                use_ssml=True
            )

            state["narration_path"] = narration_path

            logger.info(f"[Story {state['story_id']}] Speech generated")
            return state

        except Exception as e:
            logger.error(f"[Story {state['story_id']}] Error generating speech: {str(e)}")
            state["error"] = str(e)
            return state

    async def generate_music_node(self, state: StoryState) -> StoryState:
        """Node: Generate background music"""
        try:
            if state.get("error"):
                return state

            logger.info(f"[Story {state['story_id']}] Generating background music...")
            state["current_step"] = "adding_music"

            # Get narration duration
            narration_duration = self.audio_mixer.get_audio_duration(state["narration_path"])

            # Determine mood from story
            mood = self.music_service.get_story_mood(state["story_text"])
            state["mood"] = mood

            # Create unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            music_filename = f"story_{state['story_id']}_{timestamp}_music.wav"
            music_path = os.path.join(settings.STORIES_DIR, music_filename)

            # Try to generate music, fall back to silent audio if it fails
            try:
                await self.music_service.generate_music(
                    duration=int(narration_duration) + 5,  # Add 5s buffer
                    mood=mood,
                    output_path=music_path
                )
            except Exception as music_error:
                logger.warning(f"[Story {state['story_id']}] Music generation failed: {str(music_error)}")
                logger.info(f"[Story {state['story_id']}] Using silent audio as fallback")

                # Use fallback music service (silent audio)
                if FALLBACK_MUSIC_AVAILABLE:
                    fallback_music = MusicServiceFallback()
                    await fallback_music.generate_music(
                        duration=int(narration_duration) + 5,
                        mood=mood,
                        output_path=music_path
                    )
                else:
                    raise music_error

            state["music_path"] = music_path

            logger.info(f"[Story {state['story_id']}] Music generated with mood: {mood}")
            return state

        except Exception as e:
            logger.error(f"[Story {state['story_id']}] Error generating music: {str(e)}")
            # Continue without music if it fails
            logger.warning(f"[Story {state['story_id']}] Continuing without background music")
            state["music_path"] = None
            return state

    async def mix_audio_node(self, state: StoryState) -> StoryState:
        """Node: Mix narration and music into final audio"""
        try:
            if state.get("error"):
                return state

            logger.info(f"[Story {state['story_id']}] Mixing final audio...")
            state["current_step"] = "finalizing"

            # Create unique filename for final audio
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            final_filename = f"story_{state['story_id']}_{timestamp}_final.mp3"
            final_path = os.path.join(settings.STORIES_DIR, final_filename)

            if state.get("music_path"):
                # Mix narration with music
                final_audio_path, duration = await self.audio_mixer.mix_audio(
                    narration_path=state["narration_path"],
                    music_path=state["music_path"],
                    output_path=final_path,
                    music_volume_reduction_db=20
                )
            else:
                # Use narration only if music generation failed
                logger.warning(f"[Story {state['story_id']}] No music available, using narration only")
                final_audio_path = state["narration_path"]
                duration = self.audio_mixer.get_audio_duration(final_audio_path)

            state["final_audio_path"] = final_audio_path
            state["duration_seconds"] = duration
            state["current_step"] = "completed"

            logger.info(f"[Story {state['story_id']}] Final audio created: {final_audio_path}")
            return state

        except Exception as e:
            logger.error(f"[Story {state['story_id']}] Error mixing audio: {str(e)}")
            state["error"] = str(e)
            return state

    async def generate_complete_story(
        self,
        story_id: int,
        theme: str,
        character_name: str | None,
        age_group: str
    ) -> StoryState:
        """
        Execute the complete story generation workflow

        Args:
            story_id: Database ID of the story
            theme: Story theme
            character_name: Optional character name
            age_group: Target age group

        Returns:
            Final state with all generated content
        """
        try:
            logger.info(f"[Story {story_id}] Starting story generation workflow")

            # Initialize state
            initial_state: StoryState = {
                "story_id": story_id,
                "theme": theme,
                "character_name": character_name,
                "age_group": age_group,
                "story_text": None,
                "story_title": None,
                "word_count": None,
                "narration_path": None,
                "music_path": None,
                "final_audio_path": None,
                "duration_seconds": None,
                "mood": None,
                "current_step": "starting",
                "error": None
            }

            # Execute workflow
            final_state = await self.workflow.ainvoke(initial_state)

            logger.info(f"[Story {story_id}] Workflow completed. Status: {final_state['current_step']}")
            return final_state

        except Exception as e:
            logger.error(f"[Story {story_id}] Workflow failed: {str(e)}")
            raise Exception(f"Story generation workflow failed: {str(e)}")

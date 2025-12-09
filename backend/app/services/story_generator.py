import google.generativeai as genai
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class StoryGeneratorService:
    """Service for generating children's stories using Gemini AI"""

    def __init__(self):
        """Initialize Gemini API"""
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)

    def create_story_prompt(
        self,
        theme: str,
        character_name: str | None,
        age_group: str
    ) -> str:
        """Create optimized prompt for story generation based on research"""

        # Age-specific adjustments
        age_config = {
            "3-5": {
                "word_count": "400-450",
                "complexity": "simple sentences with repetition",
                "vocabulary": "basic vocabulary for toddlers"
            },
            "5-7": {
                "word_count": "450-500",
                "complexity": "short, engaging sentences",
                "vocabulary": "vocabulary appropriate for early readers"
            },
            "7-10": {
                "word_count": "500-600",
                "complexity": "varied sentence structure with dialogue",
                "vocabulary": "elementary-level vocabulary"
            }
        }

        config = age_config.get(age_group, age_config["5-7"])
        character_clause = f"The main character is named {character_name}." if character_name else ""

        prompt = f"""You are an award-winning children's book author specializing in stories for ages {age_group}.
Write a {config['word_count']} word story about: {theme}

{character_clause}

Requirements:
- Target age: {age_group} years old
- Length: {config['word_count']} words (approximately 3-4 minutes when read aloud)
- Use {config['complexity']}
- Vocabulary: {config['vocabulary']}
- Include dialogue and descriptive language
- Create a clear beginning, middle, and end
- Include sensory details (sounds, sights, feelings)
- End with a comforting, positive conclusion
- Add a moral or gentle lesson naturally woven into the story

Style Guidelines:
- Use repetition for rhythmic quality
- Include onomatopoeia where appropriate (whoosh, splash, rustle)
- Keep the tone warm, gentle, and engaging
- Make it suitable for reading aloud as bedtime stories

Format:
Provide ONLY the story text, without any title, metadata, or formatting markers.
Start directly with the story narrative.
"""
        return prompt

    async def generate_story(
        self,
        theme: str,
        character_name: str | None = None,
        age_group: str = "5-7"
    ) -> dict:
        """
        Generate a children's story using Gemini API

        Args:
            theme: Story theme or idea
            character_name: Optional main character name
            age_group: Target age group (3-5, 5-7, 7-10)

        Returns:
            dict with story_text, title, and word_count
        """
        try:
            logger.info(f"Generating story with theme: {theme}, age_group: {age_group}")

            # Create optimized prompt
            prompt = self.create_story_prompt(theme, character_name, age_group)

            # Generate story
            response = self.model.generate_content(prompt)
            story_text = response.text.strip()

            # Generate title separately
            title_prompt = f"Create a short, catchy title (max 10 words) for this children's story:\n\n{story_text[:500]}...\n\nProvide ONLY the title, nothing else."
            title_response = self.model.generate_content(title_prompt)
            story_title = title_response.text.strip().replace('"', '').replace("'", "")

            # Calculate word count
            word_count = len(story_text.split())

            logger.info(f"Story generated successfully. Word count: {word_count}, Title: {story_title}")

            return {
                "story_text": story_text,
                "story_title": story_title,
                "word_count": word_count
            }

        except Exception as e:
            logger.error(f"Error generating story: {str(e)}")
            raise Exception(f"Failed to generate story: {str(e)}")

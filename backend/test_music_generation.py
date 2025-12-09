#!/usr/bin/env python3
"""
Test script for Music Generation using Google Lyria
"""
import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from app.services.music_service import MusicService
from app.core.config import settings


async def test_music_generation():
    """Test music generation with Google Lyria"""

    print("=" * 60)
    print("Testing Music Generation with Google Lyria")
    print("=" * 60)

    # Check Gemini API key
    if not settings.GEMINI_API_KEY:
        print("\n❌ ERROR: GEMINI_API_KEY not found in environment")
        print("Please set GEMINI_API_KEY in your .env file")
        return False

    print(f"\n✓ Gemini API Key found: {settings.GEMINI_API_KEY[:10]}...")
    print(f"✓ Model: {settings.GEMINI_MODEL}")

    # Initialize music service
    print("\n" + "-" * 60)
    print("Initializing Music Service...")
    try:
        music_service = MusicService()
        print("✓ Music Service initialized successfully")
    except Exception as e:
        print(f"❌ ERROR: Failed to initialize music service: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Create output directory
    output_dir = Path("./test_output")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "test_music.wav"

    # Test music generation
    print("\n" + "-" * 60)
    print("Testing Music Generation...")
    print("Duration: 10 seconds")
    print("Mood: calm")
    print(f"Output path: {output_path}")

    try:
        result_path = await music_service.generate_music(
            duration=10,  # 10 seconds for quick test
            mood="calm",
            output_path=str(output_path)
        )

        print(f"\n✓ Music generation successful!")
        print(f"✓ Music file saved to: {result_path}")

        # Check file size
        if os.path.exists(result_path):
            file_size = os.path.getsize(result_path)
            print(f"✓ File size: {file_size:,} bytes ({file_size / 1024:.2f} KB)")
        else:
            print(f"⚠️  Warning: File not found at {result_path}")

        return True

    except Exception as e:
        print(f"\n❌ ERROR: Music generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_mood_detection():
    """Test mood detection from story text"""

    print("\n" + "=" * 60)
    print("Testing Mood Detection")
    print("=" * 60)

    music_service = MusicService()

    test_stories = {
        "Bedtime story": "The little bunny was sleepy and ready for bed. Time to dream.",
        "Adventure story": "The brave explorer embarked on an exciting quest through the jungle.",
        "Happy story": "The children laughed and played joyfully in the sunny park.",
        "Magical story": "The fairy sprinkled magical sparkles that made everything enchanted.",
        "Playful story": "The silly puppy bounced around and made everyone giggle.",
    }

    for story_type, story_text in test_stories.items():
        mood = music_service.get_story_mood(story_text)
        print(f"✓ {story_type}: {mood}")

    return True


async def test_different_moods():
    """Test generating music with different moods"""

    print("\n" + "=" * 60)
    print("Testing Different Music Moods")
    print("=" * 60)

    music_service = MusicService()
    moods_to_test = ["calm", "happy", "dreamy"]

    output_dir = Path("./test_output")
    output_dir.mkdir(exist_ok=True)

    for mood in moods_to_test:
        print(f"\n→ Testing mood: {mood}")
        output_path = output_dir / f"test_music_{mood}.wav"

        try:
            result_path = await music_service.generate_music(
                duration=5,  # 5 seconds for quick test
                mood=mood,
                output_path=str(output_path)
            )
            print(f"  ✓ {mood.capitalize()} music generated: {result_path}")

            if os.path.exists(result_path):
                file_size = os.path.getsize(result_path)
                print(f"  ✓ File size: {file_size:,} bytes")
        except Exception as e:
            print(f"  ❌ Failed to generate {mood} music: {e}")

    return True


async def main():
    """Run all tests"""

    try:
        # Test basic music generation
        success = await test_music_generation()

        if success:
            # Test mood detection
            await test_mood_detection()

            # Test different moods (commented out to save time/API calls)
            # Uncomment if you want to test multiple moods
            # await test_different_moods()

            print("\n" + "=" * 60)
            print("✅ MUSIC GENERATION TESTS PASSED!")
            print("=" * 60)
            print("\nGoogle Lyria music generation is working correctly!")
            print("You can now use it in your application.")

        else:
            print("\n" + "=" * 60)
            print("❌ TESTS FAILED")
            print("=" * 60)
            print("\nPlease check:")
            print("1. GEMINI_API_KEY is set correctly in .env")
            print("2. Your API key is valid and has access to Lyria")
            print("3. Network connection is working")
            print("4. Google Lyria API is accessible")

    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

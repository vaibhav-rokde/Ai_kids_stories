#!/usr/bin/env python3
"""
Test script for Cartesia TTS integration
"""
import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from app.services.tts_service import TTSService
from app.core.config import settings


async def test_cartesia_tts():
    """Test Cartesia TTS API integration"""

    print("=" * 60)
    print("Testing Cartesia TTS Integration")
    print("=" * 60)

    # Check API key
    if not settings.CARTESIA_API_KEY:
        print("\n❌ ERROR: CARTESIA_API_KEY not found in environment")
        print("Please set CARTESIA_API_KEY in your .env file")
        return False

    print(f"\n✓ API Key found: {settings.CARTESIA_API_KEY[:10]}...")
    print(f"✓ Model ID: {settings.CARTESIA_MODEL_ID}")
    print(f"✓ Voice ID: {settings.CARTESIA_VOICE_ID}")

    # Initialize TTS service
    print("\n" + "-" * 60)
    print("Initializing TTS Service...")
    try:
        tts_service = TTSService()
        print("✓ TTS Service initialized successfully")
    except Exception as e:
        print(f"❌ ERROR: Failed to initialize TTS service: {e}")
        return False

    # Test story text
    test_story = """
    Once upon a time, in a magical forest, there lived a little rabbit named Fluffy.
    Fluffy loved to hop around and explore the beautiful flowers and tall trees.
    One sunny day, Fluffy met a friendly squirrel who showed him a secret path.
    They became the best of friends and had many wonderful adventures together.
    """

    # Create output directory
    output_dir = Path("./test_output")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "test_cartesia_tts.wav"

    # Test TTS generation
    print("\n" + "-" * 60)
    print("Testing TTS Generation...")
    print(f"Story length: {len(test_story)} characters")
    print(f"Output path: {output_path}")

    try:
        result_path = await tts_service.generate_speech(
            story_text=test_story,
            output_path=str(output_path),
            speed=1.0,
            emotion="happy"
        )

        print(f"✓ TTS generation successful!")
        print(f"✓ Audio file saved to: {result_path}")

        # Check file size
        file_size = os.path.getsize(result_path)
        print(f"✓ File size: {file_size:,} bytes ({file_size / 1024:.2f} KB)")

        return True

    except Exception as e:
        print(f"❌ ERROR: TTS generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_emotion_detection():
    """Test emotion detection for stories"""

    print("\n" + "=" * 60)
    print("Testing Emotion Detection")
    print("=" * 60)

    tts_service = TTSService()

    test_stories = {
        "Happy story": "The children laughed and played joyfully in the sunny park.",
        "Sad story": "The little puppy was lost and cried for his mother.",
        "Exciting story": "The brave knight embarked on an exciting adventure.",
        "Calm story": "The peaceful forest was gentle and quiet under the moonlight.",
        "Scary story": "The child was afraid and worried about the dark shadows.",
    }

    for story_type, story_text in test_stories.items():
        emotion = await tts_service.get_emotion_for_story(story_text)
        print(f"✓ {story_type}: {emotion}")

    return True


async def test_voice_list():
    """Test available voices"""

    print("\n" + "=" * 60)
    print("Testing Available Voices")
    print("=" * 60)

    tts_service = TTSService()
    voices = tts_service.get_available_voices()

    print(f"\nFound {len(voices)} child-friendly voices:")
    for voice_id, voice_name in voices.items():
        print(f"  • {voice_name}")
        print(f"    ID: {voice_id}")

    return True


async def main():
    """Run all tests"""

    try:
        # Test TTS generation
        success = await test_cartesia_tts()

        if success:
            # Test emotion detection
            await test_emotion_detection()

            # Test voice list
            await test_voice_list()

            print("\n" + "=" * 60)
            print("✅ ALL TESTS PASSED!")
            print("=" * 60)
            print("\nCartesia TTS is working correctly!")
            print("You can now use it in your application.")

        else:
            print("\n" + "=" * 60)
            print("❌ TESTS FAILED")
            print("=" * 60)
            print("\nPlease check:")
            print("1. CARTESIA_API_KEY is set correctly in .env")
            print("2. Your API key is valid and has credits")
            print("3. Network connection is working")

    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

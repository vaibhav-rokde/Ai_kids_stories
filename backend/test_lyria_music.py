#!/usr/bin/env python3
"""
Test script for Google Lyria Music Generation
"""
import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from app.services.music_service import MusicService
from app.core.config import settings


async def test_lyria_music():
    """Test Lyria music generation"""

    print("=" * 60)
    print("Testing Google Lyria Music Generation")
    print("=" * 60)

    # Check Gemini API key
    if not settings.GEMINI_API_KEY:
        print("\n❌ ERROR: GEMINI_API_KEY not found in environment")
        print("Please set GEMINI_API_KEY in your .env file")
        return False

    print(f"\n✓ Gemini API Key found: {settings.GEMINI_API_KEY[:10]}...")

    # Initialize music service
    print("\n" + "-" * 60)
    print("Initializing Music Service...")
    try:
        music_service = MusicService()
        print("✓ Music Service initialized successfully")
        print(f"✓ Model: {music_service.model}")
    except Exception as e:
        print(f"❌ ERROR: Failed to initialize music service: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Create output directory
    output_dir = Path("./test_output")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "test_lyria_music.wav"

    # Test music generation
    print("\n" + "-" * 60)
    print("Testing Lyria Music Generation...")
    print("Duration: 10 seconds")
    print("Mood: calm")
    print(f"Output path: {output_path}")

    try:
        result_path = await music_service.generate_music(
            duration=10,  # 10 seconds for quick test
            mood="calm",
            output_path=str(output_path)
        )

        print(f"\n✅ Music generation successful!")
        print(f"✓ Music file saved to: {result_path}")

        # Check file size
        if os.path.exists(result_path):
            file_size = os.path.getsize(result_path)
            print(f"✓ File size: {file_size:,} bytes ({file_size / 1024:.2f} KB)")

            # Check file format
            import wave
            with wave.open(result_path, 'rb') as wav_file:
                channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                framerate = wav_file.getframerate()
                frames = wav_file.getnframes()
                duration = frames / float(framerate)
                print(f"✓ Audio format: {channels} channels, {sample_width*8}-bit, {framerate} Hz")
                print(f"✓ Duration: {duration:.2f} seconds")
        else:
            print(f"⚠️  Warning: File not found at {result_path}")

        return True

    except Exception as e:
        print(f"\n❌ ERROR: Music generation failed")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


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
        output_path = output_dir / f"test_lyria_{mood}.wav"

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
        success = await test_lyria_music()

        if success:
            print("\n" + "=" * 60)
            print("✅ LYRIA MUSIC GENERATION TESTS PASSED!")
            print("=" * 60)
            print("\nGoogle Lyria music generation is working correctly!")
            print("You can now use it in your story generation.")

            # Optionally test different moods
            # Uncomment to test multiple moods
            # await test_different_moods()

        else:
            print("\n" + "=" * 60)
            print("❌ TESTS FAILED")
            print("=" * 60)
            print("\nPossible issues:")
            print("1. GEMINI_API_KEY not set correctly in .env")
            print("2. Lyria API not accessible (experimental API)")
            print("3. google-genai package version mismatch")
            print("4. Network connection issues")
            print("\nCurrent google-genai version:")
            import google.genai
            print(f"   Version: {google.genai.__version__ if hasattr(google.genai, '__version__') else 'unknown'}")

    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
"""Test Azure Speech Service credentials"""

import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

# Load environment variables
load_dotenv('backend/.env')

AZURE_SPEECH_KEY = os.getenv('AZURE_SPEECH_KEY')
AZURE_SPEECH_REGION = os.getenv('AZURE_SPEECH_REGION')

print("Testing Azure Speech Service...")
print(f"Region: {AZURE_SPEECH_REGION}")
print(f"Key: {AZURE_SPEECH_KEY[:10]}..." if AZURE_SPEECH_KEY else "Key: NOT SET")

try:
    # Create speech config
    speech_config = speechsdk.SpeechConfig(
        subscription=AZURE_SPEECH_KEY,
        region=AZURE_SPEECH_REGION
    )
    speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

    # Test synthesis
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    result = synthesizer.speak_text_async("Hello, this is a test.").get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("✅ SUCCESS: Azure TTS is working!")
        print(f"   Audio data size: {len(result.audio_data)} bytes")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation = result.cancellation_details
        print(f"❌ FAILED: {cancellation.reason}")
        if cancellation.reason == speechsdk.CancellationReason.Error:
            print(f"   Error code: {cancellation.error_code}")
            print(f"   Error details: {cancellation.error_details}")
            print("\n💡 Common issues:")
            print("   1. Invalid subscription key")
            print("   2. Incorrect region")
            print("   3. Subscription expired or not active")
            print("\n📋 How to fix:")
            print("   1. Go to https://portal.azure.com")
            print("   2. Navigate to your Speech Service resource")
            print("   3. Go to 'Keys and Endpoint'")
            print("   4. Copy Key 1 and Region")
            print("   5. Update backend/.env with correct values")

except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    print("\n💡 This error suggests:")
    print("   - Azure credentials are not valid")
    print("   - Or Azure Speech SDK has initialization issues")

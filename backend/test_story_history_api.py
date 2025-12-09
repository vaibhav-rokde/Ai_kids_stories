#!/usr/bin/env python3
"""
Test script to verify story history API
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import SessionLocal
from app.models.user import User
from app.models.story import Story
from app.core.security import create_access_token
import requests

def test_story_history():
    print("=" * 60)
    print("Testing Story History API")
    print("=" * 60)

    # Get users from database
    db = SessionLocal()
    users = db.query(User).all()

    if not users:
        print("\n❌ No users found in database")
        return

    print(f"\n✓ Found {len(users)} users in database")

    # Test for each user
    for user in users:
        print(f"\n{'='*60}")
        print(f"Testing user: {user.username} (ID: {user.id})")
        print(f"Email: {user.email}")
        print(f"{'='*60}")

        # Get user's stories from database
        user_stories = db.query(Story).filter(Story.user_id == user.id).all()
        print(f"\n📊 Database: User has {len(user_stories)} stories")

        if user_stories:
            for story in user_stories:
                print(f"   - Story #{story.id}: {story.story_title or 'Untitled'}")
                print(f"     Theme: {story.theme}, Status: {story.status}")

        # Generate token for this user (matching auth.py format)
        token = create_access_token(data={"sub": str(user.id), "email": user.email})
        print(f"\n✓ Generated JWT token: {token[:20]}...")

        # Test API endpoint
        print(f"\n🔍 Testing API: GET /api/v1/stories/my-stories")
        try:
            response = requests.get(
                "http://localhost:8000/api/v1/stories/my-stories",
                headers={"Authorization": f"Bearer {token}"}
            )

            if response.status_code == 200:
                data = response.json()
                print(f"✅ API Success!")
                print(f"   Total stories in response: {data.get('total', 0)}")
                print(f"   Stories returned: {len(data.get('stories', []))}")

                if data.get('stories'):
                    for story in data['stories']:
                        print(f"   - Story #{story['id']}: {story.get('story_title', 'Untitled')}")
                else:
                    print("   ⚠️  API returned 0 stories but database has stories!")
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"   Response: {response.text}")

        except Exception as e:
            print(f"❌ Request failed: {e}")

    db.close()

    print("\n" + "=" * 60)
    print("Test Complete")
    print("=" * 60)

if __name__ == "__main__":
    test_story_history()

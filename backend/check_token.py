#!/usr/bin/env python3
"""
Script to decode JWT token and check which user it belongs to
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.security import verify_token
from app.core.database import SessionLocal
from app.models.user import User

def check_token(token):
    """Check which user a token belongs to"""

    print("=" * 60)
    print("JWT Token Decoder")
    print("=" * 60)

    # Decode token
    payload = verify_token(token)

    if not payload:
        print("\n❌ Invalid or expired token")
        return

    print(f"\n✓ Token is valid")
    print(f"\nToken Payload:")
    print(f"  User ID (sub): {payload.get('sub')}")
    print(f"  Email: {payload.get('email')}")
    print(f"  Expires: {payload.get('exp')}")

    # Get user from database
    user_id = int(payload.get('sub'))
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()

    if user:
        print(f"\n📊 User Details:")
        print(f"  ID: {user.id}")
        print(f"  Username: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Active: {user.is_active}")

        # Check stories
        from app.models.story import Story
        stories = db.query(Story).filter(Story.user_id == user.id).all()
        print(f"\n📚 User's Stories: {len(stories)}")
        if stories:
            for story in stories:
                print(f"  - Story #{story.id}: {story.story_title or 'Untitled'}")
                print(f"    Status: {story.status}")
        else:
            print("  No stories found for this user")
    else:
        print(f"\n❌ User not found in database")

    db.close()
    print("\n" + "=" * 60)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        token = sys.argv[1]
        check_token(token)
    else:
        print("Usage: python check_token.py <JWT_TOKEN>")
        print("\nPaste your JWT token from browser localStorage:")
        print("1. Open DevTools (F12)")
        print("2. Go to Application → Local Storage → http://localhost:8080")
        print("3. Find 'auth_token' value")
        print("4. Run: python check_token.py <token>")

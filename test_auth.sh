#!/bin/bash

echo "=== Testing Authentication System ==="
echo ""

# Login
echo "1. Logging in..."
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@example.com","password":"demo123"}')
TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
  echo "❌ Login failed"
  exit 1
fi

echo "✅ Login successful"
echo ""

# Test /auth/me
echo "2. Getting current user info..."
curl -s -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer $TOKEN" | grep -q '"email"'

if [ $? -eq 0 ]; then
  echo "✅ /auth/me working"
else
  echo "❌ /auth/me failed"
fi
echo ""

# Create story with auth
echo "3. Creating story WITH authentication..."
STORY_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/stories/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"theme":"underwater adventure","character_name":"Mia","age_group":"5-7"}')
STORY_ID=$(echo $STORY_RESPONSE | grep -o '"id":[0-9]*' | cut -d':' -f2)

if [ ! -z "$STORY_ID" ]; then
  echo "✅ Story created (ID: $STORY_ID)"
else
  echo "❌ Story creation failed"
  echo "$STORY_RESPONSE"
fi
echo ""

# Test my-stories endpoint
echo "4. Getting user's stories..."
MY_STORIES=$(curl -s -X GET http://localhost:8000/api/v1/stories/my-stories \
  -H "Authorization: Bearer $TOKEN")
echo "$MY_STORIES" | grep -q '"total"'

if [ $? -eq 0 ]; then
  TOTAL=$(echo "$MY_STORIES" | grep -o '"total":[0-9]*' | cut -d':' -f2)
  echo "✅ /my-stories working (Total stories: $TOTAL)"
else
  echo "❌ /my-stories failed"
  echo "$MY_STORIES"
fi
echo ""

# Test story creation WITHOUT auth
echo "5. Creating story WITHOUT authentication..."
NO_AUTH_STORY=$(curl -s -X POST http://localhost:8000/api/v1/stories/ \
  -H "Content-Type: application/json" \
  -d '{"theme":"forest adventure","character_name":"Sam","age_group":"7-9"}')
NO_AUTH_ID=$(echo $NO_AUTH_STORY | grep -o '"id":[0-9]*' | cut -d':' -f2)

if [ ! -z "$NO_AUTH_ID" ]; then
  echo "✅ Anonymous story created (ID: $NO_AUTH_ID)"
else
  echo "❌ Anonymous story creation failed"
  echo "$NO_AUTH_STORY"
fi
echo ""

echo "=== Test Complete ==="

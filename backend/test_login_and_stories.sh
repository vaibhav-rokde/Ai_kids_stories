#!/bin/bash

echo "=========================================="
echo "Testing Login and Story Retrieval"
echo "=========================================="

# Login
echo "Logging in as demo@example.com..."
RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@example.com", "password": "Demo@123"}')

TOKEN=$(echo "$RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)

if [ -z "$TOKEN" ]; then
    echo "❌ Login failed!"
    echo "Response: $RESPONSE"
    exit 1
fi

echo "✅ Login successful!"
echo "Token: ${TOKEN:0:30}..."
echo ""

# Get user info
echo "Getting user info..."
USER_INFO=$(curl -s http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer $TOKEN")

echo "$USER_INFO" | python -m json.tool
echo ""

# Get stories
echo "Getting user's stories..."
STORIES=$(curl -s http://localhost:8000/api/v1/stories/my-stories \
  -H "Authorization: Bearer $TOKEN")

echo "$STORIES" | python -m json.tool

echo ""
echo "=========================================="
echo "Test Complete!"
echo "=========================================="

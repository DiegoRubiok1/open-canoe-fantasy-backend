#!/bin/bash

echo "=== Testing Authentication Flow ==="

# 1. Register User
echo -e "\n1. Registering new user..."
REGISTER_RESPONSE=$(curl -s -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser5",
    "email": "test5@example.com",
    "password": "secret123",
    "first_name": "Test",
    "last_name": "User"
  }')
echo "$REGISTER_RESPONSE"

# 2. Login and get token
echo -e "\n2. Logging in..."
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test5@example.com",
    "password": "secret123"
  }')
echo "$LOGIN_RESPONSE"

# Extract token using jq
TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.access_token')

# Verify token was extracted
if [ -z "$TOKEN" ] || [ "$TOKEN" = "null" ]; then
    echo "Failed to extract token"
    exit 1
fi

echo -e "\nToken extracted: ${TOKEN:0:20}..." # Show first 20 chars only

# 3. Test protected endpoint with proper token
echo -e "\n3. Creating league with token..."
LEAGUE_RESPONSE=$(curl -s -X POST http://localhost:5000/api/leagues/leagues \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test League 2025"
  }')
echo "$LEAGUE_RESPONSE" | jq '.'

# 4. Get leagues to verify creation
echo -e "\n4. Getting leagues..."
LEAGUES_RESPONSE=$(curl -s -X GET http://localhost:5000/api/leagues/leagues \
  -H "Authorization: Bearer ${TOKEN}")
echo "$LEAGUES_RESPONSE" | jq '.'
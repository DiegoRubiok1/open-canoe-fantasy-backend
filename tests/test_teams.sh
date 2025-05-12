#!/bin/bash

echo "=== Testing Teams API Endpoints ==="

# 0. Register new user
echo -e "\n0. Registering new user..."
REGISTER_RESPONSE=$(curl -s -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "secret123",
    "first_name": "Test",
    "last_name": "User"
  }')
echo "$REGISTER_RESPONSE"

# 1. Login and get token
echo -e "\n1. Logging in..."
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "secret123"
  }')

# Debug login response
echo "Login Response:"
echo "$LOGIN_RESPONSE" | jq '.'

# Extract token with error checking
TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.access_token // empty')

# Verify token with detailed error
if [ -z "$TOKEN" ]; then
    echo "Error: Failed to extract token from response"
    echo "Raw response was:"
    echo "$LOGIN_RESPONSE"
    exit 1
fi

echo -e "\nToken extracted successfully: ${TOKEN:0:20}..."

# 1.5 Create a league first (since we need a league to create a team)
echo -e "\n1.5 Creating league..."
LEAGUE_RESPONSE=$(curl -s -X POST http://localhost:5000/api/leagues/leagues \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test League 2025"
  }')
echo "$LEAGUE_RESPONSE"

# Extract league_id
LEAGUE_ID=$(echo "$LEAGUE_RESPONSE" | jq -r '.league_id')

# 2. Create a team
echo -e "\n2. Creating team..."
TEAM_RESPONSE=$(curl -s -X POST http://localhost:5000/api/teams/create \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"Test Team 2025\",
    \"league_id\": $LEAGUE_ID
  }")
echo "$TEAM_RESPONSE"

# Extract team_id
TEAM_ID=$(echo "$TEAM_RESPONSE" | jq -r '.team_id')

# 3. Set players for team
echo -e "\n3. Setting players..."
curl -s -X POST http://localhost:5000/api/teams/set \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"team_id\": $TEAM_ID,
    \"players\": [1, 2, 3, 4]
  }" | jq '.'

# 4. Get team details
echo -e "\n4. Getting team details..."
curl -s -X GET http://localhost:5000/api/teams/teams/$TEAM_ID \
  -H "Authorization: Bearer $TOKEN" | jq '.'

# 5. Get all teams in league
echo -e "\n5. Getting all teams in league..."
curl -s -X GET http://localhost:5000/api/teams/leagues/1/teams \
  -H "Authorization: Bearer $TOKEN" | jq '.'
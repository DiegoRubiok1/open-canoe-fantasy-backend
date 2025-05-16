# Leagues API Documentation

## Overview
The leagues API enables users to create and manage fantasy leagues. All endpoints require JWT authentication.

## Endpoints

### Create League
```http
POST /api/leagues/create
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
    "name": "string",               // Required
    "budget": 10000.0              // Optional, defaults to 10000.0
}
```

**Success Response (201)**
```json
{
    "message": "League created successfully",
    "league_id": 123,
    "code": "ABC12345"             // Generated 8-character unique code
}
```

### Get User's Leagues
```http
GET /api/leagues/show
Authorization: Bearer <jwt_token>
```

**Success Response (200)**
```json
{
    "leagues": [
        {
            "id": 123,
            "name": "string",
            "code": "ABC12345",
            "budget": 10000.0,
            "points": 0,
            "created_at": "2025-05-08T12:21:20",
            "updated_at": "2025-05-08T12:21:20"
        }
    ]
}
```

**Empty Response (200)**
```json
{
    "message": "No active leagues found"
}
```

### Show League Users
```http
GET /api/leagues/users/show/{league_id}
Authorization: Bearer <jwt_token>
```

**Success Response (200)**
```json
[
    {
        "id": 1,
        "username": "string",
        "team_id": 123,            // null if user has no team
        "budget": 10000.0,
        "points": 0
    }
]
```

### Join League
```http
POST /api/leagues/join
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
    "code": "ABC12345"            // Required: League code
}
```

**Success Response (200)**
```json
{
    "message": "User username successfuly added to league name",
    "league_id": 123
}
```

## Error Responses

All endpoints may return these errors:

```json
{"error": "User not found"}                              // 404
{"error": "League not found"}                           // 404
{"error": "No JSON data provided"}                      // 400
{"error": "League name is required"}                    // 400
{"error": "code must not be empty"}                     // 402
{"message": "conflict user already in league"}          // 409
{"error": "Failed to retrieve leagues: <error>"}        // 500
```

## Implementation Details

### Authentication
- All endpoints require valid JWT token
- User ID is extracted from token using `get_jwt_identity()`

### League Features
- Unique 8-character codes using uppercase letters and numbers
- Automatic market initialization on league creation
- User budget tracking per league
- Points system per league
- Team association tracking

### Testing Example
```bash
# Login and get token
TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email":"test@example.com",
    "password":"secret123"
  }' | jq -r '.access_token')

# Create league
curl -X POST http://localhost:5000/api/leagues/create \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test League"}'

# Join league
curl -X POST http://localhost:5000/api/leagues/join \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"code": "ABC12345"}'

# List league users
curl -X GET http://localhost:5000/api/leagues/users/show/123 \
  -H "Authorization: Bearer $TOKEN"
```


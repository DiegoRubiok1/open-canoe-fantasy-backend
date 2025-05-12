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
    "budget": 100000.0             // Optional, defaults to 100000.0
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

**Error Responses**
```json
{"error": "League name is required"}                      // 400
{"error": "User ID is required"}                         // 400
{"error": "User not found"}                             // 404
{"error": "League creation failed: <error_message>"}     // 500
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
            "budget": 100000.0,
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

**Error Responses**
```json
{"error": "User not found"}                                    // 404
{"error": "Failed to retrieve leagues: <error_message>"}       // 500
```

## Implementation Details

### Authentication
- All endpoints require valid JWT token
- User ID is automatically extracted from JWT token using `get_jwt_identity()`
- Invalid/expired tokens return 401 Unauthorized

### League Creation Process
1. Validates required name field
2. Generates unique 8-character code (uppercase letters + numbers)
3. Creates League record
4. Creates UserLeague association for creator
5. Initializes market for the league
6. Handles all operations in a single transaction

### League Retrieval Features
- Returns only non-deleted leagues (deleted_at is NULL)
- Includes user-specific budget and points from UserLeague
- Returns ISO 8601 formatted timestamps
- Automatically filters soft-deleted leagues

### Testing Example
```bash
# Login and get token
TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email":"test@example.com",
    "password":"secret123"
  }' | jq -r '.access_token')

# Create new league
curl -X POST http://localhost:5000/api/leagues/create \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test League 2025",
    "budget": 100000.0
  }'

# List user's leagues
curl -X GET http://localhost:5000/api/leagues/show \
  -H "Authorization: Bearer $TOKEN"
```

### Default Values
- Initial budget: 100,000.0
- Initial points: 0
- League code: Random 8-character string using [A-Z0-9]
- Timestamps: ISO 8601 format (YYYY-MM-DDTHH:MM:SS)

### Market Initialization
- Automatically creates market entries after league creation
- Market is updated using the `update_market()` service
- Players are randomly selected and priced


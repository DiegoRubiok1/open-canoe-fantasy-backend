# Leagues API Documentation

## Overview
The leagues API enables users to create and manage fantasy leagues. All endpoints require JWT authentication.

## Endpoints

### Create League
```http
POST /api/leagues/leagues
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
    "name": "string",
    "budget": 100000.0  // Optional, defaults to 100000.0
}
```

**Response (201)**
```json
{
    "message": "League created successfully",
    "league_id": 123,
    "code": "ABC12345"  // 8 character unique code
}
```

**Error Responses**
```json
{"error": "League name is required"} // 400
{"error": "User not found"} // 404
{"error": "League creation failed: <error_message>"} // 500
```

### Get User's Leagues
```http
GET /api/leagues/leagues
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

**Error Response (404)**
```json
{
    "error": "User not found"
}
```

## Implementation Details

### League Code Generation
- 8 characters long
- Uses uppercase letters and numbers
- Guaranteed unique through database check

### Default Values
- Initial budget: 100,000.0
- Initial points: 0
- Status: Active by default
- Soft delete using `deleted_at`

### Security
- All endpoints require valid JWT token
- User ID is extracted from JWT token
- Only active (non-deleted) leagues are returned
- User validation before any operation

## Testing Example
```bash
# Login and save token
export TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"secret123"}' \
  | jq -r '.access_token')

# Create league
curl -X POST http://localhost:5000/api/leagues/leagues \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test League 2025"}'

# Get user's leagues
curl -X GET http://localhost:5000/api/leagues/leagues \
  -H "Authorization: Bearer $TOKEN"
```


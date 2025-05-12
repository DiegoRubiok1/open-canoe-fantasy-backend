# Teams API Documentation

## Overview
The teams API enables users to create and manage their fantasy teams. All endpoints require JWT authentication.

## Endpoints

### Create Team
```http
POST /api/teams/create
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
    "name": "string",        // Required
    "league_id": integer     // Required
}
```

**Success Response (201)**
```json
{
    "message": "Team created successfully",
    "team_id": 123
}
```

### Set Team Players
```http
POST /api/teams/set
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
    "team_id": integer,      // Required
    "players": [             // Required, exactly 4 player IDs
        1, 2, 3, 4
    ]
}
```

**Success Response (200)**
```json
{
    "message": "Team updated successfully",
    "team_id": 123,
    "players": [1, 2, 3, 4]
}
```

### Get Team Details
```http
GET /api/teams/teams/{team_id}
Authorization: Bearer <jwt_token>
```

### List League Teams
```http
GET /api/teams/leagues/{league_id}/teams
Authorization: Bearer <jwt_token>
```

## Testing Example
```bash
# Login and get token
TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email":"test@example.com",
    "password":"secret123"
  }' | jq -r '.access_token')

# Create team
curl -X POST http://localhost:5000/api/teams/create \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Team",
    "league_id": 1
  }'
```

## Error Responses
- 400: Bad Request (invalid/missing parameters)
- 401: Unauthorized (invalid/missing token)
- 404: Not Found (team/league/user not found)
- 500: Server Error
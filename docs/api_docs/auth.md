# Authentication API Documentation

## Overview

The authentication system provides JWT-based authentication for the Open Canoe Fantasy API. It supports user registration, login, and profile management.

## Endpoints

### Register a New User

```http
POST /api/auth/register
Content-Type: application/json

{
    "username": "string",
    "email": "string",
    "password": "string",
    "first_name": "string",
    "last_name": "string",
    "phone": "string"
}
```

**Response (201)**

```json
{
    "message": "Registration successful",
    "user_id": 123
}
```

### Login

```http
POST /api/auth/login
Content-Type: application/json

{
    "email": "string",
    "password": "string"
}
```

**Response (200)**

```json
{
    "access_token": "jwt.token.here",
    "user": {
        "id": 123,
        "username": "string",
        "email": "string",
        "role": "user",
        "status": "active"
    }
}
```

### Get User Profile (Protected Endpoint)

```http
GET /api/auth/me
Authorization: Bearer <access_token>
```

**Response (200)**

```json
{
    "id": 123,
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "role": "string",
    "status": "string"
}
```

**Error Responses**
- **401 Unauthorized**: Missing or invalid token
- **404 Not Found**: User not found

## Error Responses

- **400 Bad Request**: Invalid input data
- **401 Unauthorized**: Invalid credentials
- **404 Not Found**: Resource not found

## Models

### User

```python
class User:
    id: int                  # Auto-incrementing ID
    username: string         # Unique username
    email: string           # Unique email address
    password_hash: string   # Bcrypt hashed password
    first_name: string      # Optional
    last_name: string       # Optional
    phone: string          # Optional
    role: string           # Default: 'user'
    status: string         # 'active', 'suspended', 'deleted'
    created_at: datetime   # Auto-set on creation
    updated_at: datetime   # Auto-updated
    deleted_at: datetime   # Soft delete timestamp
```

## Security Considerations

- Passwords are hashed using Bcrypt
- Emails are normalized to lowercase
- JWT tokens are required for protected endpoints
- Input validation ensures data integrity
- Database transactions prevent partial updates
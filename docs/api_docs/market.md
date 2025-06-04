# Market API Documentation

## Endpoints

### Show Market
Lists all players available in a league's market.

**URL:** `/market/show/<league_id>`  
**Method:** `GET`  
**Auth required:** Yes (JWT Token)

**URL Parameters:**
- `league_id`: ID of the league to show market for

**Success Response:**
- **Code:** 200
- **Content:**
```json
{
    "market_entries": [
        {
            "id": 1,
            "name": "Player Name",
            "club": "Club Name",
            "category": "Position",
            "price": 1000000.0,
            "days_listed": 3
        }
    ],
    "total_entries": 1
}
```

**Error Responses:**
- **Code:** 404
  - **Content:** `{"message": "No players available in the market for this league."}`
- **Code:** 401
  - **Content:** `{"message": "User not authenticated."}`

### Purchase Player
Purchase a player from the market.

**URL:** `/market/purchase`  
**Method:** `POST`  
**Auth required:** Yes (JWT Token)

**Request Body:**
```json
{
    "league_id": 1,
    "player_id": 1
}
```

**Success Response:**
- **Code:** 200
- **Content:**
```json
{
    "message": "Player purchased successfully.",
    "remaining_budget": 5000000.0
}
```

**Error Responses:**
- **Code:** 400
  - **Content:** `{"message": "Insufficient balance to purchase this player."}`
  - **Content:** `{"message": "Team is already full."}`
  - **Content:** `{"message": "Missing required parameters."}`
- **Code:** 404
  - **Content:** `{"message": "Player not found in the market."}`
  - **Content:** `{"message": "User not found."}`
  - **Content:** `{"message": "User does not have a team in this league."}`
- **Code:** 403
  - **Content:** `{"message": "User is not a member of this league."}`

### Sell Player
Put a player up for sale in the market.

**URL:** `/market/sell`  
**Method:** `POST`  
**Auth required:** Yes (JWT Token)

**Request Body:**
```json
{
    "league_id": 1,
    "player_id": 1
}
```

**Success Response:**
- **Code:** 200
- **Content:**
```json
{
    "message": "Player sold successfully.",
    "market_entry": {
        "id": 1,
        "name": "Player Name",
        "price": 1000000.0,
        "days_listed": 0
    },
    "new_budget": 6000000.0
}
```

**Error Responses:**
- **Code:** 400
  - **Content:** `{"message": "Cannot sell a titular player."}`
  - **Content:** `{"message": "Missing required parameters."}`
- **Code:** 404
  - **Content:** `{"message": "Player not found."}`
  - **Content:** `{"message": "User not found."}`
  - **Content:** `{"message": "Player is not in your team."}`
  - **Content:** `{"message": "User does not have a team in this league."}`
- **Code:** 403
  - **Content:** `{"message": "User is not a member of this league."}`

## Notes
- Market entries are automatically updated
- Players are sold at 90% of their market price
- A team must maintain a minimum of players
- Titular players cannot be sold
- Market has a maximum capacity of 5 players
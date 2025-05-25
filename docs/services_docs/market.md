# Market Service Documentation

## Market Update Function

The `update_market()` function manages the player market for a specific league. It handles removing expired entries and adding new players to the market.

### Function Signature
```python
def update_market(league_id: int) -> List[Player]
```

### Parameters
- `league_id` (int): The unique identifier of the league to update the market for

### Returns
- `List[Player]`: A list of Player objects that were added to the market
- Returns an empty list if no players were added

### Process Flow
1. **League Validation**
   - Verifies the league exists
   - Raises ValueError if league not found

2. **Get Existing Team Players**
   - Collects IDs of all players currently in teams
   - Prevents these players from being added to market

3. **Clean Old Entries**
   - Removes market entries older than 7 days
   - Uses `available_from` timestamp for age check

4. **Add New Players**
   - Randomly selects from available players
   - Adds players until market has 5 entries
   - Only adds players not currently in teams
   - Sets player price based on `market_price` attribute

### Error Handling
- Uses database transaction rollback on errors
- Raises ValueError with descriptive message on failure

### Usage Example
```python
try:
    added_players = update_market(league_id=1)
    print(f"Added {len(added_players)} players to market")
except ValueError as e:
    print(f"Market update failed: {e}")
```

### Notes
- Maximum of 5 players in market at any time
- Players remain in market for 7 days
- Transaction is atomic - either all changes succeed or none do
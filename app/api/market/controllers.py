from app.models.user import User
from app.models.market import Market
from app.models.league import League
from app.models.player import Player

def show_market(league_id: int) -> tuple[dict, int]:
    """
    List players in a specific market for a league.
    
    Args:
        league_id: ID of the league to show market for
        
    Returns:
        tuple: (response_data, status_code)
    """
    market_entries = Market.query.filter_by(league_id=league_id).all()

    if not market_entries:
        return {"message": "No players available in the market for this league."}, 404
    
    market_data = []
    for entry in market_entries:
        player = Player.query.get(entry.player_id)
        
        if not player:
            continue
            
        market_data.append({
            "id": player.id,
            "name": player.name,
            "club": player.club,
            "category": player.category,
            "price": float(entry.price),
            "days_listed": entry.days_listed
        })
    
    return {
        "market_entries": market_data,
        "total_entries": len(market_data)
    }, 200


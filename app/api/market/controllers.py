from app.models.user import User
from app.models.market import Market
from app.models.league import League
from app.models.player import Player
from app.models.team import Team
from app.models.user_league import UserLeague
from app.models.team_player import TeamPlayer
from app.extensions import db
from app.services.market_service import update_market

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

def purchase_player(league_id: int, player_id: int, user_id: int) -> tuple[dict, int]:
    """
    Purchase a player from the market.
    
    Args:
        league_id: ID of the league to purchase from
        player_id: ID of the player to purchase
        user_id: ID of the user making the purchase
        
    Returns:
        tuple: (response_data, status_code)
    """
    try:
        # Validate market entry exists
        market_entry = Market.query.filter_by(league_id=league_id, player_id=player_id).first()
        if not market_entry:
            return {"message": "Player not found in the market."}, 404

        # Validate user and membership
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found."}, 404

        user_league = UserLeague.query.filter_by(user_id=user_id, league_id=league_id).first()
        if not user_league:
            return {"message": "User is not a member of this league."}, 403

        # Get user's team
        team = Team.query.filter_by(user_id=user_id, league_id=league_id).first()
        if not team:
            return {"message": "User does not have a team in this league."}, 404

        # Validate budget
        if market_entry.price > user_league.budget:
            return {"message": "Insufficient balance to purchase this player."}, 400

        # Validate team size
        current_players = TeamPlayer.query.filter_by(team_id=team.id).count()
        if current_players >= 10:  # Assuming max team size is 15
            return {"message": "Team is already full."}, 400

        # Check if player is already in user's team
        existing_player = TeamPlayer.query.filter_by(
            team_id=team.id, 
            player_id=player_id
        ).first()
        if existing_player:
            return {"message": "Player is already in your team."}, 400

        # Perform transaction
        user_league.budget -= market_entry.price
        db.session.delete(market_entry)
        
        user_team_player = TeamPlayer(
            team_id=team.id, 
            player_id=player_id, 
            clause=market_entry.price
        )
        db.session.add(user_team_player)
        
        db.session.commit()
        
        # Update market
        update_market(league_id)

        return {
            "message": "Player purchased successfully.",
            "remaining_budget": float(user_league.budget)
        }, 200

    except Exception as e:
        db.session.rollback()
        return {"message": f"Error purchasing player: {str(e)}"}, 500

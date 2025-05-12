from datetime import datetime, timedelta
from typing import List
from app.extensions import db
from app.models.player import Player
from app.models.league import League
from app.models.market import Market
import random

def update_market(league_id: int) -> List[Player]:
    """Update market entries for a league.
    
    Args:
        league_id: League identifier
        
    Returns:
        List of players added to market
        Empty list if no players were added
    """
    try:
        # Get league and validate
        league = League.query.filter_by(id=league_id).first()
        if not league:
            raise ValueError(f"League {league_id} not found")

        print(f"Updating market for league {league_id}")


        # Get players already in teams
        players_users_id = []
        for user in league.users:
            for player_team in user.get_team(league_id, player_associations=True):
                players_users_id.append(player_team.player_id)
        
        print(f"Players already in teams: {players_users_id}")


        # Remove old entries
        market_entries = Market.query.filter_by(league_id=league_id)
        for entry in market_entries:
            if entry.available_from <= datetime.utcnow() - timedelta(days=7):
                db.session.delete(entry)

        print(f"Removed old market entries for league {league_id}")

        # Add new players
        available_players = Player.query.all()
        if not available_players:
            return []
        random.shuffle(available_players)
        
        print(f"Available players: {[player.id for player in available_players]}")


        added_players = []
        for player in available_players:
            if player.id not in players_users_id:
                market = Market(
                    league_id=league_id,
                    player_id=player.id,
                    price=player.market_price
                )
                db.session.add(market)
                added_players.append(player)
            
            if len(Market.get_players(league_id)) >= 5:
                break
        print(f"Added players to market: {[player.id for player in added_players]}")

        # Commit changes
        db.session.commit()
        return added_players

    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Failed to update market: {str(e)}")





from app.models.league import League
from app.models.user import User
from app.models.team import Team
from app.models.user_league import UserLeague
from app.models.player import Player
from app.models.team_player import TeamPlayer
from app.extensions import db
from typing import Optional
from datetime import datetime

def create_team_user(data: dict, user_id: int) -> tuple[dict, int]:
    """Create a new team for a user in a specific league."""
    try:
        name = data.get('name')
        if not name:
            return {'error': 'Team name is required'}, 400
        
        
        league_id = data.get('league_id')
        if not league_id:
            return {'error': 'League ID is required'}, 400
        

        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        league: League = League.query.get(league_id)
        if not league:
            return {'error': 'League not found'}, 404
        
        if not league.is_user_in_league(user_id):
            return {'error': 'User is not a member of the league'}, 403
        
        team = Team.query.filter_by(user_id=user_id, league_id=league_id).first()
        if team:
            return {'error': 'User already has a team in this league'}, 400
        
        team = Team(
            name=name,
            user_id=user_id,
            league_id=league_id,
            created_at = datetime.utcnow(),
            updated_at = datetime.utcnow()
        )

        db.session.add(team)
        db.session.commit()

        return {
            'message': 'Team created successfully',
            'team_id': team.id
        }, 201
    
    except Exception as e:

        db.session.rollback()
        return {'error': f'Team creation failed: {str(e)}'}, 500
    
def set_team(data: dict) -> Optional[dict]:
    """Sets players a team. Removes all previous players and adds new ones.
    
    Args:
        data[user_id]: The ID of the user owning the team
        data[team_id]: The ID of the team to modify
        data[players_id]: List of player IDs to add to set team
    """
    try:
        user_id = data.get('user_id')
        if not user_id:
            return {'error': 'User ID is required'}, 400
        
        team_id = data.get('team_id')
        if not team_id:
            return {'error': 'Team ID is required'}, 400
        
        players_id = data.get('players_id')
        if not players_id:
            return {'error': 'Players id list is required'}, 400
          
        user = User.query.get(user_id)

        if not user:
            return {'error': 'User not found'}, 404
        
        team: Team = Team.query.get(team_id).first()
        if not team:
            return {'error': 'Team not found'}, 404
        
        # Verify team belongs to user
        if team.user_id != user_id:
            return {'error': 'Team does not belong to user'}, 403

        # Get player objects and verify they exist
        player_objects = []
        for player_id in players_id:
            player = Player.query.get(player_id).first()
            if not player:
                return {'error': f'Player {player_id} not found'}, 404
            player_objects.append(player)
        
        # Clear existing players
        team.player_associations = [] 
        
        # Add new players
        for player in player_objects:
            player: Player
            team_player = TeamPlayer(
                team_id=team.id,
                player_id = player.id,
                clause=player.market_price, # Set initial clause
                titular = False # default to non-titular
            )
            team.player_associations.append(team_player)

        db.session.commit()
        return {
            'message': 'Team updated successfully',
            'team_id': team.id,
            'players': [p.id for p in team.all_players]
        }, 200

    except Exception as e:
        db.session.rollback()
        return {'error': f'Team update failed: {str(e)}'}, 500

def get_team_details(user_id: int, team_id: int) -> tuple[dict, int]:
    """Get detailed information about a team and its players."""
    try:
        team = Team.query.get(team_id)
        if not team:
            return {'error': 'Team not found'}, 404
            
        if team.user_id != user_id:
            return {'error': 'Unauthorized access to team'}, 403

        players = []
        for assoc in team.player_associations:
            player = assoc.player
            players.append({
                'id': player.id,
                'name': player.name,
                'category': player.category,
                'club': player.club,
                'market_price': float(player.market_price),
                'points': player.points,
                'titular': assoc.titular,
                'clause': float(assoc.clause),
                'added_at': assoc.added_at.isoformat()
            })

        return {
            'id': team.id,
            'name': team.name,
            'league_id': team.league_id,
            'created_at': team.created_at.isoformat(),
            'updated_at': team.updated_at.isoformat(),
            'players': players
        }, 200

    except Exception as e:
        return {'error': f'Failed to retrieve team: {str(e)}'}, 500

def get_league_teams(user_id: int, league_id: int) -> tuple[dict, int]:
    """Get all teams in a league with basic information."""
    try:
        # Verify user belongs to league
        user_league = UserLeague.query.filter_by(
            user_id=user_id,
            league_id=league_id
        ).first()
        
        if not user_league:
            return {'error': 'User does not belong to this league'}, 403

        teams = Team.query.filter_by(league_id=league_id).all()
        
        return {
            'league_id': league_id,
            'teams': [{
                'id': team.id,
                'name': team.name,
                'owner': {
                    'id': team.user.id,
                    'username': team.user.username
                },
                'players_count': len(team.player_associations),
                'total_points': sum(assoc.player.points for assoc in team.player_associations),
                'created_at': team.created_at.isoformat()
            } for team in teams]
        }, 200

    except Exception as e:
        return {'error': f'Failed to retrieve league teams: {str(e)}'}, 500




from app.models.league import League
from app.models.user import User
from app.models.user_league import UserLeague  
from app.models.team import Team
from app.extensions import db
from app.services.market_service import update_market
from decimal import Decimal
import random
import string

def generate_league_code():
    """Generate a random league code."""

    code_length = 8
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(code_length))

def create_league(data, user_id=None):
    """Create a new league with creator user as the first member."""
    try:
        if not data.get('name'):
            return {'error': 'League name is required'}, 400
        
        if not user_id:
            return {'error': 'User ID is required'}, 400
        
        user = User.query.get(int(data['user_id']))
        if not user:
            return {'error': 'User not found'}, 404
        
        code = generate_league_code()
        while League.query.filter_by(code=code).first():
            code = generate_league_code()
        
        league = League(
            name=data['name'],
            code=code
        )
        
        user_league = UserLeague(
            league_id = league.id,
            user_id=user.id,
            budget= Decimal(data.get('budget', Decimal('10000.00'))),
        )
        
        league.user_memberships.append(user_league)
        
        db.session.add(league)
        db.session.commit()
        
        # Creates the market for the league
        update_market(league.id)

        return {
            'message': 'League created successfully',
            'league_id': league.id,
            'code': league.code
        }, 201
    
    except Exception as e:
        db.session.rollback()
        return {'error': f'League creation failed: {str(e)}'}, 500

def get_user_leagues(user_id):
    """Get all leagues for a specific user."""
    try:
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Get active leagues
        leagues = [league for league in user.leagues if not league.deleted_at]
        
        if not leagues:
            return {'message': 'No active leagues found'}, 200

        return {
            'leagues': [
                {
                    'id': league.id,
                    'name': league.name,
                    'code': league.code,
                    'budget': user.get_budget(league.id),
                    'points': user.get_points(league.id),
                    'created_at': league.created_at.isoformat(),
                    'updated_at': league.updated_at.isoformat()
                } for league in leagues
            ]
        }, 200

    except Exception as e:
        return {'error': f'Failed to retrieve leagues: {str(e)}'}, 500

def get_users_in_league(league_id: int) -> tuple[list[dict], int]:
    """Get all users data for a specific league"""

    memberships: list[UserLeague] = list(UserLeague.query.filter_by(league_id = league_id).all())
    if not memberships:
        return {'error': f'Failed to find memberships for league_id: {str(league_id)}'}, 404
    
    users: list[dict] = []

    for membership in memberships:

        user: User = membership.user

        if not user:
            return {'error': f'Empty user found for league_id: {str(league_id)}'}, 404
        
        budget: float = membership.budget
        points: float = membership.points
        team: Team = Team.query.filter_by(league_id= league_id, user_id = user.id).first()
        team_id = team.id if team else None

        users.append(
            {
                "id": user.id,
                "username": user.username,
                "team_id": team_id,
                "budget": budget,
                "points": points
            }
        )
    
    return users, 200

def join_league(user_id, code) -> tuple[dict, int]:
    
    user: User = User.query.filter_by(id = user_id).first()
    
    if not user:
        return {'error': f'user not found with id: {str(user_id)}'}, 404
    
    league: League = League.query.filter_by(code = code).first()

    if not league:
        return {'error': f'league not found with code: {str(code)}'}, 404
    
    if league.is_user_in_league(user_id):
        return {'message': 'conflict user already in league'}, 409


    membership = UserLeague(user_id= user_id, league_id=league.id, budget=Decimal('10000.00'))

    league.user_memberships.append(membership)

    db.session.add(membership) 
    db.session.commit()

    return {'message': f'User {user.username} successfuly added to league {league.name}', 'league_id': league.id}, 200



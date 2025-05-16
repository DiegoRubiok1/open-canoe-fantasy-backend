from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import leagues_bp
from app.models.league import League
from app.models.user import User
from .controllers import create_league, get_user_leagues, get_users_in_league, join_league

@leagues_bp.route('/create', methods=['POST'])
@jwt_required()
def create():
    """Create a new league endpoint."""
    user_id = int(get_jwt_identity())
    data = request.get_json()
    data['user_id'] = user_id
    result, status_code = create_league(data, user_id)
    return jsonify(result), status_code

@leagues_bp.route('/show', methods=['GET'])
@jwt_required()
def show():
    """Get user leagues endpoint."""
    user_id = int(get_jwt_identity())
    result, status_code = get_user_leagues(user_id)
    return jsonify(result), status_code

@leagues_bp.route('/users/show/<int:league_id>', methods=['GET'])
@jwt_required()
def show_users(league_id: int):
    """List all users and data from a league"""
    
    league: League = League.query.filter_by(id = league_id).first()
    
    if not league:
        return jsonify({'error': f'league not found with id {str(league_id)}'}), 404
    
    result, status = get_users_in_league(league_id)
    return jsonify(result), status

@leagues_bp.route('/join', methods=['POST'])
@jwt_required()
def join():
    """Join to a league"""

    user_id: int = int(get_jwt_identity())

    data = request.get_json()

    if not data:
        return jsonify({'error': 'body must be json'}), 400
    
    code: str = data.get('code', None)

    if not code:
        return jsonify({'error': f'code must not be empty'}), 402
    
    result, status = join_league(user_id, code)

    return jsonify(result), status
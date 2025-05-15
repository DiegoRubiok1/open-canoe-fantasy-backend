from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from .controllers import (
    create_team_user, 
    set_team, 
    get_team_details,
    get_league_teams
)
from . import teams_bp

@teams_bp.route('/create', methods=['POST'])
@jwt_required()
def create_team():
    # Get user ID from token
    user_id = int(get_jwt_identity())
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400
    
    result, status_code = create_team_user(data, user_id)
    return jsonify(result), status_code

@teams_bp.route('/set', methods=['POST'])
@jwt_required()
def set_team_players():
    # Get user ID from token
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400

    team_id = data.get('team_id')
    if not team_id:
        return jsonify({'error': 'Team ID is required'}), 400

    players = data.get('players', [])
    if not isinstance(players, list):
        return jsonify({'error': 'Players must be a list'}), 400

    player_ids = [int(p) for p in players]
    if len(player_ids) != 4:
        return jsonify({'error': 'You must select exactly 4 players'}), 400
    
    result, status_code = set_team(user_id, team_id, player_ids)
    return jsonify(result), status_code

@teams_bp.route('/show/<int:team_id>', methods=['GET'])
@jwt_required()
def show_team(team_id):
    """Get team details with its players and their contract details."""
    user_id = int(get_jwt_identity())
    result, status_code = get_team_details(user_id, team_id)
    return jsonify(result), status_code

@teams_bp.route('/leagues/<int:league_id>/show', methods=['GET'])
@jwt_required()
def list_league_teams(league_id):
    """Get all teams in a specific league."""
    user_id = int(get_jwt_identity())
    result, status_code = get_league_teams(user_id, league_id)
    return jsonify(result), status_code








from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import leagues_bp
from .controllers import create_league, get_user_leagues

@leagues_bp.route('/create', methods=['POST'])
@jwt_required()
def create():
    """Create a new league endpoint."""
    user_id = int(get_jwt_identity())
    data = request.get_json()
    data['user_id'] = user_id
    result, status_code = create_league(data)
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
    #TODO: SHOW USERS IN LEAGUE
    pass
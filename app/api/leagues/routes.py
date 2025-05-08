from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from . import leagues_bp
from .controllers import create_league, get_user_leagues

@leagues_bp.route('/leagues', methods=['POST'])
@jwt_required()
def create():
    # Convert string ID back to int
    user_id = int(get_jwt_identity())
    
    # Verify user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    data['user_id'] = user_id
    
    result, status_code = create_league(data)
    return jsonify(result), status_code

@leagues_bp.route('/leagues', methods=['GET'])
@jwt_required()
def get_leagues():
    # Convert string ID back to int
    user_id = int(get_jwt_identity())
    result, status_code = get_user_leagues(user_id)
    return jsonify(result), status_code
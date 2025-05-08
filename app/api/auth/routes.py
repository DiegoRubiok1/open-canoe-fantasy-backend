from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from . import auth_bp
from .controllers import register_user, authenticate_user
from app.models.user import User


@auth_bp.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({'error': 'Missing JSON in request'}), 400

    data = request.get_json()
    result = register_user(data)

    if result.get('error'):
        return jsonify(result), 400
    
    return jsonify({
        'message': 'Registration successful',
        'user_id': result['user_id']
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({'error': 'Missing JSON in request'}), 400

    data = request.get_json()
    result = authenticate_user(data)
    
    if result.get('error'):
        return jsonify(result), 401
    
    user = result['user']
    # Convert user.id to string for JWT
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'status': user.status
        }
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_user_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(current_user_id)
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'role': user.role,
        'status': user.status
    }), 200
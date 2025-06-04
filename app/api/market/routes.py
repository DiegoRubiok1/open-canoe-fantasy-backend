from . import market_bp
from flask_jwt_extended import jwt_required, get_jwt_identity
from .controllers import show_market, purchase_player, sell_player_market
from app.models.user import User
from flask import request, jsonify

@market_bp.route('/show/<int:league_id>', methods=['GET'])
@jwt_required()
def list_market(league_id: int):
    """
    List players in a specific market for a league.
    
    Args:
        league_id: ID of the league to show market for
    Returns:
        tuple: (response_data, status_code)
    """
    user_id = get_jwt_identity()
    
    user = User.query.get(user_id)
    if not user:
        return {"message": "User not found."}, 404
    
    return show_market(league_id)

@market_bp.route('/purchase', methods=['POST'])
@jwt_required()
def buy_player():
    """
    Purchase a player from the market.
    
    Expects JSON payload with:
        - league_id: ID of the league to purchase from
        - player_id: ID of the player to purchase
    Returns:
        tuple: (response_data, status_code)
    """
    user_id = get_jwt_identity()
    
    if not user_id:
        return {"message": "User not authenticated."}, 401
    
    data = request.get_json()
    league_id = data.get('league_id')
    player_id = data.get('player_id')
    
    if not league_id or not player_id:
        return {"message": "Missing required parameters."}, 400
    
    return purchase_player(league_id, player_id, user_id)   

@market_bp.route('/sell', methods=['POST'])
@jwt_required()
def sell_player():
    """
    Sell a player in the market.
    
    Expects JSON payload with:
        - league_id: ID of the league to sell in
        - player_id: ID of the player to sell
    Returns:
        tuple: (response_data, status_code)
    """
    user_id = get_jwt_identity()
    
    if not user_id:
        return {"message": "User not authenticated."}, 401
    
    return sell_player_market(user_id, request.get_json())
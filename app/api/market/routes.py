from . import market_bp
from flask_jwt_extended import jwt_required, get_jwt_identity
from .controllers import show_market
from app.models.user import User

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


from datetime import datetime
from decimal import Decimal
from typing import Optional
from app.extensions import db
from app.models.player import Player

class Market(db.Model):
    """Market model for the application.
    
    Represents players available for purchase in a specific league's market.
    Tracks availability and pricing information.
    """
    
    __tablename__ = 'market'

    # Primary Keys / Foreign Keys
    league_id = db.Column(db.BigInteger, 
                         db.ForeignKey('leagues.id', ondelete='CASCADE'),
                         primary_key=True)
    player_id = db.Column(db.BigInteger,
                         db.ForeignKey('players.id', ondelete='CASCADE'),
                         primary_key=True)
    
    # Market details
    price = db.Column(db.Numeric(12,2), nullable=False, default=0.0)
    available_from = db.Column(db.DateTime, nullable=False, 
server_default=db.func.current_timestamp())

    # Relationships
    league = db.relationship('League', back_populates='market_entries')
    player = db.relationship('Player', back_populates='market_entries')

    __table_args__ = (
        db.CheckConstraint('price >= 0', name='chk_price'),
        db.Index('idx_market_league_price', 'league_id', 'price'),
        db.Index('idx_market_player_price', 'player_id', 'price')
    )

    def __init__(self, league_id: int, player_id: int, 
                 price: Decimal):
        """Initialize a new market entry."""
        self.league_id = league_id
        self.player_id = player_id
        self.price = price

    def __repr__(self):
        return f'<Market {self.league_id}:{self.player_id}>'

    @property
    def days_listed(self) -> int:
        """Get number of days the player has been listed."""
        return (datetime.utcnow() - self.available_from).days

    @property
    def formatted_price(self) -> str:
        """Get formatted price string."""
        return f"${float(self.price):,.2f}"
        
    @classmethod
    def get_players(cls, league_id: int) -> list[Player]:
        """Get players available in the market for a specific league.
        
        Args:
            league_id: ID of the league to get market players from
            
        Returns:
            List of Player objects available in the market
            Empty list if no players found
        """
        return (
            Player.query
            .join(cls)
            .filter(cls.league_id == league_id)
            .all()
        )

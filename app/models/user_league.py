from datetime import datetime
from decimal import Decimal
from typing import Optional
from app.extensions import db

class UserLeague(db.Model):
    """UserLeague model for the application.
    
    Associates users with leagues and tracks their budget and points.
    Represents the many-to-many relationship between users and leagues
    with additional data.
    """
    
    __tablename__ = "user_leagues"

    # Primary Keys / Foreign Keys with CASCADE
    user_id = db.Column(db.BigInteger, 
                       db.ForeignKey('users.id', ondelete='CASCADE'), 
                       primary_key=True)
    league_id = db.Column(db.BigInteger, 
                         db.ForeignKey('leagues.id', ondelete='CASCADE'), 
                         primary_key=True)
    
    # Member attributes
    budget = db.Column(db.Numeric(12,2), nullable=False, default=1000.00)
    points = db.Column(db.Integer, nullable=False, default=0)
    joined_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', 
                          back_populates='league_memberships')
    league = db.relationship('League', 
                           back_populates='user_memberships')

    def __init__(self, user_id: int, league_id: int, 
                 budget: Optional[Decimal] = Decimal('1000.00')):
        """Initialize a new league membership."""
        self.user_id = user_id
        self.league_id = league_id
        self.budget = budget

    def __repr__(self):
        return f'<UserLeague {self.user_id}:{self.league_id}>'

    @property
    def membership_days(self) -> int:
        """Get days since joining the league."""
        return (datetime.utcnow() - self.joined_at).days

    @property
    def formatted_budget(self) -> str:
        """Get formatted budget string."""
        return f"${float(self.budget):,.2f}"



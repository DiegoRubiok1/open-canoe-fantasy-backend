from app.extensions import db
from datetime import datetime
from decimal import Decimal
from typing import Optional

class TeamPlayer(db.Model):
    """Association model between Teams and Players.
    
    Represents the contract between a player and a team, including:
    - Release clause amount
    - Titular status
    - Contract start date
    """
    
    __tablename__ = 'team_players'

    # Primary Keys / Foreign Keys
    team_id = db.Column(db.BigInteger, db.ForeignKey('teams.id', ondelete='CASCADE'), primary_key=True)
    player_id = db.Column(db.BigInteger, db.ForeignKey('players.id', ondelete='CASCADE'), primary_key=True)
    
    # Contract details
    clause = db.Column(db.Numeric(12,2), nullable=False, default=0.0)  # Added default value
    titular = db.Column(db.Boolean, nullable=False, default=False)
    added_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    team = db.relationship('Team', back_populates='player_associations')
    player = db.relationship('Player', back_populates='team_associations')

    def __init__(self, team_id: int, player_id: int, clause: Decimal, 
                 titular: bool = False):
        """Initialize a new team-player association."""
        self.team_id = team_id
        self.player_id = player_id
        self.clause = clause
        self.titular = titular

    def __repr__(self):
        return f'<TeamPlayer {self.team_id}:{self.player_id}>'

    @property
    def contract_age(self) -> int:
        """Get days since contract started."""
        return (datetime.utcnow() - self.added_at).days

    @property
    def clause_amount(self) -> Decimal:
        """Get formatted clause amount."""
        return Decimal(str(self.clause))
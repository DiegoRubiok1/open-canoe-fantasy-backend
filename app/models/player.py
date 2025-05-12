from app.extensions import db
from datetime import datetime
from typing import Optional, List

class Player(db.Model):
    """Player model for the application."""
    
    __tablename__ = 'players'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    club = db.Column(db.String(100), nullable=False)
    market_price = db.Column(db.Numeric(12, 2), nullable=False, default=0.0)
    points = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    teams = db.relationship('Team', secondary='team_players', back_populates='players', viewonly=True)
    team_associations = db.relationship('TeamPlayer', back_populates='player', cascade='all, delete-orphan')
    market_entries = db.relationship('Market', back_populates='player', cascade='all, delete-orphan')

    __table_args__ = (
        db.Index('idx_players_club', 'club'),
    )

    def __repr__(self):
        return f'<Player {self.name}>'

    @property
    def is_active(self) -> bool:
        """Check if player is active in any team."""
        return any(assoc.titular for assoc in self.team_associations)

    @property
    def current_teams(self) -> list:
        """Get list of teams where player is currently playing."""
        return [assoc.team for assoc in self.team_associations]
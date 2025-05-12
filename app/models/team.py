from app.extensions import db
from datetime import datetime
from typing import List, Optional
from app.models.player import Player

class Team(db.Model):
    """Team model for the application.
    
    Represents a team in a specific league, owned by a user.
    Contains relationships to players through team_players association.
    """
    
    __tablename__ = 'teams'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    league_id = db.Column(db.BigInteger, db.ForeignKey('leagues.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='teams')
    league = db.relationship('League', back_populates='teams')
    players = db.relationship('Player', secondary='team_players',back_populates='teams', viewonly=True)
    player_associations = db.relationship('TeamPlayer', back_populates='team', cascade='all, delete-orphan')

    __table_args__ = (
        db.UniqueConstraint('user_id', 'league_id', 'name', name='_user_league_team_uc'),
        db.Index('idx_teams_user_league', 'user_id', 'league_id'),
    )

    def __repr__(self):
        return f'<Team {self.name}>'

    @property
    def total_points(self) -> int:
        """Calculate total team points from titular players."""
        return sum(
            assoc.player.points 
            for assoc in self.player_associations 
            if assoc.titular
        )

    @property
    def titular_players(self):
        """Get list of titular players."""
        return [
            assoc.player 
            for assoc in self.player_associations 
            if assoc.titular
        ]
    
    @property
    def all_players(self) -> List['Player']:
        """Get all players in the team."""
        return [
            assoc.player 
            for assoc in self.player_associations
        ]
    
    @property
    def non_titular_players(self) -> List['Player']:
        """Get list of non-titular players."""
        return [
            assoc.player 
            for assoc in self.player_associations 
            if not assoc.titular
        ]

    @classmethod
    def get_user_players_in_league(cls, user_id: int, league_id: int) -> List['Player']:
        """Get all players owned by a user in a specific league.
        
        Args:
            user_id: The ID of the user
            league_id: The ID of the league
            
        Returns:
            List of Player objects owned by the user in the league
        """
        # Get user's team in the league
        team = cls.query.filter_by(
            user_id=user_id,
            league_id=league_id
        ).first()
        
        return team.all_players if team else []

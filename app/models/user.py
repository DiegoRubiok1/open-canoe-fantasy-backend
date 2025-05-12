"""User model."""
from datetime import datetime
from app.extensions import db
from app.models.user_league import UserLeague
from app.models.team import Team
from app.models.team_player import TeamPlayer
from sqlalchemy.sql import expression


class User(db.Model):
    """User model for the application."""
    
    __tablename__ = "users"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), nullable=False, default='user')
    status = db.Column(
        db.String(20), 
        nullable=False, 
        default='active',
        info={'check': "status IN ('active', 'suspended', 'deleted')"}
    )
    email_verified_at = db.Column(db.DateTime, nullable=True)
    last_login_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    __table_args__ = (
        db.Index('idx_users_email', 'email'),
        db.Index('idx_users_username', 'username')
    )

    # Relationships
    league_memberships = db.relationship('UserLeague', back_populates='user', cascade='all, delete-orphan')
    
    leagues = db.relationship('League',
                            secondary='user_leagues',
                            back_populates='users',
                            viewonly=True,
                            overlaps="league_memberships,user")
    
    teams = db.relationship('Team', back_populates='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    @property
    def is_active(self):
        return self.status == 'active' and self.deleted_at is None
    
    def get_budget(self, league_id: int) -> float:
        """Get the user's budget for a specific league."""
        user_league = UserLeague.query.filter_by(
            user_id=self.id,
            league_id=league_id
        ).first()
        return float(user_league.budget) if user_league else 0.0
    
    def get_points(self, league_id: int) -> int:
        """Get the user's points for a specific league."""
        user_league = UserLeague.query.filter_by(
            user_id=self.id,
            league_id=league_id
        ).first()
        return user_league.points if user_league else 0
    
    def get_team(self, league_id: int, player_associations = False) -> list:
        """Get the user's team for a specific league. 
        If player_associations is True, return player associations instead of players.
        Returns [] if no team is found.
        """
        team: Team = Team.query.filter_by(user_id = self.id, league_id = league_id).first()
        
        if not team:
            return []
        
        players = team.players
        associations: list[TeamPlayer] = team.player_associations

        if player_associations:
            return associations
        return players






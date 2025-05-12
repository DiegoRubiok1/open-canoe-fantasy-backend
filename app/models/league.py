from datetime import datetime
from app.extensions import db

class League(db.Model):
    """League model for the application."""

    __tablename__ = "leagues"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    user_memberships = db.relationship('UserLeague',
                                     back_populates='league',
                                     cascade='all, delete-orphan',
                                     overlaps="leagues")
    
    users = db.relationship('User',
                          secondary='user_leagues',
                          back_populates='leagues',
                          viewonly=True)
    
    teams = db.relationship('Team',back_populates='league', cascade='all, delete-orphan')

    market_entries = db.relationship('Market', back_populates='league', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<League {self.name}>'
    
    @property
    def is_active(self):
        """Check if league is not soft-deleted."""
        return self.deleted_at is None

    @property
    def member_count(self):
        """Get number of users in league."""
        return len(self.user_memberships)
    
    def is_user_in_league(self, user_id):
        """Check if a user is a member of the league."""
        return any(user.id == user_id for user in self.users)

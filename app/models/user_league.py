from datetime import datetime
from app.extensions import db

class UserLeague(db.Model):
    """UserLeague model for the application."""

    __tablename__ = "user_leagues"

    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), primary_key=True)
    league_id = db.Column(db.BigInteger, db.ForeignKey('leagues.id'), primary_key=True)
    budget = db.Column(db.Numeric(12,2), nullable=False, default=1000)
    points = db.Column(db.Integer, nullable=False, default=0)
    joined_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='league_memberships')
    league = db.relationship('League', back_populates='user_memberships')
    
    def __repr__(self):
        return f'<UserLeague {self.user_id}:{self.league_id}>'



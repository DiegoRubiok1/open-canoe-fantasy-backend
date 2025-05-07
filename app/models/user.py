"""User model."""
from datetime import datetime
from app.extensions import db

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
    status = db.Column(db.String(20), nullable=False, default='active')
    email_verified_at = db.Column(db.DateTime, nullable=True)
    last_login_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    # Relationships TODO: IMPLEMENT 'LEAGUE' AND 'TEAM' MODELS
    #leagues = db.relationship('League', secondary='user_leagues', back_populates='users')
    #teams = db.relationship('Team', back_populates='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    @property
    def is_active(self):
        return self.status == 'active' and self.deleted_at is None
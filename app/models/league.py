from app.extensions import db



class League(db.Model):
    """League model for the application."""

    __tablename__ = "leagues"

    id  = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    user_memberships = db.relationship('UserLeague', back_populates='league')
    users = db.relationship('User', secondary='user_leagues', back_populates='leagues', viewonly=True)

    def __repr__(self):
        return f'<League {self.name}>'
    
    @property
    def is_active(self):
        return self.deleted_at is None


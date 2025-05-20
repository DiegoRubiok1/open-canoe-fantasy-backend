from flask import Flask
from .config import config
from .extensions import db, migrate, jwt, bcrypt, cache
from .api.auth import auth_bp
from .api.leagues import leagues_bp
from .api.teams import teams_bp

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Load config
    app.config.from_object(config[config_name or 'default'])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    
    # Register blueprints with proper prefixes
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(leagues_bp, url_prefix='/api/leagues')
    app.register_blueprint(teams_bp, url_prefix='/api/teams')
    
    return app

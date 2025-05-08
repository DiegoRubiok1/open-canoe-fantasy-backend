from .extensions import db, migrate, jwt, ma, bcrypt, cache
from flask import Flask
from .config import config
from .api.auth import auth_bp  # noqa
from .api.leagues import leagues_bp  # noqa


def create_app(config_name=None):
    app = Flask(__name__)
    app.config.from_object(config[config_name or 'default'])

    # initialize all extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    
    app.register_blueprint(leagues_bp, url_prefix='/api/leagues', name='leagues')
    app.register_blueprint(auth_bp, url_prefix='/api/auth', name='auth')
    return app

from app import create_app
from app.extensions import db
from dotenv import load_dotenv
import os

from app.models.user import User
from app.models.league import League
from app.models.team import Team
from app.models.player import Player
from app.models.team_player import TeamPlayer
from app.models.user_league import UserLeague

load_dotenv(override=True)

def run():
    # Create the Flask application
    app = create_app(config_name='default')
    print(f"Database URI: {os.getenv('DATABASE_URI')} actual value: {app.config['SQLALCHEMY_DATABASE_URI']}")

    # Create the database tables
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully!")

        except Exception as e:
            print(f"Error creating tables: {e}")

    # Run the application
    app.run(debug=True)

if __name__ == '__main__':
    run()
# This script is the entry point for running the Flask application.
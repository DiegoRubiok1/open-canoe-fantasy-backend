from app.__init__ import create_app
from app.extensions import db

def run():
    # Create the Flask application
    app = create_app()

    # Create the database tables
    with app.app_context():
        db.create_all()

    # Run the application
    app.run(debug=True)

if __name__ == '__main__':
    run()
# This script is the entry point for running the Flask application.
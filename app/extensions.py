from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_caching import Cache

# database ORM
db = SQLAlchemy()

# alembic migrations
migrate = Migrate()

# JWT support (tokens for login)
jwt = JWTManager()

# request/response serialization & validation
ma = Marshmallow()

# password hashing
bcrypt = Bcrypt()

# optional: simple caching (Redis, in‑memory, etc.)
cache = Cache()


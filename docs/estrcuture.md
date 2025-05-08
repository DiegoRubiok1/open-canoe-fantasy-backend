# Flask Backend Project Structure for LaLiga Fantasy Clone

This document outlines the folder and file structure for a Flask backend designed to replicate LaLiga Fantasy. It follows the **Application Factory** pattern and **Blueprints** for modularity, with support for migrations, testing, and Docker deployment.

```bash
fantasy-backend/
├── app/
│   ├── __init__.py            # Application factory
│   ├── config.py              # Configuration classes (Dev, Test, Prod)
│   ├── extensions.py          # Initialization of extensions (DB, Migrate, JWT)
│   ├── models/                # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py            # User model
│   │   ├── player.py          # Player model
│   │   ├── team.py            # Team model
│   │   ├── match.py           # Match model
│   │   └── fantasy_team.py    # Fantasy team model
│   ├── api/                   # API Blueprints
│   │   ├── __init__.py
│   │   ├── auth/              # Authentication (login, register)
│   │   │   ├── routes.py
│   │   │   └── schemas.py
│   │   ├── users/             # User endpoints
│   │   │   ├── routes.py
│   │   │   └── schemas.py
│   │   ├── players/           # Player endpoints
│   │   │   ├── routes.py
│   │   │   └── schemas.py
│   │   ├── teams/             # Team endpoints
│   │   │   ├── routes.py
│   │   │   └── schemas.py
│   │   └── fantasy/           # Fantasy logic (lineups, scores)
│   │       ├── routes.py
│   │       └── schemas.py
│   ├── services/              # Business logic services
│   │   ├── auth_service.py
│   │   ├── player_service.py
│   │   └── fantasy_service.py
│   └── utils/                 # Helpers and validators
│       ├── helpers.py
│       └── validators.py
│
├── sql/                       # SQL scripts for DB initialization and seeding
│   ├── init_db.sql            # Create database and tables
│   └── seed_data.sql          # Insert static data (players, teams)
│
├── migrations/                # Alembic/Flask-Migrate versioning folder
│
├── tests/                     # Unit and integration tests (pytest)
│   ├── conftest.py            # Fixtures (app, client, in-memory DB)
│   ├── test_auth.py
│   ├── test_players.py
│   └── test_fantasy.py
│
├── .env                       # Environment variables (should not be committed)
├── .flaskenv                  # FLASK_APP, FLASK_ENV setup
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker image configuration
├── docker-compose.yml         # Compose services (Postgres, Redis, etc.)
└── run.py                     # App entry point
```

---

## Component Overview

### 1. `app/__init__.py`

* Implements the **Application Factory** pattern with `create_app()`.
* Loads configuration, initializes extensions, and registers Blueprints.

### 2. `app/config.py`

Defines configuration classes:

* `Config`: base config with shared values (e.g., SECRET\_KEY, SQLALCHEMY\_DATABASE\_URI).
* `DevelopmentConfig`, `TestingConfig`, `ProductionConfig` extend `Config`.

### 3. `app/extensions.py`

Defines and initializes extensions without binding them immediately to the app:

```python
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
```

### 4. `app/models/`

Each file defines a SQLAlchemy `db.Model`:

* Models for users, players, matches, teams, and fantasy teams.
* Includes methods such as stats calculations or relationships.

### 5. `app/api/`

Domain-based Blueprint structure:

* `routes.py`: defines REST endpoints (GET, POST, PUT, DELETE).
* `controllers.py`: Logic and functions for routes.

### 6. `app/services/`

Encapsulates business logic separate from API routes:

* Fantasy score calculation.
* Transfers and drafting logic.
* Auth workflows and token generation.

### 7. `app/utils/`

Utility and helper functions:

* Custom validators.
* Date formatting, stats helpers, etc.

### 8. `sql/`

Standalone SQL scripts:

* **`init_db.sql`**: initializes database and tables using DDL.
* **`seed_data.sql`**: seeds initial data like players, teams, and leagues.

### 9. `migrations/`

Directory managed by Alembic:

* Tracks schema changes.
* Supports `flask db migrate` and `flask db upgrade`.

### 10. `tests/`

Organized pytest structure:

* `conftest.py`: fixtures for test app and database.
* Unit/integration tests for auth, player routes, and fantasy features.

### 11. Root Files

* **`.env`** and **`.flaskenv`**: environment-specific config.
* **`requirements.txt`**: all Python packages used.
* **`run.py`**: runs the app using `create_app()`.

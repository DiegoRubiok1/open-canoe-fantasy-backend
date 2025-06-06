# Flask Backend Project Structure for Open Canoe Fantasy

This document outlines the folder and file structure. It follows the **Application Factory** pattern and **Blueprints** for modularity.

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
│   │   ├── league.py          # League model
│   │   └── user_laegue.py     # Relation model
│   │   └── team_player.py     # Relation model
│   │   └── market.py          # Market model
│   ├── api/                   # API Blueprints
│   │   ├── __init__.py
│   │   ├── auth/              # Authentication (login, register)
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── controllers.py
│   │   ├── users/             # User endpoints
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── controllers.py
│   │   ├── players/           # Player endpoints
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── controllers.py
│   │   ├── teams/             # Team endpoints
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── controllers.py
│   │   └── market/           # Fantasy logic (lineups, scores)
│   │       ├── __init__.py
│   │       ├── routes.py
│   │       └── controllers.py
│   ├── services/              # Business logic services
│   │   └── market_service.py
│   └── utils/                 # Helpers and validators
│ 
├── sql/                       # SQL scripts for DB initialization and seeding
│   ├── init_db.sql            # Create database and tables
│   └── seed_data.sql          # Insert static data (players, teams)
│
├── tests/                     # Unit and integration tests (pytest)
│
├── .env                       # Environment variables (should not be committed)
├── requirements.txt           # Python dependencies
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

* Models for users, players, leagues, teams, and more.
* Includes methods such as stats calculations or relationships.

### 5. `app/api/`

Domain-based Blueprint structure:

* `routes.py`: defines REST endpoints (GET, POST, PUT, DELETE).
* `controllers.py`: Logic and functions for routes.

### 6. `app/services/`

Encapsulates business logic separate from API routes:

* Fantasy score calculation.
* Transfers and drafting logic.
* Market logic and functions.

### 7. `app/utils/` 

Utility and auxiliar functions.

### 8. `sql/`

Standalone SQL scripts:

* **`init_db.sql`**: initializes database and tables using DDL.
* **`seed_data.sql`**: seeds initial data like players.

### 9. `migrations/`

Directory managed by Alembic: (not implemented)

* Tracks schema changes.
* Supports `flask db migrate` and `flask db upgrade`.

### 10. `tests/`

Diferent tests for endpoints. 

### 11. Root Files

* **`.env`** and **`.flaskenv`**: environment-specific config.
* **`requirements.txt`**: all Python packages used.
* **`run.py`**: runs the app using `create_app()`.

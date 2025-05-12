# Open Canoe Fantasy

A fantasy canoe backend API built with Flask and SQLAlchemy, inspired by popular fantasy sport games.

## Features

- **User Management**: Registration, authentication using JWT
- **League System**: Create and join leagues with unique codes
- **Team Management**: Create teams and manage player rosters
- **Market System**: Dynamic player market with price fluctuation
- **Points System**: Automatic point calculation based on player performance

## Tech Stack

- Python 3.12+
- Flask + Extensions
  - Flask-SQLAlchemy (ORM)
  - Flask-JWT-Extended (Authentication)
  - Flask-Migrate (Database migrations)
  - Flask-Marshmallow (Serialization)
- MySQL 8.0+

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/open-canoe-fantasy.git
cd open-canoe-fantasy
```

2. Create virtual environment:
```bash
python -m venv env
source env/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up MySQL database:
```bash
mysql -u root -p < sql/init_db.sql
```

5. Run the application:
```bash
python run.py
```

## API Documentation

- [Authentication](docs/api_docs/auth.md)
- [Leagues](docs/api_docs/leagues.md)
- [Teams](docs/api_docs/teams.md)
- [Market](docs/api_docs/market.md)

## Project Structure

```
open-canoe-fantasy/
├── app/                    # Application package
│   ├── api/               # API endpoints
│   ├── models/            # Database models
│   ├── services/          # Business logic
│   └── extensions.py      # Flask extensions
├── docs/                  # Documentation
├── sql/                   # SQL scripts
├── tests/                 # Test suite
└── run.py                # Application entry point
```
Check complete estructure in [structure](/docs/structure.md)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

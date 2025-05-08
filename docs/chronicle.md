# Project Chronicle

## May 7, 2025

Today I've built the project structure. I had no idea on how to design the architecture, so I got guidance from ChatGPT. After that, I used a database schema to build the SQL script and deployed it to MySQL.

**Completed Tasks:**

- [x] Set up `config.py` file
- [x] Configure `app/__init__.py` with `create_app()`
- [x] Set up `run.py` configuration
- [x] Create user models in `/app/models`
- [x] Implement login feature at `app/api/auth`
- [x] Authentication tests with curl

**Next Tasks:**
- [x] League managment:
    - [x] Implement models (league) and its relations following `docs/database_eschema.pdf`
    - [x] Implement endpoints with routes at following `docs/estructure.md`
    - [x] Test features with curl
    - [x] Document API endpoints in `docs/api_docs/leagues.md`

## May 8, 2025

Today I implemented and tested the leagues management features.

**Completed Tasks:**
- [x] Implemented League model with relationships
- [x] Created UserLeague association model
- [x] Added league creation endpoint
- [x] Added get user leagues endpoint
- [x] Created test script for API testing
- [x] Fixed JWT identity handling
- [x] Documented API endpoints

**Next Tasks:**
- [ ] Teams management:
    - [ ] Implement Team model
    - [ ] Create team creation endpoint
    - [ ] Add team listing endpoint
    - [ ] Document team endpoints

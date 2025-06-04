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
- [x] Document new estructure
- [ ] Teams management:
    - [x] Implement Team and Player model
    - [x] Modify `team_players` adding to field: `titular` and `clause`  
    - [x] Create team creation endpoint
    - [x] Add team listing endpoint
    - [x] Test team endpoints
    - [x] Document team endpoints

## May 9, 2025

Today I implemented team management features and created test scripts.

**Completed Tasks:**
- [x] Created TeamPlayer association model
- [x] Implemented team creation endpoint
- [x] Added player assignment to teams
- [x] Created team listing endpoints
- [x] Created test script for team endpoints

## May 11, 2025

Today I worked on fixing relationship issues and implementing the market feature.

**Completed Tasks:**
- [x] Fixed SQLAlchemy relationship warnings
- [x] Added overlaps parameter to handle relationship conflicts
- [x] Implemented Market model with proper constraints
- [x] Added market initialization on league creation
- [x] Created market update service
- [x] Fixed Team-Player associations
- [x] Updated API documentation

## May 12, 2025

Today I focused on fixing critical bugs and improving documentation.

**Completed Tasks:**
- [x] Fixed market logic implementation
- [x] Improved league creation endpoint
- [x] Refined team and player models
- [x] Updated README.md
- [x] Updated requirements documentation

## May 14-15, 2025

Focused on documentation and API testing.

**Completed Tasks:**
- [x] Updated API documentation
- [x] Tested and documented team endpoints
- [x] Refined API documentation structure

## May 16, 2025

Implemented new league features and improved documentation.

**Completed Tasks:**
- [x] Added league join functionality
- [x] Implemented endpoint to show users in a league
- [x] Updated README.md with new features
- [x] Enhanced documentation coverage

## May 20, 2025

Major code refactoring session.

**Completed Tasks:**
- [x] Removed unnecessary code
- [x] Reorganized codebase structure
- [x] Improved code organization
- [x] Cleaned up redundant files

## June 4, 2025

Today I focused on fixing market functionality and improving documentation.

**Completed Tasks:**
- [x] Implemented market endpoints and features
- [x] Created comprehensive market API documentation
- [x] Improved error handling in market controllers
- [x] Fixed price calculation logic using Decimal instead of float

**Next Tasks:**
- [ ] Make a demo frontend with kivy.




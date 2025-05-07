# Project Chronicle

## May 7, 2025

Today I've built the project structure. I had no idea on how to design the architecture, so I got guidance from ChatGPT. After that, I used a database schema to build the SQL script and deployed it to MySQL.

**Completed Tasks:**

- [x] Set up `config.py` file
- [x] Configure `app/__init__.py` with `create_app()`
- [x] Set up `run.py` configuration
- [x] Create user models in `/app/models`
- [x] Implement login feature at `app/api/auth`
- [ ] Post man tests

**Next Tasks:**
- [ ] League managment:
    - [ ] Implement models (league) and its relations following `docs/database_eschema.pdf`
    - [ ] Implement endpoints with routes at following `docs/estructure.md`
    - [ ] Test features with postman

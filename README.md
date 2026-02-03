# Cs491-09S2026G2-FinalTake
Capstone Project for CSUF computers science. Social media/media reviewing app. Following the designs left from a previous group in a previous semester. 

Architecture/Design Docs:
https://docs.google.com/document/d/1gknaDwY_yAnbjHSUbM4AaqW4XNb5sO8mFJNR-zJ8-94/edit?usp=sharing


## File Structure

# FinalTake Repository Structure

This project is organized as a simple, industry-ready monorepo with a frontend client, backend server, and database resources.

## Folder Tree

```text
finaltake/
├─ README.md
├─ .gitignore
├─ .env.example
├─ docker-compose.yml
├─ .github/
│  └─ workflows/
│     └─ ci.yml
│
├─ docs/
│  ├─ overview.md
│  ├─ architecture.md
│  ├─ api.md
│  └─ database.md
│
├─ client/
│  ├─ package.json
│  ├─ public/
│  └─ src/
│     ├─ app/                 # routing + app bootstrap
│     ├─ pages/               # screens (Login, Search, Media, Profile...)
│     ├─ components/          # reusable UI pieces (stars, cards, modals)
│     ├─ services/            # API + realtime client (fetch/websocket)
│     ├─ state/               # global state (auth user, feed, tags)
│     ├─ styles/              # global CSS/theme
│     └─ utils/               # helpers (format dates, debounce, etc.)
│
├─ server/
│  ├─ requirements.txt
│  └─ app/
│     ├─ __init__.py          # create app + register routes
│     ├─ config.py            # env config + settings
│     ├─ routes/              # Controllers (REST endpoints)
│     ├─ services/            # Business logic (use cases)
│     ├─ models/              # Data models (User, Media, Review...)
│     ├─ db/                  # DB access + migrations/seed
│     ├─ realtime/            # websocket/SSE for friend feed
│     └─ tests/               # unit + integration tests
│
└─ database/
   ├─ migrations/             # schema changes (Alembic/etc.)
   ├─ seed/                   # sample data scripts
   └─ schema.sql              # optional initial schema


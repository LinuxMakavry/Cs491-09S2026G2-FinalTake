# Cs491-09S2026G2-FinalTake
Capstone Project for CSUF computers science. Social media/media reviewing app. Following the designs left from a previous group in a previous semester. 

Architecture/Design Docs:
https://docs.google.com/document/d/1gknaDwY_yAnbjHSUbM4AaqW4XNb5sO8mFJNR-zJ8-94/edit?usp=sharing

## File Structure

# FinalTake Repository Structure

This project is organized as a simple, industry-ready monorepo with a frontend client, backend server, and database resources.

# Instructions On How To Run
1. Run the following:
- make install
*this is for installing dependencies*
2. Run 
- make dev
3. ctrl+click on link
4. boom, you're in
5. To stop server
- ctrl+c
## Linting

```text
cd client
npm run lint
```

## Continous Integration
This project uses GitHub Actions located in the ci.yaml file
in .github/workflows/ci.yml

## What CI Currently Does

# Client job
- Installs dependencies

- Runs ESLint

- Optionally runs tests/build

# Server Job
- Installs Python dependencies

- Runs Ruff lint

- Runs Pytest (when tests exist)


***Note: Server CI may be partially skipped until backend implementation is complete.***

## Docker setup (In Progress)

## Project Structure
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
│  ├─ package-lock.json
│  ├─ public/
│  └─ src/
│     ├─ app/
│     ├─ pages/
│     ├─ components/
│     ├─ services/
│     ├─ state/
│     ├─ styles/
│     └─ utils/
│
├─ server/
│  ├─ requirements.txt
│  └─ app/
│     ├─ __init__.py
│     ├─ config.py
│     ├─ routes/
│     ├─ services/
│     ├─ models/
│     ├─ db/
│     ├─ realtime/
│     └─ tests/
│
└─ database/
   ├─ migrations/
   ├─ seed/
   └─ schema.sql
```

# Cs491-09S2026G2-FinalTake
Capstone Project for CSUF computers science. Social media/media reviewing app. Following the designs left from a previous group in a previous semester. 

Architecture/Design Docs:
https://docs.google.com/document/d/1gknaDwY_yAnbjHSUbM4AaqW4XNb5sO8mFJNR-zJ8-94/edit?usp=sharing


## File Structure

# FinalTake Repository Structure

This project is organized as a simple, industry-ready monorepo with a frontend client, backend server, and database resources.

# Instructions On How To Run
(This will be for Visual Studio code, as that is what I use)

1. [ IMPORTANT ] Ensure you have Node.js installed (You can check by opening the command prompt and typing "node --version". The version will display if you have it, otherwise, download it at https://nodejs.org/en)

2. Open a new terminal

3. On the top right of the terminal, look for the "⌄" symbol, right next to the plus symbol beside "powershell"

4. Click that, and select "Command Prompt"

5. Type "cd client" into the terminal
(This is assuming you are currently located somewhere like: C:\Users\yourName\Documents\Cs491-09S2026G2-FinalTake>)

6. Type "npm install" into the terminal

7. Type "npm run dev" into the terminal

8. Ctrl + left click on "http://localhost:5173/" to visit the site

9. When done, Press Ctrl + C in the terminal to terminate the process

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
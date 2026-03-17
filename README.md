# Cs491-09S2026G2-FinalTake
Capstone Project for CSUF computers science. Social media/media reviewing app. Following the designs left from a previous group in a previous semester. 

Architecture/Design Docs:
https://docs.google.com/document/d/1gknaDwY_yAnbjHSUbM4AaqW4XNb5sO8mFJNR-zJ8-94/edit?usp=sharing

## File Structure

# FinalTake Repository Structure

This project is organized as a simple, industry-ready monorepo with a frontend client, backend server, and database resources.

# Getting Started

## Prerequisites
1. **Node.js** v20+ - verify with `node --version` (download from https://nodejs.org/)
2. **Python** v3.10+ - verify with `python --version` (download from https://www.python.org/)
3. **TMDB API Key** (sign up at https://www.themoviedb.org/settings/api)

## Quick Start (using Makefile)
1. Run `make install` to install all dependencies
2. Run `make dev` to start both servers
3. Ctrl+click the link to open the app
4. Press `Ctrl+C` to stop

## Manual Setup

### Backend Setup (Terminal 1)

1. Open PowerShell in the project root directory

2. Create and activate virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
   (You should see `(venv)` at the start of your terminal prompt)

3. Navigate to the server directory:
   ```powershell
   cd server
   ```

4. Install Python dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the `server/` directory and add:
   ```
   TMDB_API_KEY=your_api_key_here
   FLASK_DEBUG=True
   ```

6. Run the backend server:
   ```powershell
   python run.py
   ```
   The server starts on `http://localhost:5000`

### Frontend Setup (Terminal 2)

1. Open a new PowerShell terminal in the project root directory

2. Navigate to the client directory:
   ```powershell
   cd client
   ```

3. Install Node dependencies:
   ```powershell
   npm install
   ```

4. Start the development server:
   ```powershell
   npm run dev
   ```
   The frontend starts on `http://localhost:5173`

5. Ctrl + click on `http://localhost:5173/` to open the site in your browser

6. When done, press `Ctrl + C` in each terminal to stop the servers

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

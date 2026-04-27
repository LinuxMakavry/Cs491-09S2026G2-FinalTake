# FinalTake Makefile (root)
# Monorepo helper for:
# - client/ (Vite + React)
# - server/ (Python)
#
# Quick start:
#   make install
#   make lint
#   make test
#   make build
#   make dev        # client dev server
#   make run        # backend server (python -m app)

# IMPORTANT:
# In Make, SHELL must be a *single executable path* (no spaces).
# Use /bin/bash (common on Linux).

SHELL := /bin/bash
.ONESHELL:
.SHELLFLAGS := -euo pipefail -c

.DEFAULT_GOAL := help

# -------- Paths --------
CLIENT_DIR := client
SERVER_DIR := server
VENV_DIR   := $(SERVER_DIR)/.venv
CLIENT_NODE_MODULES := $(CLIENT_DIR)/node_modules

# -------- Tooling --------
PYTHON ?= python3
PIP    := $(VENV_DIR)/bin/pip
PYTEST := $(VENV_DIR)/bin/pytest
RUFF   := $(VENV_DIR)/bin/ruff

NPM_INSTALL_CMD := npm install
ifneq ("$(wildcard $(CLIENT_DIR)/package-lock.json)","")
  NPM_INSTALL_CMD := npm ci
endif

# -------- Help --------
.PHONY: help
help: ## Show this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nTargets:\n"} /^[a-zA-Z0-9_\/-]+:.*##/ {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2} END {printf "\n"}' $(MAKEFILE_LIST)

.PHONY: info
info: ## Print detected toolchain info
	@echo "Client dir:        $(CLIENT_DIR)"
	@echo "Server dir:        $(SERVER_DIR)"
	@echo "Python:            $(PYTHON)"
	@echo "Venv:              $(VENV_DIR)"
	@echo "NPM install:       $(NPM_INSTALL_CMD)"
	@echo "Shell:             $(SHELL)"
	@if [[ -d "$(CLIENT_NODE_MODULES)" ]]; then echo "Client node_modules: present"; else echo "Client node_modules: MISSING"; fi

# ---------------------------------------------------------------------
# General commands (aliases)
# ---------------------------------------------------------------------
.PHONY: install build lint test dev run fmt clean

install: client-install server-install ## Install dependencies for both client + server

build: client-build ## Build the project (client build)

lint: client-lint server-lint ## Lint both client + server

test: client-test server-test ## Run tests for both (client test is optional)

dev: client-dev ## Run dev server (defaults to client)

run: server-run ## Run backend locally (python -m app)

fmt: client-fmt server-fmt ## Format code (client prettier if available; server ruff format)

# -------- Client (Node) --------
.PHONY: client-ensure client-install client-dev client-build client-preview client-lint client-test client-fmt

client-ensure: ## Ensure client deps are installed (auto-installs if vitest missing)
	if [[ ! -d "$(CLIENT_NODE_MODULES)" ]] || [[ ! -x "$(CLIENT_DIR)/node_modules/.bin/vitest" ]]; then
		echo "Client deps missing (node_modules or vitest not found) -> running 'make client-install'..."
		$(MAKE) client-install
	fi

client-install: ## Install client dependencies (npm ci / npm install)
	cd $(CLIENT_DIR)
	$(NPM_INSTALL_CMD)

client-dev: client-ensure ## Run Vite dev server (client)
	cd $(CLIENT_DIR)
	npm run dev

client-build: client-ensure ## Build client for production (client)
	cd $(CLIENT_DIR)
	npm run build

client-preview: client-ensure ## Preview built client locally (client)
	cd $(CLIENT_DIR)
	npm run preview

client-lint: client-ensure ## Run ESLint (client)
	cd $(CLIENT_DIR)
	npm run lint

client-test: client-ensure ## Run client tests IF the project defines them (npm run test --if-present)
	cd $(CLIENT_DIR)
	npm run test --if-present

client-fmt: client-ensure ## Format client IF prettier exists (npm run format --if-present)
	cd $(CLIENT_DIR)
	npm run format --if-present

# -------- Server (Python) --------
.PHONY: server-venv server-install server-run server-lint server-test server-fmt

server-venv: ## Create Python virtual environment at server/.venv
	@if [[ ! -d "$(VENV_DIR)" ]]; then
		$(PYTHON) -m venv "$(VENV_DIR)"
	fi
	@"$(PIP)" --version >/dev/null

server-install: server-venv ## Install server deps (requirements.txt if non-empty) + dev tools (ruff, pytest)
	cd $(SERVER_DIR)
	../$(PIP) install -U pip setuptools wheel
	# Dev tools used by CI
	../$(PIP) install -U ruff pytest
	# Install app deps only if requirements.txt is non-empty
	if [[ -f "requirements.txt" ]] && [[ -s "requirements.txt" ]]; then
		../$(PIP) install -r requirements.txt
	else
		echo "requirements.txt is empty; skipping app deps install."
	fi

server-run: server-install ## Run the Python server (matches server/dockerfile CMD)
	cd $(SERVER_DIR)
	../$(VENV_DIR)/bin/python -m app

server-lint: server-install ## Lint Python with ruff
	cd $(SERVER_DIR)
	../$(RUFF) check .

server-test: server-install ## Run pytest (server)
	cd $(SERVER_DIR)
	../$(PYTEST) -q

server-fmt: server-install ## Format Python with ruff formatter
	cd $(SERVER_DIR)
	../$(RUFF) format .

# -------- Docker (server) --------
.PHONY: docker-build-server docker-run-server
docker-build-server: ## Build server Docker image (uses server/dockerfile)
	docker build -f $(SERVER_DIR)/dockerfile -t finaltake-server:local $(SERVER_DIR)

docker-run-server: ## Run server Docker image (maps 5173:5173 per Dockerfile EXPOSE)
	docker run --rm -p 5173:5173 finaltake-server:local

# -------- Cleanup --------
clean: ## Remove build artifacts + Python virtualenv + client node_modules
	rm -rf "$(VENV_DIR)"
	rm -rf "$(CLIENT_DIR)/dist"
	rm -rf "$(CLIENT_NODE_MODULES)"
	find "$(SERVER_DIR)" -type d -name "__pycache__" -prune -exec rm -rf {} +
	find "$(SERVER_DIR)" -type f -name "*.pyc" -delete

# ----------------------------------------------------------------------
# Templates / sources used (for transparency):
# - GNU Make manual (targets, .PHONY, default goal, recipe behavior)
# - Self-documenting help target pattern (awk-based) commonly used in OSS Makefiles
# - npm documentation for `npm ci` vs `npm install` and `--if-present`
# - Python documentation for `python -m venv`
# - Ruff documentation for `ruff check` and `ruff format`
# ----------------------------------------------------------------------

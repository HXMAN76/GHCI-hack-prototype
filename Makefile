.PHONY: help install dev test lint format clean docker-up docker-down

help:
	@echo "VoiceBanker Development Commands"
	@echo "=================================="
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make install          Install all dependencies (Python + Node)"
	@echo "  make install-python   Install Python dependencies only"
	@echo "  make install-frontend Install frontend dependencies only"
	@echo ""
	@echo "Development:"
	@echo "  make dev              Start backend and frontend (local mode)"
	@echo "  make backend          Start FastAPI backend only"
	@echo "  make frontend         Start React frontend only"
	@echo "  make rasa             Run Rasa NLU server"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  make test             Run all tests"
	@echo "  make test-backend     Run backend tests only"
	@echo "  make test-coverage    Run tests with coverage report"
	@echo "  make lint             Check code style (Python + JS)"
	@echo "  make format           Auto-format code (Python + JS)"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-up        Start services with Docker Compose"
	@echo "  make docker-down      Stop Docker services"
	@echo "  make docker-logs      View Docker logs"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean            Remove cache and build files"
	@echo "  make db-reset         Reset PostgreSQL database (⚠️ deletes data)"
	@echo ""

# Installation
install: install-python install-frontend
	@echo "✓ All dependencies installed"

install-python:
	pip install -r requirements.txt

install-frontend:
	cd frontend && npm install

# Development
dev:
	@echo "Starting VoiceBanker (backend + frontend)..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:3000"
	@echo ""
	@echo "Run in separate terminals:"
	@echo "  Terminal 1: make backend"
	@echo "  Terminal 2: make frontend"

backend:
	uvicorn backend.main:app --reload

frontend:
	cd frontend && npm start

rasa:
	cd backend/nlu && rasa run

# Testing
test:
	pytest -v

test-backend:
	pytest tests/ -v --tb=short

test-coverage:
	pytest --cov=backend tests/ --cov-report=html --cov-report=term
	@echo "Coverage report: htmlcov/index.html"

# Linting & Formatting
lint:
	@echo "Checking Python style..."
	black --check backend/ tests/
	flake8 backend/ tests/
	@echo "Checking JavaScript style..."
	cd frontend && npm run lint 2>/dev/null || echo "⚠️ JS linter not configured"

format:
	@echo "Formatting Python..."
	black backend/ tests/
	isort backend/ tests/
	@echo "Formatting JavaScript..."
	cd frontend && npx prettier --write src/ 2>/dev/null || echo "⚠️ Prettier not installed"
	@echo "✓ Code formatted"

# Docker
docker-up:
	docker-compose up --build

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

# Utilities
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/ .coverage htmlcov/ dist/ build/ *.egg-info/
	cd frontend && rm -rf node_modules/ build/ .eslintcache 2>/dev/null || true
	@echo "✓ Cleaned build artifacts"

db-reset:
	@echo "⚠️  This will delete all database data!"
	@read -p "Continue? (y/N) " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose down -v; \
		echo "✓ Database reset"; \
	fi

# Development shortcuts
re-install: clean install
	@echo "✓ Fresh installation complete"

all-tests: test lint
	@echo "✓ All checks passed!"

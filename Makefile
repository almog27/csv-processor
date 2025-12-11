.PHONY: prepare install run test lint fmt docker-build docker-up docker-test clean

VENV := .venv
PY := $(VENV)/bin/python
UV := $(VENV)/bin/uv

prepare:
	@test -d $(VENV) || python3 -m venv $(VENV)
	@echo "Virtual environment ready. To activate it, run:"
	@echo "  source $(VENV)/bin/activate"

install:
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install uv
	$(UV) sync
	$(UV) add --dev pytest pytest-asyncio httpx ruff mypy || true

run:
	$(UV) run uvicorn src.app.main:app --reload --port 2701

test:
	$(UV) run pytest

lint:
	$(UV) run ruff check

fmt:
	$(UV) run ruff format

docker-build:
	docker-compose build

docker-up:
	docker-compose up

docker-test:
	docker-compose run sensor_service $(UV) run pytest

clean:
	rm -rf $(VENV)
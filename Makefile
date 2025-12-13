.PHONY: prepare install run test lint fmt docker-build docker-up docker-down docker-test clean cli-process ui-prep ui-run

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
	PAYTHONPATH=src $(UV) run uvicorn app.main:app --reload --port 2701

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

docker-down:
	docker-compose down --rmi all -v

docker-test:
	docker-compose run csv_processor uv run pytest

clean:
	rm -rf $(VENV)

cli-process:
	${UV} run python -m src.app.cli process ${FILE_ID} ${FILE}

ui-prep:
	cd frontend && npm install

ui-run:
	cd frontend && npm run dev
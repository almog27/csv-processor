FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock* /app/
COPY src /app/src

RUN uv sync

ENV PYTHONPATH=/app/src

EXPOSE 2701

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "2701"]

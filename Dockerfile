FROM python:3.11-slim

WORKDIR /app

RUN pip install poetry

# Disable default Poetry venv creation
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

COPY src/ ./src/
COPY pyproject.toml ./pyproject.toml
COPY poetry.lock ./poetry.lock

RUN poetry install --no-root --only main

ENV PYTHONPATH=/app

CMD ["python", "src/main.py"]
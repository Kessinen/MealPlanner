FROM python:3.12-alpine
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app

COPY .python-version .
COPY pyproject.toml .
COPY uv.lock .

RUN uv sync --locked

COPY src .

FROM python:3.12-slim-bookworm

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=1.8.0

# Install Poetry:
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python3 -

# Install Python dependencies:
WORKDIR /code
COPY poetry.lock pyproject.toml /code/
RUN poetry install --only=main --no-root

# Install sc-audit:
COPY . /code
RUN poetry install --only=main

# Initialize DB with schema
RUN sc-audit schema upgrade

# TODO: bootstrap/restore DB from dump

# Do an initial DB catch-up
RUN sc-audit catch-up

LABEL org.opencontainers.image.source=https://github.com/stellarcarbon/sc-audit
LABEL org.opencontainers.image.description="Stellarcarbon core database with monitoring and audit functionality"
LABEL org.opencontainers.image.licenses=MIT

ENTRYPOINT [ "sc-audit" ]

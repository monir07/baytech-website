FROM python:3.11.8-slim-bullseye as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"


ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


FROM python-base as builder-base
ARG MODE
ARG ENVIRONMENT
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml build-poetry.sh ./
RUN apt-get update && \
    apt-get install --no-install-recommends -y git curl build-essential gcc g++ libpq-dev && \
    curl -sSL https://install.python-poetry.org | python
RUN ./build-poetry.sh


# `production` image used for runtime
FROM python-base as runner

COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
WORKDIR /usr/code
RUN mkdir -p /usr/logs && \
    addgroup --system user && \
    adduser --system --no-create-home --group user && \
    chown -R user:user /usr && chmod -R 755 /usr
COPY . /usr/code
CMD ["python", "manage.py", "runserver", "0.0.0.0:8010"]
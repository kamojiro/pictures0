# build frontend
FROM node:23.7 AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend .
RUN npm run build

# build backend
FROM python:3.12-slim-bookworm AS backend-builder
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app/backend

COPY backend/ .
RUN uv sync --frozen

# backend

FROM python:3.12-slim-bookworm

EXPOSE 8000

RUN apt-get update

WORKDIR /app/backend
COPY backend /app/backend
COPY --from=backend-builder /app/backend/.venv /app/backend/.venv

RUN rm -rf /app/backend/static/*
COPY --from=frontend-builder /app/frontend/dist/ /app/backend/static/

# FastAPI アプリケーション (backend/main.py 内の app) を起動
ENTRYPOINT [".venv/bin/uvicorn", "main:app", "--host", "0.0.0.0"]

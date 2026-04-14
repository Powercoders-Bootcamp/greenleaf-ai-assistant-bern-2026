FROM python:3.14-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

FROM base AS deps
COPY src/backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

FROM base AS runner
COPY --from=deps /usr/local /usr/local
COPY src/backend /app/src/backend
COPY prompts /app/prompts
COPY data /app/data

WORKDIR /app/src

EXPOSE 10000

CMD ["sh", "-c", "python -m alembic -c backend/alembic.ini upgrade head && uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-10000}"]
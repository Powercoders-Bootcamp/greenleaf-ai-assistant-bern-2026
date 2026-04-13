FROM python:3.14-slim

WORKDIR /app

COPY src/backend/requirements.txt /app/src/backend/requirements.txt

RUN pip install --no-cache-dir -r /app/src/backend/requirements.txt

COPY src/backend /app/src/backend
COPY prompts /app/prompts
COPY data /app/data

WORKDIR /app/src

EXPOSE 8000

CMD ["sh", "-c", "python -m alembic -c backend/alembic.ini upgrade head && uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-10000}"]

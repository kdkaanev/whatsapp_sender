FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app/backend

COPY backend/requirements.txt .
COPY docker/celery/entrypoint.sh /entrypoint.sh
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]


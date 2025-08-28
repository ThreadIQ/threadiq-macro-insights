FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/backend/requirements.txt

COPY . /app

# Change ownership of the app directory to the non-root user
RUN chown -R appuser:appuser /app

# Create directories that might be created by Django/Celery and ensure they're owned by appuser
RUN mkdir -p /app/backend/staticfiles /app/backend/static /tmp && chown -R appuser:appuser /app/backend/staticfiles /app/backend/static /tmp

# entrypoint runs migrate/collectstatic then execs CMD
RUN chmod +x /app/docker/entrypoint.sh

# Switch to non-root user
USER appuser

ENTRYPOINT ["/app/docker/entrypoint.sh"]

# default CMD = web; App Platform overrides for worker/beat
CMD ["gunicorn", "core.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080"]
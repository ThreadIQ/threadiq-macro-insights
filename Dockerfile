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

# Create static files directory and collect static files
RUN mkdir -p /app/backend/staticfiles /app/backend/static
RUN chown -R appuser:appuser /app/backend/staticfiles /app/backend/static

# Switch to non-root user
USER appuser

# Collect static files during build
RUN cd /app/backend && python manage.py collectstatic --noinput

# entrypoint runs migrate then execs CMD
RUN chmod +x /app/docker/entrypoint.sh

ENTRYPOINT ["/app/docker/entrypoint.sh"]

# default CMD = web; App Platform overrides for worker/beat
CMD ["gunicorn", "core.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080"]
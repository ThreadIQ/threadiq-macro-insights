web: gunicorn backend.core.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
worker: celery -A backend.core worker -l info -Q default,ingest,analyze,email --autoscale=12,2
beat: celery -A backend.core beat -l info --pidfile= --schedule=/tmp/celerybeat-schedule.db
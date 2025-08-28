web: gunicorn core.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --chdir backend
worker: celery -A core worker -l info -Q default,ingest,analyze,email --autoscale=12,2 --chdir backend
beat: celery -A core beat -l info --pidfile= --schedule=/tmp/celerybeat-schedule.db --chdir backend
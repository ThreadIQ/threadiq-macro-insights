web: bash -c "cd backend && gunicorn core.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT"
worker: bash -c "cd backend && celery -A core worker -l info -Q default,ingest,analyze,email --autoscale=12,2"
beat: bash -c "cd backend && celery -A core beat -l info --pidfile= --schedule=/tmp/celerybeat-schedule.db"
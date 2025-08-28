#!/usr/bin/env bash
set -euo pipefail

# Ensure the staticfiles directory exists and has correct permissions
mkdir -p backend/staticfiles backend/static

# Set proper permissions for static files
chmod -R 755 backend/staticfiles backend/static

python backend/manage.py migrate --noinput || true
python backend/manage.py collectstatic --noinput --clear || true

# Ensure static files have correct permissions after collection
chmod -R 755 backend/staticfiles

exec "$@"
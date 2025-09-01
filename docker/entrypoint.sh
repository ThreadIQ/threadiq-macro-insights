#!/usr/bin/env bash
set -euo pipefail

# Debug: Show static files that were collected during build
echo "Current directory: $(pwd)"
echo "Backend directory contents:"
ls -la backend/
echo "Static files directory contents (collected during build):"
ls -la backend/staticfiles/
echo "Admin static files:"
ls -la backend/staticfiles/admin/ || echo "admin directory not found"

python backend/manage.py migrate --noinput || true

# Debug: Show Django settings for static files
echo "Django static files configuration:"
python backend/manage.py shell -c "
from django.conf import settings
print(f'STATIC_URL: {settings.STATIC_URL}')
print(f'STATIC_ROOT: {settings.STATIC_ROOT}')
print(f'STATICFILES_DIRS: {settings.STATICFILES_DIRS}')
print(f'DEBUG: {settings.DEBUG}')
print(f'INSTALLED_APPS: {settings.INSTALLED_APPS}')
"

exec "$@"
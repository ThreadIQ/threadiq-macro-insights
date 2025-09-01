#!/usr/bin/env bash
set -euo pipefail

# Ensure static files directory exists and has correct permissions
mkdir -p backend/staticfiles backend/static

# Set proper permissions for static files
chmod -R 755 backend/staticfiles backend/static

# Debug: Show current directory and list contents
echo "Current directory: $(pwd)"
echo "Backend directory contents:"
ls -la backend/
echo "Static files directory contents (before collection):"
ls -la backend/staticfiles/ || echo "staticfiles directory is empty or doesn't exist"

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

# Collect static files with verbose output
echo "Collecting static files..."
python backend/manage.py collectstatic --noinput --clear --verbosity=2

# Debug: Show static files after collection
echo "Static files directory contents (after collection):"
ls -la backend/staticfiles/
echo "Admin static files:"
ls -la backend/staticfiles/admin/ || echo "admin directory not found"

# Ensure static files have correct permissions after collection
chmod -R 755 backend/staticfiles

exec "$@"
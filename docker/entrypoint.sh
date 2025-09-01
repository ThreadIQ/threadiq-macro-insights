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

# Test static file serving
echo "Testing static file access:"
python backend/manage.py shell -c "
from django.conf import settings
from django.contrib.staticfiles.finders import find
import os

# Try to find a specific admin CSS file
admin_css = find('admin/css/login.css')
print(f'Found admin/css/login.css: {admin_css}')
if admin_css:
    print(f'File exists: {os.path.exists(admin_css)}')
    print(f'File readable: {os.access(admin_css, os.R_OK)}')

# Check if STATIC_ROOT is accessible
static_root = settings.STATIC_ROOT
print(f'STATIC_ROOT accessible: {os.access(static_root, os.R_OK)}')
print(f'STATIC_ROOT contents: {os.listdir(static_root)}')
"

exec "$@"
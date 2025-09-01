"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Always serve static files (both development and production)
# Note: In production, this should ideally be handled by a web server like nginx
# But for now, we'll let Django serve them to get things working
if not settings.DEBUG:
    # In production, we need to serve static files ourselves
    # Create a custom view that logs static file requests
    def static_serve_with_logging(request, path):
        print(f"Static file request: /static/{path}")
        print(f"Looking for file at: {settings.STATIC_ROOT}/{path}")
        import os
        full_path = os.path.join(settings.STATIC_ROOT, path)
        print(f"Full path: {full_path}")
        print(f"File exists: {os.path.exists(full_path)}")
        if os.path.exists(full_path):
            print(f"File readable: {os.access(full_path, os.R_OK)}")
        return serve(request, path, document_root=settings.STATIC_ROOT)
    
    # Add static file serving patterns
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', static_serve_with_logging, name='static'),
    ]
    print(f"Added production static file serving for {settings.STATIC_URL} from {settings.STATIC_ROOT}")
else:
    # In development, use Django's static helper
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    print(f"Added development static file serving for {settings.STATIC_URL} from {settings.STATIC_ROOT}")

print(f"Final URL patterns: {urlpatterns}")
print(f"Static file serving enabled: {any('static' in str(pattern) for pattern in urlpatterns)}")

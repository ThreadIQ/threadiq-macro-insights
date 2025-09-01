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
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Always serve static files (both development and production)
# Note: In production, this should ideally be handled by a web server like nginx
# But for now, we'll let Django serve them to get things working
if not settings.DEBUG:
    # In production, we need to serve static files ourselves
    # Create a custom view that serves static files without ASGI warnings
    def static_serve_with_logging(request, path):
        import os
        from django.http import FileResponse, Http404
        from django.conf import settings
        
        full_path = os.path.join(settings.STATIC_ROOT, path)
        
        if not os.path.exists(full_path):
            raise Http404(f"Static file not found: {path}")
        
        # Use FileResponse instead of serve() to avoid ASGI warnings
        response = FileResponse(open(full_path, 'rb'))
        
        # Set appropriate content type based on file extension
        if path.endswith('.css'):
            response['Content-Type'] = 'text/css'
        elif path.endswith('.js'):
            response['Content-Type'] = 'application/javascript'
        elif path.endswith('.png'):
            response['Content-Type'] = 'image/png'
        elif path.endswith('.jpg') or path.endswith('.jpeg'):
            response['Content-Type'] = 'image/jpeg'
        elif path.endswith('.svg'):
            response['Content-Type'] = 'image/svg+xml'
        elif path.endswith('.woff'):
            response['Content-Type'] = 'font/woff'
        elif path.endswith('.woff2'):
            response['Content-Type'] = 'font/woff2'
        elif path.endswith('.ttf'):
            response['Content-Type'] = 'font/ttf'
        elif path.endswith('.eot'):
            response['Content-Type'] = 'font/eot'
        
        return response
    
    # Add static file serving patterns
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', static_serve_with_logging, name='static'),
    ]
else:
    # In development, use Django's static helper
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

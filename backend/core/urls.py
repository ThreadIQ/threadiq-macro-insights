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

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Serve static files in development and production
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    print(f"DEBUG mode: Added static files serving for {settings.STATIC_URL} from {settings.STATIC_ROOT}")
else:
    # In production, serve static files directly
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    print(f"PRODUCTION mode: Added static files serving for {settings.STATIC_URL} from {settings.STATIC_ROOT}")

print(f"Final URL patterns: {urlpatterns}")

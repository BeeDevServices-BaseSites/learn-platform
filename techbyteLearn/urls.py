
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from app import views as app_views
from api import views as app_views

urlpatterns = [
    path('', include('app.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

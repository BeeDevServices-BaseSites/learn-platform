
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from coreApp import views as app_views
from api import views as app_views
from courseApp import views as app_views
from financeApp import views as app_views

urlpatterns = [
    path('', include('coreApp.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('course/', include('courseApp.urls')),
    path('finance/', include('financeApp.urls')),
]

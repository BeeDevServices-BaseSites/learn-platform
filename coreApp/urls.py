from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Base Route
    path('', views.index),
    path('login_page/', views.login_page ),
    path('login/', views.login),
    path('dashboard/', views.dashboard),
    path('queen/bees/admin-register/', views.admin_register),
    path('register/', views.register),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
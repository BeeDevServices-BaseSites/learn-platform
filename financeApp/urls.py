from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
<<<<<<< HEAD:app/urls.py
    # Base Route
    path('', views.index),
    path('login', views.userLogin, name='user_login'),
    
    

=======
    # /finance Base Route
    # path('', views.),
>>>>>>> dev:financeApp/urls.py
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
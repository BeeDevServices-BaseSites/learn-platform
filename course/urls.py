from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # /course Base Route
    path('', views.intro_prog_ch01_pg01),
    path('010102/', views.intro_prog_ch01_pg02),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
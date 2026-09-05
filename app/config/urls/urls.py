
from django.contrib import admin
from django.urls import path, include
from .v1 import urlpatterns  as v1_urlpatterns
from config.settings import production
from django.conf.urls.static import static


urlpatterns = [
    path('v1/', include(v1_urlpatterns)),
]


if production.DEBUG:
    urlpatterns += static(production.MEDIA_URL, document_root=production.MEDIA_ROOT)
    urlpatterns += static(production.STATIC_URL, document_root=production.STATIC_ROOT)
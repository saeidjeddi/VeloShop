
from django.contrib import admin
from django.urls import path, include
from .v1 import urlpatterns  as v1_urlpatterns
from config.settings import production
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include(v1_urlpatterns)),
]

urlpatterns += [

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]


if production.DEBUG:
    urlpatterns += static(production.MEDIA_URL, document_root=production.MEDIA_ROOT)
    urlpatterns += static(production.STATIC_URL, document_root=production.STATIC_ROOT)
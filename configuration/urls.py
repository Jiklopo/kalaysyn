from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

open_api_patterns = [
    path('', SpectacularAPIView.as_view(), name='schema'),
    path('swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

api_patterns = [
    path('health/', include('apps.health.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_patterns)),
    path('api/schema/', include(open_api_patterns)),
]
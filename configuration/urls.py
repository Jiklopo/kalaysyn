from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from apps import goals

open_api_patterns = [
    path('', SpectacularAPIView.as_view(), name='schema'),
    path('swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

auth_patterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', include('apps.authentication.urls'))
]

api_patterns = [
    path('auth/', include(auth_patterns)),
    path('health/', include('apps.health.urls')),
    path('records/', include('apps.records.urls')),
    path('code/', include('apps.qr.urls')),
    path('profile/', include('apps.profile.urls')),
    path('goals/', include('apps.goals.urls')),
    path('tests/', include('apps.psytests.urls'))
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_patterns)),
    path('api/schema/', include(open_api_patterns)),
]

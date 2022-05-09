from django.urls import path
from apps.authentication.views import (
    ChangePasswordView,
    DeactivateAccountView,
    RegisterView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('deactivate/', DeactivateAccountView.as_view(), name='delete-account'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]

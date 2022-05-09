from django.urls import path, include
from apps.authentication.views import (
    ChangePasswordView,
    DeactivateAccountView,
    RegisterView,
    RequestPasswordResetView,
    ResetPasswordView,
    ValidateResetCodeView
)

reset_patterns = [   
     path('', ResetPasswordView.as_view(), name='request-password-reset'),
     path('request/', RequestPasswordResetView.as_view(), name='request-password-reset'),
     path('validate-code/', ValidateResetCodeView.as_view(), name='request-password-reset'),
]

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('deactivate/', DeactivateAccountView.as_view(), name='delete-account'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('reset/', include(reset_patterns))
]

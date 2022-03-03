from django.urls import path
from apps.authentication.views import DeactivateAccountView, RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('deactivate/', DeactivateAccountView.as_view(), name='delete-account')
]

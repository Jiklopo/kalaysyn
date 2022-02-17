from django.urls import path
from .views import *

urlpatterns = [
    path('', HealthView.as_view(), name='check-health')
]

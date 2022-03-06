from django.urls import path

from apps.profile.views import BecomeDoctorView

urlpatterns = [
    path('become-doctor/', BecomeDoctorView.as_view(), name='become-doctor')
]

from django.urls import path

from apps.profile.views import BecomeDoctorView, PatientRecordsView, ProfileView

urlpatterns = [
    path('become-doctor/', BecomeDoctorView.as_view(), name='become-doctor'),
    path('patients/', PatientRecordsView.as_view(), name='profile-patients'),
    path('', ProfileView.as_view(), name='profile-retrieve-update')
]

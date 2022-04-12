from django.urls import path

from apps.profile.views import BecomeDoctorView, PatientView, PatientsListView, ProfileView

urlpatterns = [
    path('become-doctor/', BecomeDoctorView.as_view(), name='become-doctor'),
    path('patients/', PatientsListView.as_view(), name='profile-patients-list'),
    path('patients/<str:pk>/', PatientView.as_view(), name='profile-patients-retrieve'),
    path('', ProfileView.as_view(), name='profile-retrieve-update')
]

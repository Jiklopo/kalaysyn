from django.urls import path

from apps.profile.views import (
    BecomeDoctorView,
    PatientView,
    PatientsListView,
    PermissionRetrieveUpdateDestroyView,
    ProfileView,
    RelationshipRetrieveDestroyView
)

urlpatterns = [
    path('become-doctor/', BecomeDoctorView.as_view(), name='become-doctor'),
    path('relationships/<int:pk>/', RelationshipRetrieveDestroyView.as_view(),
         name='profile-relationship'),
    path('permissions/<int:pk>/', PermissionRetrieveUpdateDestroyView.as_view(),
         name='profile-permissions'),
    path('patients/', PatientsListView.as_view(), name='profile-patients-list'),
    path('patients/<str:pk>/', PatientView.as_view(),
         name='profile-patients-retrieve'),
    path('', ProfileView.as_view(), name='profile-retrieve-update')
]

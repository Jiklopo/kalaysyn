from django.urls import path, include

from apps.profile.views import (
    BecomeDoctorView,
    PatientView,
    PatientsListView,
    PermissionRetrieveUpdateDestroyView,
    PermissionsListView,
    ProfileView,
    RelationshipRetrieveDestroyView,
    RelationshipListView
)

relationship_patterns = [
    path('', RelationshipListView.as_view(), name='profile-relationship-list'),
    path('<int:pk>/', RelationshipRetrieveDestroyView.as_view(),
         name='profile-relationship-retrive-update-delete')
]

patients_patterns = [
    path('', PatientsListView.as_view(), name='profile-patients-list'),
    path('<str:pk>/', PatientView.as_view(),
         name='profile-patients-retrieve'),
]

permission_patterns = [
    path('', PermissionsListView.as_view(), name='permissions-list'),
    path('<int:pk>/', PermissionRetrieveUpdateDestroyView.as_view(),
         name='profile-permissions-retrieve-update-delete'),
]

urlpatterns = [
    path('become-doctor/', BecomeDoctorView.as_view(), name='become-doctor'),
    path('relationships/', include(relationship_patterns)),
    path('patients/', include(patients_patterns)),
    path('permissions/', include(permission_patterns)),
    path('', ProfileView.as_view(), name='profile-retrieve-update')
]

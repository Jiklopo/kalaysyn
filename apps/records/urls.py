from django.urls import path

from apps.records.views import (
    RecordListCreateView,
    RecordUpdateDeleteView,
    RecordImageUploadView,
    RecordDateRangeView,
    ReportListCreateView
)

urlpatterns = [
    path('', RecordListCreateView.as_view(), name='records-list-create'),
    path('<int:pk>/', RecordUpdateDeleteView.as_view(), name='records-update-delete'),
    path('<int:record_id>/upload-image', RecordImageUploadView.as_view(), name='records-image-upload'),
    path('range/', RecordDateRangeView.as_view(), name='records-range'),
    path('reports/', ReportListCreateView.as_view(), name='reports-list-create'),
]

from django.urls import path

from apps.records.views import (
    RecordListCreateView,
    RecordUpdateDeleteView,
    RecordImageUploadDeleteView,
    RecordDateRangeView,
    ReportListCreateView
)

urlpatterns = [
    path('', RecordListCreateView.as_view(), name='records-list-create'),
    path('<int:pk>/', RecordUpdateDeleteView.as_view(), name='records-update-delete'),
    path('<int:record_id>/image/', RecordImageUploadDeleteView.as_view(), name='records-image-upload-delete'),
    path('range/', RecordDateRangeView.as_view(), name='records-range'),
    path('reports/', ReportListCreateView.as_view(), name='reports-list-create'),
]

from django.urls import path

from apps.records.views import (
    ImageUploadView,
    RecordListCreateView,
    RecordUpdateDeleteView,
    RecordDateRangeView,
    ReportListCreateView
)

urlpatterns = [
    path('', RecordListCreateView.as_view(), name='records-list-create'),
    path('<int:pk>/', RecordUpdateDeleteView.as_view(), name='records-update-delete'),
    path('range/', RecordDateRangeView.as_view(), name='records-range'),
    path('reports/', ReportListCreateView.as_view(), name='reports-list-create'),
    path('image', ImageUploadView.as_view(), name='record-upload-image')
]

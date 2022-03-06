from django.urls import path

from apps.records.views import (
    RecordListCreateView,
    RecordUpdateDeleteView,
    RecordDateRangeView
)

urlpatterns = [
    path('', RecordListCreateView.as_view(), name='records-list-create'),
    path('<int:pk>/', RecordUpdateDeleteView.as_view(), name='records-update-delete'),
    path('range/', RecordDateRangeView.as_view(), name='records-range'),
]

from django.urls import path, include

from apps.psytests.views import PsyTestsListView, PsyTestRateView, RecordListCreateView, RecordRetrieveUpdateDeleteView

psytests_urls = [
    path('', PsyTestsListView.as_view(), name='psytests-list'),
    path('<int:pk>/rate/', PsyTestRateView.as_view(), name='psytest-rate')
]

records_urls = [
    path('', RecordListCreateView.as_view(), name='psytestrecord-list-create'),
    path('<int:pk>/', RecordRetrieveUpdateDeleteView.as_view(),
         name='psytestrecord-retrieve-update-destroy')
]

urlpatterns = [
    path('', include(psytests_urls)),
    path('records/', include(records_urls))
]

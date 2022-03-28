from django.urls import path, include

from apps.psytests.views import ListPsyTestsView

psytests_urls = [
    path('', ListPsyTestsView.as_view(), name='psytests-list')
]

urlpatterns = [
    path('tests/', include(psytests_urls))    
]


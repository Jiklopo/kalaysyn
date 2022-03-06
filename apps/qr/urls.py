from django.urls import path

from apps.qr.views import GenerateCodeView, LinkCodeView

urlpatterns = [
    path('generate/', GenerateCodeView.as_view(), name='generate-code'),
    path('link/<str:pk>/', LinkCodeView.as_view(), name='link-code')
]

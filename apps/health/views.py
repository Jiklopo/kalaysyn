from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthView(APIView):
    @extend_schema(description='Check connection to the server')
    def get(self, request):
        return Response()


class AuthHealthView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(description='Check authorization')
    def get(self, request):
        return Response()

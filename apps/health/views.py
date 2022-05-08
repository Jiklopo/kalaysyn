from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.views import IsAuthenticatedView
from apps.health.tasks import test_task


class HealthView(APIView):
    @extend_schema(description='Check connection to the server')
    def get(self, request):
        return Response()


class AuthHealthView(IsAuthenticatedView):
    @extend_schema(description='Check authorization')
    def get(self, request):
        return Response()


class CeleryHealthView(IsAuthenticatedView):
    @extend_schema(description='Run test celery task')
    def post(self, request):
        task = test_task.delay()
        return Response(task.id)

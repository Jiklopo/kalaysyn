from urllib import response
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.views import IsAuthenticatedView
from apps.health.tasks import test_task


class HealthView(APIView):
    @extend_schema(
        description='Check connection to the server',
        responses={200:None}
    )
    def get(self, request):
        return Response()


class AuthHealthView(IsAuthenticatedView):
    @extend_schema(
        description='Check authorization', 
        responses={200:None}
    )
    def get(self, request):
        return Response()


class CeleryHealthView(IsAuthenticatedView):
    @extend_schema(
        description='Run test celery task',
        responses={200:None}
        )
    def post(self, request):
        task = test_task.delay()
        return Response({'task_id':task.id})

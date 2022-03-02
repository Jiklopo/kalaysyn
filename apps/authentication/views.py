from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from drf_spectacular.utils import extend_schema

from apps.authentication.serializers import UserInputSerializer
from apps.authentication.services import create_user

class RegisterView(APIView):
    @extend_schema(
        request=UserInputSerializer,
        responses={201:'', 400: ''}
    )
    def post(self, request: Request):
        serializer = UserInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        user = create_user(
            username=validated_data.pop('username'),
            password=validated_data.pop('password'),
            **validated_data
        )
        return Response(status=status.HTTP_201_CREATED)
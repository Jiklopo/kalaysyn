from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from apps.authentication.models import User
from apps.authentication.serializers import PasswordSerializer, UserInputSerializer
from apps.common.views import IsAuthenticatedView


class RegisterView(GenericAPIView, mixins.CreateModelMixin):
    serializer_class = UserInputSerializer
    queryset = User.objects.all()

    @extend_schema(
        request=UserInputSerializer,
        responses={
            201: None,
            400: OpenApiResponse(
                [OpenApiTypes.STR],
                description='errors dictionary'
            )
        }
    )
    def post(self, request, *args, **kwargs):
        password = request.data.get('password')
        if not password:
            return self.create(request, *args, **kwargs)

        try:
            validate_password(password)
        except ValidationError as e:
            data = {msg.code: msg.messages[0] for msg in e.error_list}
            return Response(data, status.HTTP_400_BAD_REQUEST)

        return self.create(request, *args, **kwargs)


class DeactivateAccountView(IsAuthenticatedView):
    serializer_class = PasswordSerializer

    @extend_schema(
        description='Deactivate user account',
        responses={
            204: None
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get('password')

        user: User = request.user
        if not user.check_password(password):
            data = {'error': 'Incorrect password provided'}
            return Response(data, status.HTTP_403_FORBIDDEN)

        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

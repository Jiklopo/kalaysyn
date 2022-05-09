from rest_framework import status
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

from apps.authentication.mixins import ValidatePasswordMixin
from apps.authentication.models import User
from apps.authentication.serializers import ChangePasswordSerializer, PasswordSerializer, UserInputSerializer
from apps.common.views import IsAuthenticatedView


class RegisterView(GenericAPIView, mixins.CreateModelMixin):
    serializer_class = UserInputSerializer
    queryset = User.objects.all()

    @extend_schema(
        request=UserInputSerializer,
        responses={201: '', 400: ''}
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



class DeactivateAccountView(IsAuthenticatedView, ValidatePasswordMixin):
    serializer_class = PasswordSerializer

    @extend_schema(
        description='Deactivate user account',
        responses={
            204: None
        }
    )
    def post(self, request):
        self.validate_password(request)
        user = request.user
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(IsAuthenticatedView, ValidatePasswordMixin):
    serializer_class = ChangePasswordSerializer
    
    @extend_schema(
        description='Change user password',
        responses={
            204: None
        }
    )
    def post(self, request):
        serializer = self.validate_password(request)
        new_pass = serializer.validated_data.get('new_password')
        user: User = request.user
        user.set_password(new_pass)
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


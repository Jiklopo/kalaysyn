from http.client import NO_CONTENT
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework import mixins
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

from apps.authentication.mixins import ValidatePasswordMixin
from apps.authentication.models import PasswordResetCode, User
from apps.common.views import IsAuthenticatedView
from apps.authentication.serializers import UserSerializer


class RegisterView(GenericAPIView, mixins.CreateModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @extend_schema(
        request=UserSerializer,
        responses={201: '', 400: ''}
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DeactivateAccountView(IsAuthenticatedView, ValidatePasswordMixin):
    class PasswordSerializer(serializers.Serializer):
        password = serializers.CharField()

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
    class ChangePasswordSerializer(serializers.Serializer):
        password = serializers.CharField()
        new_password = serializers.CharField()

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
        user = request.user
        user.set_password(new_pass)
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordResetBaseView(GenericAPIView):
    def get_user(self) -> User:
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        return get_object_or_404(User, username=username)

    def get_reset_code(self, user=None) -> PasswordResetCode:
        user = user or self.get_user()
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data.get('code')
        return get_object_or_404(PasswordResetCode, user=user, code=code)


class RequestPasswordResetView(PasswordResetBaseView):
    class RequestPasswordResetSerializer(serializers.Serializer):
        username = serializers.CharField()

    serializer_class = RequestPasswordResetSerializer

    @extend_schema(
        description='Request reset code to email',
        responses={
            204: None
        }
    )
    def post(self, request):
        user = self.get_user()
        if not user.email:
            return Response(status=status.HTTP_404_NOT_FOUND)

        reset_code = PasswordResetCode.objects.create(user=user)
        reset_msg = f'Hi, {user.get_full_name()}! We have received a password reset request for your account. ' +\
                    f'If you have not submitted any request, please, ignore this message.\n\n' +\
                    f'Here is your code: {reset_code.code}'
        
        send_mail(
            subject='Kalaysyn Password Reset',
            message=reset_msg,
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class ValidateResetCodeView(PasswordResetBaseView):
    class ValidateResetCodeSerializer(serializers.Serializer):
        username = serializers.CharField()
        code = serializers.CharField()

    serializer_class = ValidateResetCodeSerializer

    @extend_schema(
        description='Validate',
        responses={
            204: None
        }
    )
    def post(self, request):
        reset_code = self.get_reset_code()
        if not reset_code.is_valid:
            return Response(status=status.HTTP_404_NOT_FOUND)

        reset_code.was_validated = True
        reset_code.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ResetPasswordView(PasswordResetBaseView):
    class ResetPasswordSerializer(serializers.Serializer):
        username = serializers.CharField()
        code = serializers.CharField()
        new_password = serializers.CharField()

    serializer_class = ResetPasswordSerializer

    def post(self, request):
        user = self.get_user()
        reset_code = self.get_reset_code(user=user)
        if not reset_code.was_validated:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data.get('new_password')
        user.set_password(new_password)
        user.save()
        reset_code.delete()
        return Response(status=NO_CONTENT)
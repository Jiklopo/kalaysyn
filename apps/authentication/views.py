from rest_framework import status
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

from apps.authentication.models import User
from apps.authentication.serializers import PasswordSerializer, UserInputSerializer
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
            return Response('Incorrect password provided', status.HTTP_403_FORBIDDEN)

        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

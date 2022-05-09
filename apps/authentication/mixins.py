from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import Serializer

from apps.authentication.models import User


class ValidatePasswordMixin:
    def validate_password(self, request) -> Serializer:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get('password')

        user: User = request.user
        if not user.check_password(password):
            raise PermissionDenied

        return serializer

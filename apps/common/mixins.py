from rest_framework import status, exceptions
from rest_framework.response import Response


class CreateAndAddUserMixin:
    """
    Retrieve user from request and to as user_field
    """
    user_field = 'user'

    def create(self, request, *args, **kwargs):
        if request.user is None:
            raise exceptions.NotAuthenticated()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_kwargs = {}
        user_kwargs[self.user_field] = request.user
        user = serializer.save(**user_kwargs)
        data = {self.user_field: user.id, **serializer.data}
        return Response(data=data, status=status.HTTP_201_CREATED)

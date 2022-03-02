from rest_framework import status, exceptions
from rest_framework.response import Response


class CreateAndAddUserMixin:
    """
    Retrieve user from request
    """

    def create(self, request, *args, **kwargs):
        if request.user is None:
            raise exceptions.NotAuthenticated()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(user=request.user)
        data = {'id': user.id, **serializer.data}
        return Response(data=data, status=status.HTTP_201_CREATED)

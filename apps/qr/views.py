from rest_framework import mixins
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from drf_spectacular.utils import extend_schema

from apps.common.views import IsAuthenticatedView
from apps.qr.models import RelationshipCode
from apps.qr.serializers import LinkCodeSerializer, GenerateCodeSerializer


class GenerateCodeView(IsAuthenticatedView, mixins.CreateModelMixin):
    serializer_class = GenerateCodeSerializer
    queryset = RelationshipCode.objects.all()

    def get_serializer(self, *args, **kwargs):
        kwargs['data'] = {'doctor_id': self.request.user.id}
        return super().get_serializer(*args, **kwargs)

    @extend_schema(
        request=None,
        responses={
            201: GenerateCodeSerializer
        }
    )
    def post(self, request: Request, *args, **kwargs):
        if not request.user.is_doctor:
            return Response('Only doctors can generate codes', status.HTTP_403_FORBIDDEN)

        return self.create(request, *args, **kwargs)


class LinkCodeView(IsAuthenticatedView, mixins.UpdateModelMixin):
    serializer_class = LinkCodeSerializer
    queryset = RelationshipCode.objects.all()

    def get_serializer(self, *args, **kwargs):
        kwargs['data'] = {'user_id': self.request.user.id}
        return super().get_serializer(*args, **kwargs)

    def get_object(self):
        code = super().get_object()
        if not code or not code.is_valid or code.user is not None:
            raise NotFound()
        return code

    @extend_schema(
        request=None,
        responses=None
    )
    def post(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

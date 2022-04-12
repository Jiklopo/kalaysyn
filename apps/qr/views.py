from rest_framework import mixins
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from drf_spectacular.utils import extend_schema

from apps.common.views import IsAuthenticatedView
from apps.qr.models import RelationshipCode
from apps.qr.serializers import GenerateCodeSerializer, RelationshipSerializer


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
            return Response({'error': 'Only doctors can generate codes'}, status.HTTP_403_FORBIDDEN)

        return self.create(request, *args, **kwargs)


class LinkCodeView(IsAuthenticatedView):
    serializer_class = RelationshipSerializer
    queryset = RelationshipCode.objects.all()

    def get_object(self):
        code = super().get_object()
        if not code or not code.is_valid or code.user is not None:
            raise NotFound()
        if code.doctor.id == self.request.user.id:
            raise ParseError('user cannot link with himself')
        return code

    @extend_schema(
        request=None,
        responses=None
    )
    def post(self, request):
        code = self.get_object()
        data = {
            'doctor': code.doctor.id,
            'user': request.user.id
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        code.delete()
        return Response(serializer.data, status.HTTP_201_CREATED)

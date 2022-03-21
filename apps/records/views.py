from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework import mixins

from apps.common.filters import DateRangeFilter, UserFieldFilter
from apps.common.mixins import CreateAndAddUserMixin
from apps.common.views import IsAuthenticatedView
from apps.records.models import Record
from apps.records.serializers import RecordSerializer


class RecordListCreateView(IsAuthenticatedView,
                           CreateAndAddUserMixin,
                           mixins.ListModelMixin):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

    @extend_schema(description='Returns list of user records')
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        description='Create user record',
        responses={
            201: serializer_class
        }
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RecordUpdateDeleteView(IsAuthenticatedView,
                             mixins.DestroyModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.RetrieveModelMixin):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    filter_backends = [UserFieldFilter]

    @extend_schema(description='Get record details')
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(description='Update record, all arguments are optional')
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(description='Delete record')
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class RecordDateRangeView(IsAuthenticatedView,
                          mixins.ListModelMixin):
    serializer_class = RecordSerializer
    filter_backends = [UserFieldFilter, DateRangeFilter]

    @extend_schema(
        description='Get user records in specified date range',
        parameters=[
            OpenApiParameter('from', OpenApiTypes.DATE,
                             description='DD-MM-YY HH:MM | Default: the beginning of times'),
            OpenApiParameter('to', OpenApiTypes.DATE,
                             description='DD-MM-YY HH:MM | Default: Now')
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

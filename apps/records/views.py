from datetime import datetime

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework import mixins
from rest_framework.exceptions import ParseError

from apps.common.mixins import CreateAndAddUserMixin, UserSpecificQuerysetMixin
from apps.common.views import IsAuthenticatedView
from apps.records.models import Record
from apps.records.serializers import RecordSerializer


class RecordListCreateView(IsAuthenticatedView,
                           CreateAndAddUserMixin,
                           UserSpecificQuerysetMixin,
                           mixins.ListModelMixin):
    serializer_class = RecordSerializer
    queryset = Record.objects.all()

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
                             UserSpecificQuerysetMixin,
                             mixins.DestroyModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.RetrieveModelMixin):
    serializer_class = RecordSerializer
    queryset = Record.objects.all()

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
                          UserSpecificQuerysetMixin,
                          mixins.ListModelMixin):
    serializer_class = RecordSerializer

    def parse_date(self, parameter_name, default) -> datetime:
        date_string = self.request.query_params.get(parameter_name)
        if not date_string:
            return default

        format = '%d-%m-%y %H:%M'
        try:
            return datetime.strptime(date_string, format)
        except ValueError:
            raise ParseError('date must have format DD-MM-YY HH:MM')

    def get_queryset(self):
        from_date = self.parse_date('from', datetime.fromtimestamp(0))
        to_date = self.parse_date('to', datetime.now())
        return Record\
            .objects\
            .filter(user=self.request.user, date__gte=from_date, date__lte=to_date)\
            .order_by('date')

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

from datetime import datetime

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework import mixins
from rest_framework.exceptions import ParseError

from apps.common.mixins import CreateAndAddUserMixin
from apps.common.views import IsAuthenticatedView
from apps.records.models import Record
from apps.records.serializers import RecordSerializer


class RecordListCreateView(IsAuthenticatedView,
                           CreateAndAddUserMixin,
                           mixins.ListModelMixin):
    serializer_class = RecordSerializer

    def get_queryset(self):
        return Record.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RecordUpdateDeleteView(IsAuthenticatedView,
                             mixins.DestroyModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.RetrieveModelMixin):
    serializer_class = RecordSerializer

    def get_queryset(self):
        return Record.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class RecordDateRangeView(IsAuthenticatedView, mixins.ListModelMixin):
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
        parameters=[
            OpenApiParameter('from', OpenApiTypes.DATE, description='DD-MM-YY HH:MM | Default: the beginning of times'),
            OpenApiParameter('to', OpenApiTypes.DATE, description='DD-MM-YY HH:MM | Default: Now')
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

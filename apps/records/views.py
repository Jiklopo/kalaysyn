from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from apps.common.filters import DateRangeFilter, UserFieldFilter
from apps.common.mixins import CreateAndAddUserMixin
from apps.common.views import IsAuthenticatedView
from apps.records.models import Record, RecordReport
from apps.records.serializers import RecordOutputSerializer, RecordSerializer, ReportSerializer
from apps.records.tasks import generate_report_task


class RecordListCreateView(IsAuthenticatedView,
                           CreateAndAddUserMixin,
                           mixins.ListModelMixin):
    queryset = Record.objects.all()
    filter_backends = [UserFieldFilter]

    def get_serializer_class(self):
        return RecordOutputSerializer if self.request.method == 'GET'\
            else RecordSerializer

    @extend_schema(description='Returns list of user records')
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        description='Create user record',
        responses={
            201: RecordSerializer
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


class RecordImageUploadDeleteView(IsAuthenticatedView):
    lookup_url_kwarg = 'record_id'
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    filter_backends = [UserFieldFilter]
    parser_classes = [MultiPartParser]

    @extend_schema(
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'file': {
                        'type': 'string',
                        'format': 'binary'
                    }
                }
            }
        },
    )
    def post(self, request, record_id):
        files = list(request.FILES.values())
        if not files:
            return Response({'detail': 'No files were provided'}, status=status.HTTP_400_BAD_REQUEST)

        file = files[0]
        record: Record = self.get_object()
        record.image.save(file.name, file)
        serializer = self.get_serializer(instance=record)
        return Response(serializer.data)

    def delete(self, request, record_id):
        record: Record = self.get_object()
        record.image = None
        record.save()
        serializer = self.get_serializer(instance=record)
        return Response(serializer.data)


class RecordDateRangeView(IsAuthenticatedView,
                          mixins.ListModelMixin):
    queryset = Record.objects.all()
    serializer_class = RecordOutputSerializer
    filter_backends = [UserFieldFilter, DateRangeFilter]

    @extend_schema(
        description='Get user records in specified date range, inclusive',
        parameters=[
            OpenApiParameter('from', OpenApiTypes.DATE,
                             description='DD-MM-YY | Default: the beginning of times'),
            OpenApiParameter('to', OpenApiTypes.DATE,
                             description='DD-MM-YY | Default: Now')
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ReportListCreateView(IsAuthenticatedView,
                           mixins.ListModelMixin):
    queryset = RecordReport.objects.all()
    serializer_class = ReportSerializer
    filter_backends = [UserFieldFilter]

    def get(self, request):
        return self.list(request)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        report = serializer.save(user=request.user)
        task = generate_report_task.delay(report_id=report.id)
        return Response(serializer.data, status.HTTP_201_CREATED)

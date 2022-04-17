from datetime import date, timedelta
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import ParseError
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import OpenApiParameter, extend_schema
from drf_spectacular.types import OpenApiTypes

from apps.authentication.models import User
from apps.common.filters import DateRangeFilter
from apps.common.permissions import IsDoctorPermission
from apps.profile.serializers import PatientSerializer, PatientRecordsSerializer
from apps.qr.models import Relationship
from apps.records.models import Record


class PatientBaseView(GenericAPIView):
    permission_classes = [IsDoctorPermission]


class PatientsListView(PatientBaseView, mixins.ListModelMixin):
    serializer_class = PatientSerializer

    def get_queryset(self):
        user = self.request.user
        return User\
            .objects\
            .prefetch_related('user_relationships', 'doctor_relationships')\
            .filter(user_relationships__id__in=[r.id for r in user.doctor_relationships.all()])

    def get(self, request):
        return self.list(request)


class PatientView(PatientBaseView, mixins.ListModelMixin):
    serializer_class = PatientRecordsSerializer
    queryset = Record.objects.all()
    lookup_url_kwarg = 'patient_id'

    filter_backends = [DateRangeFilter]
    default_from_date = date.today() - timedelta(30)

    def get_queryset(self):
        qs = super().get_queryset()
        patient_id = self.kwargs.get(self.lookup_url_kwarg)
        if patient_id is None:
            raise ParseError('no patient id provided')

        qs = qs.filter(user__id=patient_id)
        return qs

    def get_serializer(self, *args, **kwargs):
        relationship = get_object_or_404(
            Relationship,
            doctor=self.request.user,
            user__id=self.kwargs.get(self.lookup_url_kwarg)
        )
        kwargs['permission'] = relationship.permissions
        return super().get_serializer(*args, **kwargs)

    @extend_schema(
        description='Get patient records in specified date range, inclusive',
        parameters=[
            OpenApiParameter('from', OpenApiTypes.DATE,
                             description='DD-MM-YY | Default: 30 days ago'),
            OpenApiParameter('to', OpenApiTypes.DATE,
                             description='DD-MM-YY | Default: Now')
        ],
        responses={200: PatientRecordsSerializer}
    )
    def get(self, request, patient_id):
        return self.list(request)

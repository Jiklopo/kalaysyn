from rest_framework import mixins
from rest_framework.generics import GenericAPIView

from apps.authentication.models import User
from apps.common.permissions import IsDoctorPermission
from apps.profile.serializers import PatientSerializer, PatientRecordsSerializer


class PatientBaseView(GenericAPIView):
    permission_classes = [IsDoctorPermission]

    def get_queryset(self):
        user = self.request.user
        return User\
            .objects\
            .prefetch_related('user_relationships', 'doctor_relationships')\
            .filter(user_relationships__id__in=[r.id for r in user.doctor_relationships.all()])


class PatientsListView(PatientBaseView, mixins.ListModelMixin):
    serializer_class = PatientSerializer

    def get(self, request):
        return self.list(request)


class PatientView(PatientBaseView, mixins.RetrieveModelMixin):
    serializer_class = PatientRecordsSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)
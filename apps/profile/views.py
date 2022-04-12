from rest_framework import mixins
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.db.models import Q
from drf_spectacular.utils import extend_schema

from apps.common.views import IsAuthenticatedView
from apps.common.permissions import IsDoctorPermission
from apps.authentication.models import User
from apps.profile.serializers import BecomeDoctorSerializer, PatientRecordsSerializer, PatientSerializer, PermissionsSerializer, ProfileSerializer, RelationshipSerializer
from apps.qr.models import Relationship, RelationshipPermission


class PatientBaseView(GenericAPIView):
    permission_classes = [IsDoctorPermission]

    def get_queryset(self):
        user = self.request.user
        return User\
            .objects\
            .prefetch_related('user_relationships', 'doctor_relationships')\
            .filter(user_relationships__id__in=[r.id for r in user.doctor_relationships.all()])


class ProfileView(IsAuthenticatedView,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin):
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user

    def get(self, request):
        return self.retrieve(request)

    def put(self, request):
        return self.partial_update(request)


class PatientsListView(PatientBaseView, mixins.ListModelMixin):
    serializer_class = PatientSerializer

    def get(self, request):
        return self.list(request)


class PatientView(PatientBaseView, mixins.RetrieveModelMixin):
    serializer_class = PatientRecordsSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)


class RelationshipBaseView(IsAuthenticatedView):
    serializer_class = RelationshipSerializer

    def get_queryset(self):
        user = self.request.user
        query = Q(user=user) | Q(doctor=user)
        return Relationship.objects.filter(query)


class RelationshipListView(RelationshipBaseView,
                           mixins.ListModelMixin):
    def get(self, request):
        return self.list(request)


class RelationshipRetrieveDestroyView(RelationshipBaseView,
                                      mixins.DestroyModelMixin,
                                      mixins.RetrieveModelMixin):

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)


class PermissionsBaseView(IsAuthenticatedView):
    serializer_class = PermissionsSerializer

    def get_queryset(self):
        return RelationshipPermission.objects\
            .prefetch_related('relationship')\
            .filter(relationship__user__id=self.request.user.id)


class PermissionsListView(PermissionsBaseView, mixins.ListModelMixin):
    def get(self, request):
        return self.list(request)


class PermissionRetrieveUpdateDestroyView(PermissionsBaseView,
                                          mixins.RetrieveModelMixin,
                                          mixins.DestroyModelMixin,
                                          mixins.UpdateModelMixin):

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.partial_update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)


class BecomeDoctorView(IsAuthenticatedView, mixins.UpdateModelMixin):
    def get_serializer(self, *args, **kwargs):
        kwargs['data'] = {'is_doctor': True}
        return BecomeDoctorSerializer(*args, **kwargs)

    def get_object(self):
        return self.request.user

    @extend_schema(
        request=None,
        responses=None
    )
    def post(self, request, *args, **kwargs):
        if(self.request.user.is_doctor):
            return Response({'error': 'user is already a doctor.'}, status.HTTP_400_BAD_REQUEST)

        response = self.partial_update(request, *args, **kwargs)
        response.data = None
        return response

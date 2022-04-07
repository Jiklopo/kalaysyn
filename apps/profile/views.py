from rest_framework import mixins
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from apps.common.views import IsAuthenticatedView
from apps.common.permissions import IsDoctorPermission
from apps.profile.serializers import BecomeDoctorSerializer, PatientRecordsSerializers, ProfileSerializer


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


class PatientRecordsView(APIView):
    permission_classes = [IsDoctorPermission]

    def get(self, request):
        patients = [relationship.user for relationship in request.user.doctor_relationships.all()]
        serializer = PatientRecordsSerializers(instance=patients, many=True)
        return Response(data=serializer.data)


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
            return Response({'error': 'user is already a doctor'}, status.HTTP_400_BAD_REQUEST)

        response = self.partial_update(request, *args, **kwargs)
        response.data = None
        return response

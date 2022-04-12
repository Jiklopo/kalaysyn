from rest_framework import mixins

from apps.common.views import IsAuthenticatedView
from apps.profile.serializers import PermissionsSerializer
from apps.qr.models import RelationshipPermission


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
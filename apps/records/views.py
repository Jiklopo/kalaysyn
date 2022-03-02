from rest_framework import mixins

from apps.common.mixins import CreateAndAddUserMixin
from apps.common.views import IsAuthenticatedView
from apps.records.models import Record
from apps.records.serializers import RecordSerializer


class RecordListCreateView(IsAuthenticatedView,
                           CreateAndAddUserMixin,
                           mixins.ListModelMixin):
    serializer_class = RecordSerializer

    def get_queryset(self):
        qs = Record.objects.filter(user=self.request.user)
        return qs

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
        qs = Record.objects.filter(user=self.request.user)
        return qs

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

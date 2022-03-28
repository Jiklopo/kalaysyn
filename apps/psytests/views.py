from rest_framework import mixins

from apps.common.views import IsAuthenticatedView
from apps.psytests.models import PsyTest
from apps.psytests.serializers import PsyTestSerializer


class ListPsyTestsView(IsAuthenticatedView, mixins.ListModelMixin):
    queryset = PsyTest.objects.all()
    serializer_class = PsyTestSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

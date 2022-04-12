from django.db.models import Q
from rest_framework import mixins

from apps.common.views import IsAuthenticatedView
from apps.profile.serializers import RelationshipSerializer
from apps.qr.models import Relationship


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
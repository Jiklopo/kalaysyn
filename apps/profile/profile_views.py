from rest_framework import mixins
from apps.common.views import IsAuthenticatedView
from apps.profile.serializers import ProfileSerializer


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

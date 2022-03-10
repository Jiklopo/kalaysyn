from rest_framework import mixins
from apps.common.mixins import CreateAndAddUserMixin, UserSpecificQuerysetMixin

from apps.common.views import IsAuthenticatedView
from apps.goals.models import Goal, GoalRecord, Roadmap
from apps.goals.serializers import GoalRecordSerializer, GoalSerializer, RoadmapSerializer


class GoalsCreateListView(IsAuthenticatedView,
                          mixins.CreateModelMixin,
                          mixins.ListModelMixin
                          ):
    serializer_class = GoalSerializer
    queryset = Goal.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GoalsRetrieveUpdateDestroyView(IsAuthenticatedView,
                                     mixins.RetrieveModelMixin,
                                     mixins.UpdateModelMixin,
                                     mixins.DestroyModelMixin
                                     ):
    serializer_class = GoalSerializer
    queryset = Goal.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class RoadmapCreateListView(IsAuthenticatedView,
                            mixins.CreateModelMixin,
                            mixins.ListModelMixin
                            ):
    serializer_class = RoadmapSerializer
    queryset = Roadmap.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RoadmapRetrieveUpdateDelete(IsAuthenticatedView,
                                  mixins.RetrieveModelMixin,
                                  mixins.UpdateModelMixin,
                                  mixins.DestroyModelMixin
                                  ):
    serializer_class = RoadmapSerializer
    queryset = Roadmap.objects.all().prefetch_related('goals')

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class GoalRecordCreateListView(IsAuthenticatedView,
                               CreateAndAddUserMixin,
                               UserSpecificQuerysetMixin,
                               mixins.ListModelMixin
                               ):
    serializer_class = GoalRecordSerializer
    queryset = GoalRecord.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GoalRecordRetrieveUpdateDelete(IsAuthenticatedView,
                                     mixins.RetrieveModelMixin,
                                     mixins.UpdateModelMixin,
                                     mixins.DestroyModelMixin
                                     ):
    serializer_class = GoalRecordSerializer
    queryset = GoalRecord.objects.all().prefetch_related('goal')

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

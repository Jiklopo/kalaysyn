from rest_framework import mixins
from apps.common.filters import UserFieldFilter
from apps.common.mixins import CreateAndAddUserMixin

from apps.common.views import IsAuthenticatedView
from apps.goals.models import Goal, GoalRecord, Roadmap
from apps.goals.serializers import GoalRecordSerializer, GoalSerializer, RoadmapInputSerializer, RoadmapOutputSerializer


class GoalsCreateListView(IsAuthenticatedView,
                          CreateAndAddUserMixin,
                          mixins.ListModelMixin
                          ):
    serializer_class = GoalSerializer
    queryset = Goal.objects.all()
    user_field = 'created_by'
    allow_null = True
    filter_backends = [UserFieldFilter]

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GoalRetrieveUpdateDestroyView(IsAuthenticatedView,
                                    mixins.RetrieveModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.DestroyModelMixin
                                    ):
    serializer_class = GoalSerializer
    queryset = Goal.objects.all()
    user_field = 'created_by'
    allow_null = True
    filter_backends = [UserFieldFilter]

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
    queryset = Roadmap.objects.prefetch_related('goals')
    user_field = 'created_by'
    allow_null = True
    filter_backends = [UserFieldFilter]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RoadmapOutputSerializer
        return RoadmapInputSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RoadmapRetrieveUpdateDelete(IsAuthenticatedView,
                                  mixins.RetrieveModelMixin,
                                  mixins.UpdateModelMixin,
                                  mixins.DestroyModelMixin
                                  ):
    queryset = Roadmap.objects.prefetch_related('goals')
    user_field = 'created_by'
    allow_null = True
    filter_backends = [UserFieldFilter]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RoadmapOutputSerializer
        return RoadmapInputSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class GoalRecordCreateListView(IsAuthenticatedView,
                               CreateAndAddUserMixin,
                               mixins.ListModelMixin
                               ):
    serializer_class = GoalRecordSerializer
    queryset = GoalRecord.objects.all()
    filter_backends = [UserFieldFilter]

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
    filter_backends = [UserFieldFilter]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

from drf_spectacular.utils import OpenApiParameter, extend_schema
from drf_spectacular.types import OpenApiTypes
from rest_framework import mixins

from apps.common.filters import DateRangeFilter, UserFieldFilter
from apps.common.mixins import CreateAndAddUserMixin
from apps.common.views import IsAuthenticatedView
from apps.goals.models import Goal, GoalRecord, Roadmap
from apps.goals.serializers import (
    GoalRecordSerializer,
    GoalSerializer,
    RoadmapInputSerializer,
    RoadmapOutputSerializer
)


class GoalsCreateListView(IsAuthenticatedView,
                          CreateAndAddUserMixin,
                          mixins.ListModelMixin
                          ):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    filter_backends = [UserFieldFilter]
    user_field = 'created_by'
    allow_null = True

    @extend_schema(responses={201: GoalSerializer})
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GoalRetrieveUpdateDestroyView(IsAuthenticatedView,
                                    mixins.RetrieveModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.DestroyModelMixin
                                    ):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    filter_backends = [UserFieldFilter]
    user_field = 'created_by'

    def get_allow_null(self):
        if self.request.method == 'GET':
            return True
        return False

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class RoadmapCreateListView(IsAuthenticatedView,
                            CreateAndAddUserMixin,
                            mixins.ListModelMixin
                            ):
    queryset = Roadmap.objects.prefetch_related('goals')
    filter_backends = [UserFieldFilter]
    user_field = 'created_by'
    allow_null = True

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RoadmapOutputSerializer
        return RoadmapInputSerializer

    @extend_schema(responses={201: RoadmapOutputSerializer})
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RoadmapRetrieveUpdateDestroyView(IsAuthenticatedView,
                                       mixins.RetrieveModelMixin,
                                       mixins.UpdateModelMixin,
                                       mixins.DestroyModelMixin
                                       ):
    queryset = Roadmap.objects.prefetch_related('goals')
    filter_backends = [UserFieldFilter]
    user_field = 'created_by'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RoadmapOutputSerializer
        return RoadmapInputSerializer

    def get_allow_null(self):
        if self.request.method == 'GET':
            return True
        return False

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CommonRoadmapListView(IsAuthenticatedView, mixins.ListModelMixin):
    queryset = Roadmap.objects\
        .filter(created_by__isnull=True)\
        .prefetch_related('goals')
    serializer_class = RoadmapOutputSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GoalRecordCreateListView(IsAuthenticatedView,
                               CreateAndAddUserMixin,
                               mixins.ListModelMixin
                               ):
    serializer_class = GoalRecordSerializer
    queryset = GoalRecord.objects.all()
    filter_backends = [UserFieldFilter]

    @extend_schema(responses={201: GoalRecordSerializer})
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GoalRecordRetrieveUpdateDeleteView(IsAuthenticatedView,
                                         mixins.RetrieveModelMixin,
                                         mixins.UpdateModelMixin,
                                         mixins.DestroyModelMixin
                                         ):
    serializer_class = GoalRecordSerializer
    queryset = GoalRecord.objects.prefetch_related('goal')
    filter_backends = [UserFieldFilter]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class GoalRecordRangeView(IsAuthenticatedView,
                          mixins.ListModelMixin
                          ):
    serializer_class = GoalRecordSerializer
    queryset = GoalRecord.objects.prefetch_related('goal')
    filter_backends = [UserFieldFilter, DateRangeFilter]

    @extend_schema(
        description='Get user records in specified date range',
        parameters=[
            OpenApiParameter('from', OpenApiTypes.DATE,
                             description='DD-MM-YY HH:MM | Default: the beginning of times'),
            OpenApiParameter('to', OpenApiTypes.DATE,
                             description='DD-MM-YY HH:MM | Default: Now')
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

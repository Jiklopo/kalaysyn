from django.urls import path, include

from apps.goals.views import (
    GoalRecordCreateListView,
    GoalRecordRetrieveUpdateDelete,
    GoalsCreateListView,
    GoalRetrieveUpdateDestroyView,
    RoadmapCreateListView,
    RoadmapRetrieveUpdateDelete
)


goal_patterns = [
    path('', GoalsCreateListView.as_view(), name='goal-list-create'),
    path('<int:pk>/', GoalRetrieveUpdateDestroyView.as_view(),
         name='goal-update-delete'),
]

roadmap_patterns = [
    path('', RoadmapCreateListView.as_view(), name='roadmap-list-create'),
    path('<int:pk>', RoadmapRetrieveUpdateDelete.as_view(),
         name='roadmap-update-delete')
]

goal_record_patterns = [
    path('', GoalRecordCreateListView.as_view(),
         name='goal-record-list-create'),
    path('<int:pk>', GoalRecordRetrieveUpdateDelete.as_view(),
         name='goal-record-update-delete')
]


urlpatterns = [
    path('', include(goal_patterns)),
    path('roadmap/', include(roadmap_patterns)),
    path('records/', include(goal_record_patterns)),
]

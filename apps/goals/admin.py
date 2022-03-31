from django.contrib import admin
from apps.goals.models import Goal, Roadmap, RoadmapGoals


class RoadmapGoalsInline(admin.TabularInline):
    model = RoadmapGoals
    extra = 1


@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    inlines = [RoadmapGoalsInline]
    exclude = ['created_by']


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    exclude = ['created_by']

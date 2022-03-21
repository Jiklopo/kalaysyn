from django.contrib import admin
from apps.goals.models import Goal, Roadmap, RoadmapGoals


class RoadmapGoalsInline(admin.TabularInline):
    model = RoadmapGoals
    extra = 1


class RoadmapAdmin(admin.ModelAdmin):
    inlines = [RoadmapGoalsInline]
    exclude = ['created_by']


class GoalAdmin(admin.ModelAdmin):
    exclude = ['created_by']


admin.site.register(Goal, GoalAdmin)
admin.site.register(Roadmap, RoadmapAdmin)

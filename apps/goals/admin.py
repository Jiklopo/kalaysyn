from django.contrib import admin
from apps.goals.models import Goal, Roadmap, RoadmapGoals


class RoadmapGoalsInline(admin.TabularInline):
    model = RoadmapGoals
    extra = 1


class RoadmapAdmin(admin.ModelAdmin):
    inlines = [RoadmapGoalsInline]


admin.site.register(Goal)
admin.site.register(Roadmap, RoadmapAdmin)

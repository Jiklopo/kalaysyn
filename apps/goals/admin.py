from django.contrib import admin

from apps.goals.models import Goal, Roadmap

admin.site.register(Goal)
admin.site.register(Roadmap)
from django.db import models
from apps.authentication.models import User
from apps.common.models import TimeStampModel


class Goal(TimeStampModel):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    def __str__(self) -> str:
        return self.name


class Roadmap(TimeStampModel):
    goals = models.ManyToManyField(Goal, through='RoadmapGoals')
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    def __str__(self):
        return self.name


class RoadmapGoals(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE)


class GoalRecord(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    date = models.DateField('Goal date')
    is_done = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)

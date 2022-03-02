from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator

from apps.authentication.models import User
from apps.common.models import TimeStampModel
from apps.records import EmotionsTextChoices


class Record(TimeStampModel):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    rating = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)])
    description = models.TextField(default="", blank=True, null=True)
    emotions = ArrayField(
        models.CharField(max_length=16, choices=EmotionsTextChoices.choices),
        default=list
    )
    activities = ArrayField(
        models.CharField(max_length=128),
        default=list
    )

    sleep_rating = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)])
    fatigue_rating = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)])
    health_rating = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)])

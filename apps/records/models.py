from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator

from apps.authentication.models import User
from apps.common.models import TimeStampModel
from apps.records import EmotionsTextChoices


class Record(TimeStampModel):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateField()
    rating = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(5)])
    description = models.TextField(default="", blank=True, null=True)
    emotions = ArrayField(
        models.CharField(max_length=16, choices=EmotionsTextChoices.choices),
        default=list,
        null=True, blank=True
    )

    sleep_rating = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(5)],
        blank=True, null=True
    )
    fatigue_rating = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(5)],
        blank=True, null=True
    )
    health_rating = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(5)],
        blank=True, null=True
    )

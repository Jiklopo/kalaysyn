from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator

from apps.authentication.models import User
from apps.common.models import TimeStampModel
from apps.records import EmotionsTextChoices, ReportStatusChoices


class Record(TimeStampModel):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE,
        related_name='records'
    )
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

    class Meta:
        ordering = ['-date']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'date'], name='one_record_per_day')
        ]


class RecordReport(TimeStampModel):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE,
        related_name='reports'
    )
    from_date = models.DateField()
    to_date = models.DateField()
    status = models.CharField(
        max_length=16,
        choices=ReportStatusChoices.choices,
        default=ReportStatusChoices.CREATED
    )
    file = models.FileField(
        null=True, blank=True
    )

    def get_file_name(self):
        return f'{self.id}_{self.user.id}_{self.from_date}_{self.to_date}.pdf'

    def delete(self, *args, **kwargs):
        self.file.delete()
        return super().delete(*args, **kwargs)

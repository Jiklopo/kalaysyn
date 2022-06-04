from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator

from apps.authentication.models import User
from apps.common.models import TimeStampModel
from apps.records import EmotionsTextChoices, ReportStatusChoices


def get_image_path(instance, filename):
    extension = filename.split('.')[-1]
    return f'images/{instance.user.id}/{instance.id}.{extension}'


class Record(TimeStampModel):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE,
        related_name='records'
    )
    title = models.CharField(max_length=256, null=True, blank=True)
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
    image = models.ImageField(upload_to=get_image_path, null=True, blank=True)

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
        return f'reports/{self.user.id}/{self.id}_{self.from_date}_{self.to_date}.pdf'

    def delete(self, *args, **kwargs):
        self.file.delete()
        return super().delete(*args, **kwargs)

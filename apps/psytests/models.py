from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.authentication.models import User

from apps.common.models import TimeStampModel


class PsyTest(TimeStampModel):
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    rating = models.FloatField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ],
        blank=True, null=True
    )

    def __str__(self) -> str:
        return self.title


class Question(models.Model):
    test = models.ForeignKey(
        PsyTest,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    text = models.CharField(max_length=256)

    def __str__(self) -> str:
        return self.text


class Variant(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='variants'
    )
    text = models.CharField(max_length=256)
    points = models.IntegerField()

    def __str__(self) -> str:
        return self.text


class PsyTestRecord(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(PsyTest, on_delete=models.CASCADE)
    chosen_variants = models.ManyToManyField(Variant)

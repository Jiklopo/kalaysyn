from email.policy import default
from unicodedata import category
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.authentication.models import User

from apps.common.models import TimeStampModel
from apps.psytests import PsyTestCategoryChoices


class PsyTest(TimeStampModel):
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    result_map = models.JSONField(
        default=dict,
        help_text='Result mappings as a dictionary, order does not matter, e.g. {"1":"Sobaka", "8":"Psina", "3": "Pyos"}\n\
            Compute examples: 4 => Pyos | 8 => Psina | 0 => Error!!!'
    )
    category = models.CharField(
        max_length=16,
        choices=PsyTestCategoryChoices.choices,
        default=PsyTestCategoryChoices.OTHER.value
    )
    rating = models.FloatField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ],
        blank=True, null=True
    )
    ratings_received = models.IntegerField(default=0)

    def rate(self, rating):
        self.rating = (self.rating * self.ratings_received +
                       rating) / (self.ratings_received + 1)
        self.ratings_received += 1
        self.save()

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

    @property
    def result_points(self):
        variants = self.chosen_variants.all()
        sum = 0
        for v in variants:
            sum += v.points
        return sum

    @property
    def result(self):
        result_map = self.test.result_map
        points = [int(i) for i in result_map.keys()]
        points.sort(reverse=True)
        result_points = self.result_points
        for p in points:
            if result_points < p:
                continue

            result = result_map.get(str(p), None)
            return result

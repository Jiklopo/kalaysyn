import factory
from factory import Faker
from factory import fuzzy
from factory.django import DjangoModelFactory
from django.utils import timezone
from datetime import datetime, timedelta

from apps.authentication.models import User
from apps.records.models import Record
from apps.records import EmotionsTextChoices
from apps.authentication.tests.factories import UserFactory

EMOTIONS = [choice[0] for choice in EmotionsTextChoices.choices]


class RecordFactory(DjangoModelFactory):
    class Meta:
        model = Record

    date = fuzzy.FuzzyDate(
        datetime.now() - timedelta(days=30),
        datetime.now()
    )
    description = Faker('sentence')
    emotions = factory.List(
        [fuzzy.FuzzyChoice(EMOTIONS) for _ in range(3)]
    )
    rating = fuzzy.FuzzyInteger(1, 5)
    sleep_rating = fuzzy.FuzzyInteger(1, 5)
    fatigue_rating = fuzzy.FuzzyInteger(1, 5)
    health_rating = fuzzy.FuzzyInteger(1, 5)

    @classmethod
    def build(cls, **kwargs):
        user = User.objects.order_by('?').first()
        if not user:
            user = UserFactory.create()
        kwargs['user'] = user
        return super().build(**kwargs)

    @classmethod
    def create(cls, **kwargs):
        instance = cls.build(**kwargs)
        return instance.save()

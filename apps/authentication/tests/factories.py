from factory import Faker
from factory.django import DjangoModelFactory
from apps.authentication.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker('user_name')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    phone_number = Faker('phone_number')
    is_premium = Faker('boolean')
    is_doctor = Faker('boolean')
    password = '1234'

    @classmethod
    def create(cls, **kwargs):
        password = kwargs.pop('password', '1234')
        instance: User = cls.build(**kwargs)
        instance.set_password(password)
        return instance.save()

from django.db import IntegrityError
from rest_framework.exceptions import ParseError

from .models import User


def create_user(*, username, password, **kwargs) -> User:
    try:
        user = User.objects.create_user(username=username, password=password, **kwargs)
    except IntegrityError as e:
        raise ParseError(str(e))

    return user

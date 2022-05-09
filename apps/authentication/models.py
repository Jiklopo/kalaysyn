import uuid
from datetime import datetime, timedelta, timezone
from os import urandom
from struct import unpack

from django.db import models
from django.contrib.auth.models import AbstractUser

from configuration.settings import CODE_VALID_SECONDS
from apps.common.models import TimeStampModel


def generate_code():
    random_bytes = urandom(4)
    random_number = unpack('i', random_bytes)[0]
    return str(random_number)[-6:]


class User(AbstractUser, TimeStampModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=32, null=True, blank=True)
    is_premium = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class PasswordResetCode(TimeStampModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reset_codes'
    )
    code = models.CharField(max_length=6, default=generate_code)
    was_validated = models.BooleanField(default=False)

    @property
    def is_valid(self):
        diff = datetime.now(timezone.utc) - self.created_at
        return diff < timedelta(seconds=CODE_VALID_SECONDS)

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.common.models import TimeStampModel


class User(AbstractUser, TimeStampModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=16, default='')
    is_premium = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)

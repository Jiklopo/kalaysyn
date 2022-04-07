import uuid
from datetime import datetime, timedelta, timezone
from django.db import models

from configuration.settings import CODE_VALID_SECONDS
from apps.authentication.models import User
from apps.common.models import TimeStampModel


class RelationshipCode(TimeStampModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    doctor = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='user_relationship_codes',
        null=True,
        blank=True
    )

    @property
    def is_valid(self):
        "Returns if code is still valid"
        diff = datetime.now(timezone.utc) - self.created_at
        return diff < timedelta(seconds=CODE_VALID_SECONDS)

    @property
    def valid_until(self):
        "Returns code validity time"
        return self.created_at + timedelta(seconds=CODE_VALID_SECONDS)


class RelationshipPermission(TimeStampModel):
    can_view = models.BooleanField(default=True)


class Relationship(TimeStampModel):
    doctor = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='doctor_relationships'
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='user_relationships'
    )
    permissions = models.OneToOneField(
        RelationshipPermission, 
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            name='unique-doctor-patient-relationship', fields=['doctor', 'user'])]

    def save(self, *args, **kwargs):
        if self.permissions is None:
            self.permissions = RelationshipPermission.objects.create(relationship=self)
            
        super().save(*args, **kwargs)
        return self

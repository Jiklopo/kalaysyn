from django.db import IntegrityError
from apps.common.serializers import UniqueConstraintModelSerializer

from apps.records.models import Record


class RecordSerializer(UniqueConstraintModelSerializer):
    class Meta:
        model = Record
        exclude = ['user']
        read_only_fields = ['id']

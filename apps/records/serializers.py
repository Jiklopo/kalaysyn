from rest_framework import serializers

from apps.common.serializers import UniqueConstraintModelSerializer
from apps.records.models import Record, RecordReport


class RecordSerializer(UniqueConstraintModelSerializer):
    class Meta:
        model = Record
        exclude = ['user']
        read_only_fields = ['id']


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordReport
        fields = [
            'from_date',
            'to_date',
            'status',
            'file'
        ]
        read_only_fields = [
            'status',
            'file'
        ]

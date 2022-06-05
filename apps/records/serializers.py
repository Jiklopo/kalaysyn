from datetime import date, datetime
from rest_framework import serializers

from apps.common.serializers import UniqueConstraintModelSerializer
from apps.records.models import Record, RecordReport


class DateAsDateTimeField(serializers.DateField):
    def to_representation(self, value):
        dt = datetime.combine(value, datetime.min.time())
        return f'{dt.isoformat()}.785043Z'


class RecordSerializer(UniqueConstraintModelSerializer):
    class Meta:
        model = Record
        exclude = ['user']
        read_only_fields = ['id', 'image']

class RecordOutputSerializer(UniqueConstraintModelSerializer):
    created_at = DateAsDateTimeField(source='date')

    class Meta:
        model = Record
        exclude = ['user', 'date']
        read_only_fields = ['id', 'image']


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
            'file',
        ]

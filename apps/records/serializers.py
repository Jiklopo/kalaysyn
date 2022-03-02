from rest_framework import serializers

from apps.records.models import Record


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = [
            'id',
            'created_at',
            'updated_at',
            'date',
            'rating',
            'description',
            'emotions',
            'activities',
            'sleep_rating',
            'fatigue_rating',
            'health_rating'
        ]
        read_only_fields = ['id']

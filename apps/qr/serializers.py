from dataclasses import fields
from rest_framework import serializers

from apps.qr.models import RelationshipCode


class GenerateCodeSerializer(serializers.ModelSerializer):
    doctor_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = RelationshipCode
        fields = ['id', 'doctor_id', 'created_at', 'valid_until']
        read_only_fields = ['id', 'created_at', 'valid_until']


class LinkCodeSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField()

    class Meta:
        model = RelationshipCode
        fields = ['doctor', 'user_id']
        read_only_fields = ['doctor']

from dataclasses import fields
from rest_framework import serializers

from apps.qr.models import RelationshipCode


class GenerateCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelationshipCode
        fields = ['id', 'doctor', 'created_at', 'valid_until']
        read_only_fields = ['id', 'created_at', 'valid_until']
        extra_kwargs = {
            'doctor': {'write_only': True}
        }


class LinkCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelationshipCode
        fields = ['doctor', 'user']
        read_only_fields = ['doctor']

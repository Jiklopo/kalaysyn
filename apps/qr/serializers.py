from rest_framework import serializers
from apps.authentication.models import User

from apps.qr.models import Relationship, RelationshipCode


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


class RelationshipSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    doctor = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Relationship
        fields = '__all__'

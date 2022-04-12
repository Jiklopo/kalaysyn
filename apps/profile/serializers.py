from rest_framework import serializers
from apps.qr.models import Relationship, RelationshipPermission

from apps.records.models import Record
from apps.authentication.models import User


class InlineRecordSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Record
        exclude = [
            'description'
        ]


class PermissionsSerializer(serializers.ModelSerializer):
    relationship = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = RelationshipPermission
        exclude = ['id']


class RelationshipSerializer(serializers.ModelSerializer):
    doctor = serializers.StringRelatedField()
    permissions = PermissionsSerializer()

    def update(self, instance, validated_data):
        return self.permissions.update(self.permissions.instance, validated_data=validated_data.get('permissions'))

    class Meta:
        model = Relationship
        exclude = ['user']


class ProfileSerializer(serializers.ModelSerializer):
    user_relationships = RelationshipSerializer(
        many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'is_premium',
            'is_doctor',
            'user_relationships',
        ]
        read_only_fields = [
            'username',
            'is_premium'
        ]


class BecomeDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_doctor']


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
        ]


class PatientRecordsSerializer(serializers.ModelSerializer):
    records = InlineRecordSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'records'
        ]

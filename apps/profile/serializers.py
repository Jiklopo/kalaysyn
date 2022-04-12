from rest_framework import serializers
from apps.qr.models import Relationship, RelationshipPermission

from apps.records.models import Record
from apps.authentication.models import User


class InlinePermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelationshipPermission
        exclude = ['id']


class InlineRelationshipSerializer(serializers.ModelSerializer):
    doctor = serializers.StringRelatedField(read_only=True)
    permissions = InlinePermissionsSerializer(read_only=True)

    class Meta:
        model = Relationship
        exclude = ['user', 'id']


class ProfileSerializer(serializers.ModelSerializer):
    user_relationships = InlineRelationshipSerializer(
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


class InlineRecordSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Record
        exclude = [
            'description'
        ]


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


class BecomeDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_doctor']

from rest_framework import serializers

from apps.records.models import Record
from apps.authentication.models import User


class ProfileSerializer(serializers.ModelSerializer):
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


class PatientRecordsSerializers(serializers.ModelSerializer):
    records = InlineRecordSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'records'
        ]


class BecomeDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_doctor']

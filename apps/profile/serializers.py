from rest_framework import serializers

from apps.authentication.models import User


class BecomeDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_doctor']

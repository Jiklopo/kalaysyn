from rest_framework import serializers

from apps.authentication.models import User


class UserInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'phone_number']

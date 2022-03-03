from rest_framework import serializers

from apps.authentication.models import User


class UserInputSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'phone_number'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField()

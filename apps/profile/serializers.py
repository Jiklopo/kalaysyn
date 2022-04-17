from rest_framework import serializers
from apps.qr.models import Relationship, RelationshipPermission

from apps.records.models import Record
from apps.authentication.models import User


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
        ]


class PatientRecordsSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, data=None, permission=None, **kwargs):
        super().__init__(instance, data, **kwargs)
        self.update_permissions(permission)

    def update_permissions(self, permission: RelationshipPermission):
        if permission is None:
            return
        if not permission.can_view_emotions:
            self.fields.pop('emotions')
        if not permission.can_view_rating:
            self.fields.pop('rating')
        if not permission.can_view_health_rating:
            self.fields.pop('health_rating')
        if not permission.can_view_sleep_rating:
            self.fields.pop('sleep_rating')
        if not permission.can_view_fatigue_rating:
            self.fields.pop('fatigue_rating')

    class Meta:
        model = Record
        exclude = [
            'description',
            'user',
        ]


class PermissionsSerializer(serializers.ModelSerializer):
    relationship = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = RelationshipPermission
        fields = '__all__'


class RelationshipSerializer(serializers.ModelSerializer):
    doctor = serializers.StringRelatedField()
    permissions = PermissionsSerializer()

    class Meta:
        model = Relationship
        exclude = ['user']


class ProfileSerializer(serializers.ModelSerializer):
    user_relationships = RelationshipSerializer(
        many=True, read_only=True)
    doctor_relationships = RelationshipSerializer(
        many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'is_premium',
            'is_doctor',
            'user_relationships',
            'doctor_relationships'
        ]
        read_only_fields = [
            'id',
            'username',
            'is_premium'
        ]

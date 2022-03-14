from dataclasses import fields
from rest_framework import serializers

from apps.goals.models import Goal, GoalRecord, Roadmap


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
        ]


class RoadmapInputSerializer(serializers.ModelSerializer):
    goals = serializers.PrimaryKeyRelatedField(
        queryset=Goal.objects.all(),
        write_only=True,
        many=True
    )

    class Meta:
        model = Roadmap
        fields = '__all__'
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
        ]


class RoadmapOutputSerializer(serializers.ModelSerializer):
    goals = GoalSerializer(many=True, read_only=True)

    class Meta:
        model = Roadmap
        fields = '__all__'

class GoalRecordSerializer(serializers.ModelSerializer):
    goal = serializers.PrimaryKeyRelatedField(queryset=Goal.objects.all())

    class Meta:
        model = GoalRecord
        fields = [
            'id',
            'goal',
            'date',
            'is_done',
            'description',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'goal',
            'created_at',
            'updated_at',
        ]

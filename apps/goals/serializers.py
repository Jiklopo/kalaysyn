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


class RoadmapSerializer(serializers.ModelSerializer):
    goals = GoalSerializer(many=True)

    class Meta:
        models = Roadmap
        fields = '__all__'
        read_only_fields = [
            'id',
            'created_at',
            'updated_at'
        ]


class GoalRecordSerializer(serializers.ModelSerializer):
    goal = serializers.StringRelatedField()

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


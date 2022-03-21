from rest_framework import serializers
from rest_framework.exceptions import ParseError, NotFound

from apps.goals.models import Goal, GoalRecord, Roadmap
from apps.authentication.models import User


class GoalSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

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

    def save(self, **kwargs):
        goals = self.validated_data.get('goals', None)
        user = kwargs.get('user', None)
        if goals is None or user is None:
            raise ParseError

        for goal in goals:
            if goal.created_by is not None and goal.created_by != user:
                raise ParseError

        return super().save(**kwargs)

    class Meta:
        model = Roadmap
        exclude = ['created_by']
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

    def save(self, **kwargs):
        goal = self.validated_data.get('goal', None)
        user = kwargs.get('user', None)
        if goal is None or user is None:
            raise ParseError

        if goal.created_by is not None and goal.created_by != user:
            raise ParseError

        return super().save(**kwargs)

    class Meta:
        model = GoalRecord
        fields = [
            'id',
            'goal',
            'date',
            'user',
            'is_done',
            'description',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'goal',
            'user',
            'created_at',
            'updated_at',
        ]

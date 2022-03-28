from dataclasses import fields
from rest_framework import serializers

from apps.psytests.models import PsyTest, Question, Variant


class VariantNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = [
            'text',
            'points'
        ]


class QuestionNestedSerializer(serializers.ModelSerializer):
    variants = VariantNestedSerializer(
        queryset=Variant.objects.all(),
        many=True
    )

    class Meta:
        model = Question
        fields = [
            'text',
            'variants'
        ]


class PsyTestSerializer(serializers.ModelSerializer):
    questions = QuestionNestedSerializer(
        queryset=Question.objects.all(),
        many=True
    )

    class Meta:
        model = PsyTest
        fields = '__all__'


class PsyTestRecordSerializer(serializers.ModelSerializer):
    pass
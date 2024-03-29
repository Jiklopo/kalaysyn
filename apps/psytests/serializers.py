from unittest import result
from rest_framework import serializers

from apps.psytests.models import PsyTest, PsyTestRecord, Question, Variant


class VariantNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = [
            'id',
            'text',
            'points'
        ]


class QuestionNestedSerializer(serializers.ModelSerializer):
    variants = VariantNestedSerializer(
        read_only=True,
        many=True
    )

    class Meta:
        model = Question
        fields = [
            'id',
            'text',
            'variants'
        ]


class PsyTestDetailsSerializer(serializers.ModelSerializer):
    questions = QuestionNestedSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = PsyTest
        fields = '__all__'


class PsyTestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PsyTest
        exclude = ['result_map']


class PsyTestRatingInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = PsyTest
        fields = ['rating']


class PsyTestRatingOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = PsyTest
        fields = '__all__'


class ChosenVariantsField(serializers.PrimaryKeyRelatedField):
        def get_queryset(self):
            qs = super().get_queryset()
            test_id = self.context['request'].data.get('test')
            if test_id is not None:
                qs = qs.filter(question__test_id=test_id)
            return qs

class PsyTestRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PsyTestRecord
        exclude = ['user']

    
    test = serializers.PrimaryKeyRelatedField(queryset=PsyTest.objects.all())
    result_points = serializers.IntegerField(read_only=True)
    result = serializers.CharField(read_only=True)
    chosen_variants = ChosenVariantsField(
        queryset=Variant.objects.all(),
        many=True
    )

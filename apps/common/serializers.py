from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ParseError


class UniqueConstraintModelSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        try:
            return super().save(**kwargs)
        except IntegrityError as e:
            msg = str(e).split('\n')[1].split(':')[1].strip()
            raise ParseError(msg)

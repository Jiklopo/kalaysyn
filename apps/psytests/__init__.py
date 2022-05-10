from django.db import models


class PsyTestCategoryChoices(models.TextChoices):
    CHARACTER = 'CHARACTER', 'Character'
    RELATIONS = 'RELATIONS', 'Relations'
    SOCIAL = 'SOCIAL', 'Social'
    FAMILY = 'FAMILY', 'Family'
    FEELINGS = 'FEELINGS', 'Bad Feelings'
    OTHER = 'OTHER', 'Other'

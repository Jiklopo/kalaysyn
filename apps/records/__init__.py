from django.db import models


class ReportStatusChoices(models.TextChoices):
    CREATED = 'CREATED', 'Created'
    PROCESSING = 'PROCESSING', 'Processing'
    READY = 'READY', 'Ready'
    ERROR = 'ERROR', 'Error'

class EmotionsTextChoices(models.TextChoices):
    # Note for my Android friends:
    # VAR_NAME = DB_VALUE, HUMAN_READABLE_NAME
    # E.g. VAR_NAME = ANGER; DB_VALUE = ANGER; HUMAN_READABLE_NAME = Anger

    # VAR_NAME is local, you do not need to care about that
    # DB_VALUE is how it is actually stored in DB, you will send and receive this value
    # HUMAN_READABLE_NAME is how it is displayed on admin page, no need to care as well

    # Main Emotions
    ANGER = 'ANGER', 'Anger'
    SADNESS = 'SADNESS', 'Sadness'
    SURPRISE = 'SURPRISE', 'Surprise'
    JOY = 'JOY', 'Joy'
    LOVE = 'LOVE', 'Love'
    FEAR = 'FEAR', 'Fear'

    # Anger subtypes
    RAGE = 'RAGE', 'Rage'
    EXASPERATION = 'EXASPERATION', 'Exasperation'
    IRRITATION = 'IRRITATION', 'Irritation'
    ENVY = 'ENVY', 'Envy'
    DISGUST = 'DISGUST', 'Disgust'

    # Sadness subtypes
    SUFFERING = 'SUFFER', 'Suffering'
    DISAPPOINTMENT = 'DISSAPPOINT', 'Disappointment'
    SHAME = 'SHAME', 'Shame'
    NEGLECTION = 'NEGLECTION', 'Neglection'
    DESPAIR = 'DESPAIR', 'Despair'

    # Surprise subtypes
    STUN = 'STUN', 'Stun'
    CONFUSION = 'CONFUSION', 'Confusion'
    AMAZEMENT = 'AMAZEMENT', 'Amazement'
    OVERCOME = 'OVERCOME', 'Overcome'
    MOVED = 'MOVED', 'Moved'

    # Joy subtypes
    CONTENT = 'CONTENT', 'Content'
    HAPPINESS = 'HAPPY', 'Happiness'
    CHEER = 'CHEER', 'Cheer'
    PROUDNESS = 'PROUD', 'Proudness'
    OPTIMISM = 'OPTIMISM', 'Optimism'
    ENTHUSIASM = 'ENTHUSIASM', 'Enthusiasm'
    ELATION = 'ELATION', 'Elation'
    ENTHRALLED = 'ENTHRALLED', 'Enthralled'

    # Love subtypes
    AFFECTION = 'AFFECTION', 'Affection'
    LONGING = 'LONGING', 'Longing'
    DESIRE = 'DESIRE', 'Desire'
    TENDERNESS = 'TENDERNESS', 'Tenderness'
    PEACE = 'PEACE', 'Peace'

    # Fear subtypes
    SCARE = 'SCARE', 'Scare'
    TERROR = 'TERROR', 'Terror'
    INSECURE = 'INSECURE', 'Insecure'
    NERVOUSNESS = 'NERVOUSNESS', 'Nervousness'
    HORROR = 'HORROR', 'Horror'

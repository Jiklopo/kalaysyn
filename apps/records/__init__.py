from django.db import models


class EmotionsTextChoices(models.TextChoices):
    # Note for my Android friends:
    # VAR_NAME = DB_VALUE, HUMAN_READABLE_NAME
    # E.g. VAR_NAME = ANGER; DB_VALUE = ANGR; HUMAN_READABLE_NAME = Anger

    # VAR_NAME is local, you do not need to care about that
    # DB_VALUE is how it is actually stored in DB, you will send and receive this value
    # HUMAN_READABLE_NAME is how it is displayed on admin page, no need to care as well

    # Main Emotions
    ANGER = 'ANGR', 'Anger'
    SADNESS = 'SADNESS', 'Sadness'
    SURPRISE = 'SURPRISE', 'Surprise'
    JOY = 'JOY', 'Joy'
    LOVE = 'LOVE', 'Love'
    FEAR = 'FEAR', 'Fear'

    # Anger subtypes
    RAGE = 'RAGE', 'Rage'
    EXASPERATION = 'EXASPERATION', 'Exasperation'
    IRRITATION = 'IRRTN', 'Irritation'
    ENVY = 'ENVY', 'Envy'
    DISGUST = 'DISGUST', 'Disgust'

    # Sadness subtypes
    SUFFERING = 'SUFFER', 'Suffering'
    DISAPPOINTMENT = 'DISSAPPOINT', 'Disappointment'
    SHAME = 'SHAME', 'Shame'
    NEGLECTION = 'NGLCT', 'Neglection'
    DESPAIR = 'DSPR', 'Despair'

    # Surprise subtypes
    STUN = 'STUN', 'Stun'
    CONFUSION = 'CONF', 'Confusion'
    AMAZEMENT = 'AMAZE', 'Amazement'
    OVERCOME = 'OVERCOME', 'Overcome'
    MOVED = 'MOVED', 'Moved'

    # Joy subtypes
    CONTENT = 'CNTNT', 'Content'
    HAPPINESS = 'HAPPY', 'Happiness'
    CHEER = 'CHEER', 'Cheer'
    PROUDNESS = 'PROUD', 'Proudness'
    OPTIMISM = 'OPTIM', 'Optimism'
    ENTHUSIASM = 'ENTHSM', 'Enthusiasm'
    ELATION = 'ELTN', 'Elation'
    ENTHRALLED = 'ENTHRL', 'Enthralled'

    # Love subtypes
    AFFECTION = 'AFFCTN', 'Affection'
    LONGING = 'LONGING', 'Longing'
    DESIRE = 'DSR', 'Desire'
    TENDERNESS = 'TNDRNS', 'Tenderness'
    PEACE = 'PEACE', 'Peace'

    # Fear subtypes
    SCARE = 'SCARE', 'Scare'
    TERROR = 'TERROR', 'Terror'
    INSECURE = 'INSEC', 'Insecure'
    NERVOUSNESS = 'NRVSNS', 'Nervousness'
    HORROR = 'HORROR', 'Horror'

# Generated by Django 4.0.2 on 2022-03-02 15:29

from django.conf import settings
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateTimeField()),
                ('rating', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('emotions', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('ANGR', 'Anger'), ('SADNESS', 'Sadness'), ('SURPRISE', 'Surprise'), ('JOY', 'Joy'), ('LOVE', 'Love'), ('FEAR', 'Fear'), ('RAGE', 'Rage'), ('EXASPERATION', 'Exasperation'), ('IRRTN', 'Irritation'), ('ENVY', 'Envy'), ('DISGUST', 'Disgust'), ('SUFFER', 'Suffering'), ('DISSAPPOINT', 'Disappointment'), ('SHAME', 'Shame'), ('NGLCT', 'Neglection'), ('DSPR', 'Despair'), ('STUN', 'Stun'), ('CONF', 'Confusion'), ('AMAZE', 'Amazement'), ('OVERCOME', 'Overcome'), ('MOVED', 'Moved'), ('CNTNT', 'Content'), ('HAPPY', 'Happiness'), ('CHEER', 'Cheer'), ('PROUD', 'Proudness'), ('OPTIM', 'Optimism'), ('ENTHSM', 'Enthusiasm'), ('ELTN', 'Elation'), ('ENTHRL', 'Enthralled'), ('AFFCTN', 'Affection'), ('LONGING', 'Longing'), ('DSR', 'Desire'), ('TNDRNS', 'Tenderness'), ('PEACE', 'Peace'), ('SCARE', 'Scare'), ('TERROR', 'Terror'), ('INSEC', 'Insecure'), ('NRVSNS', 'Nervousness'), ('HORROR', 'Horror')], max_length=16), default=list, size=None)),
                ('activities', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=128), default=list, size=None)),
                ('sleep_rating', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('fatigue_rating', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('health_rating', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

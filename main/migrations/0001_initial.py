# Generated by Django 3.1.1 on 2020-09-06 15:07

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import main.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EventInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('rating', models.IntegerField(validators=[main.models.validate_rating_value])),
                ('description', models.TextField(blank=True, max_length=300, null=True)),
                ('emotions', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('FR', 'Fear'), ('AR', 'Anger'), ('SD', 'Sadness'), ('JY', 'Joy'), ('DG', 'Disgust'), ('SP', 'Surprise'), ('TR', 'Trust'), ('AP', 'Anticipation')], max_length=30), blank=True, null=True, size=None)),
                ('is_hungry', models.BooleanField()),
                ('auth', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DayInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('rating', models.IntegerField(validators=[main.models.validate_rating_value])),
                ('emotions', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('FR', 'Fear'), ('AR', 'Anger'), ('SD', 'Sadness'), ('JY', 'Joy'), ('DG', 'Disgust'), ('SP', 'Surprise'), ('TR', 'Trust'), ('AP', 'Anticipation')], max_length=30), blank=True, null=True, size=None)),
                ('description', models.TextField(blank=True, max_length=300, null=True)),
                ('fatigue_rating', models.IntegerField(blank=True, null=True, validators=[main.models.validate_rating_value])),
                ('sleep_rating', models.IntegerField(blank=True, null=True, validators=[main.models.validate_rating_value])),
                ('productivity_rating', models.IntegerField(blank=True, null=True, validators=[main.models.validate_rating_value])),
                ('thins_done', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, null=True, size=None)),
                ('appetite_rate', models.IntegerField(blank=True, null=True, validators=[main.models.validate_rating_value])),
                ('meals_eaten', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, null=True, size=None)),
                ('communication_rate', models.IntegerField(blank=True, null=True, validators=[main.models.validate_rating_value])),
                ('auth', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='dayinfo',
            constraint=models.UniqueConstraint(fields=('auth', 'date'), name='unique_user_date'),
        ),
    ]

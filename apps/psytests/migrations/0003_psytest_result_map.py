# Generated by Django 4.0.2 on 2022-05-07 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psytests', '0002_psytest_ratings_received_alter_psytest_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='psytest',
            name='result_map',
            field=models.JSONField(default=dict),
        ),
    ]

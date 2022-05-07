# Generated by Django 4.0.2 on 2022-04-14 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qr', '0003_remove_relationshippermission_relationship_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='relationshippermission',
            name='can_view',
        ),
        migrations.AddField(
            model_name='relationshippermission',
            name='can_view_emotions',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='relationshippermission',
            name='can_view_fatigue_rating',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='relationshippermission',
            name='can_view_health_rating',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='relationshippermission',
            name='can_view_rating',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='relationshippermission',
            name='can_view_sleep_rating',
            field=models.BooleanField(default=True),
        ),
    ]
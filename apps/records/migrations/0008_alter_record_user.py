# Generated by Django 4.0.2 on 2022-04-07 17:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('records', '0007_alter_record_options_record_one_record_per_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to=settings.AUTH_USER_MODEL),
        ),
    ]

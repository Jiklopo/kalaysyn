# Generated by Django 4.0.2 on 2022-04-05 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0005_remove_record_activities'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='date',
            field=models.DateField(),
        ),
    ]

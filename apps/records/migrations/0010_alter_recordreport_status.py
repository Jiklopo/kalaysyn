# Generated by Django 4.0.2 on 2022-05-09 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0009_recordreport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recordreport',
            name='status',
            field=models.CharField(choices=[('CREATED', 'Created'), ('PROCESSING', 'Processing'), ('READY', 'Ready'), ('ERROR', 'Error')], default='CREATED', max_length=16),
        ),
    ]

# Generated by Django 3.1.1 on 2020-09-26 15:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='dayinfo',
            name='unique_user_date',
        ),
        migrations.RenameField(
            model_name='dayinfo',
            old_name='thins_done',
            new_name='things_done',
        ),
        migrations.RenameField(
            model_name='dayinfo',
            old_name='auth',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='eventinfo',
            old_name='auth',
            new_name='user',
        ),
        migrations.AddField(
            model_name='eventinfo',
            name='name',
            field=models.CharField(default='no_name', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dayinfo',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='eventinfo',
            name='is_hungry',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddConstraint(
            model_name='dayinfo',
            constraint=models.UniqueConstraint(fields=('user', 'date'), name='unique_user_date'),
        ),
    ]

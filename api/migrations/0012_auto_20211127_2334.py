# Generated by Django 3.2.7 on 2021-11-27 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_stockpile_stocks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='change_day',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='change_week',
        ),
        migrations.AddField(
            model_name='stock',
            name='day_change',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='stock',
            name='week_change',
            field=models.JSONField(default=list),
        ),
    ]

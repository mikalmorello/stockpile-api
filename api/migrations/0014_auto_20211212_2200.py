# Generated by Django 3.2.7 on 2021-12-12 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_alter_stock_last_refreshed'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockpile',
            name='day_change',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='stockpile',
            name='week_change',
            field=models.FloatField(default=0),
        ),
    ]
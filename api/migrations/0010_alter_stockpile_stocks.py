# Generated by Django 3.2.7 on 2021-11-27 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_stockpile_stocks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockpile',
            name='stocks',
            field=models.ManyToManyField(related_name='stockpiles', to='api.Symbol'),
        ),
    ]

# Generated by Django 3.2.7 on 2021-11-28 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20211127_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='last_refreshed',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

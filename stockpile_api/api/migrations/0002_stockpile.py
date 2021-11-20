# Generated by Django 3.2.7 on 2021-11-20 19:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stockpile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='created', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

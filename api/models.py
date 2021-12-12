from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

# Create your models here.


class User(AbstractUser):
    pass


class Stockpile(models.Model):
    title = models.CharField(max_length=80)
    stocks = models.ManyToManyField("Stock", related_name="stockpiles")
    date_created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created",
        default=1
    )
    day_change = models.FloatField(default=0)
    week_change = models.FloatField(default=0)

    def __str__(self):
        return f"{self.title}"


class Symbol(models.Model):
    symbol = models.CharField(max_length=5)
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol}"


class Stock(models.Model):
    symbol = models.CharField(max_length=5)
    last_refreshed = models.DateTimeField(auto_now=True)
    daily = models.JSONField(default=list)
    day_change = models.JSONField(default=list)
    week_change = models.JSONField(default=list)

    def __str__(self):
        return f"{self.symbol}"

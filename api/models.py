from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

# Create your models here.


class User(AbstractUser):
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }


class Stockpile(models.Model):
    title = models.CharField(max_length=80)
    date_created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created",
        default=1
    )

    def __str__(self):
        return f"{self.title}"

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "creator": self.creator.username
        }


class Symbol(models.Model):
    symbol = models.CharField(max_length=5)
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol}"

    def serialize(self):
        return {
            "id": self.id,
            "symbol": self.symbol,
            "name": self.name
        }

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("stockpiles", views.stockpiles, name="stockpiles"),
    path("stockpiles/<str:stockpile_id>", views.stockpile, name="stockpile")
]

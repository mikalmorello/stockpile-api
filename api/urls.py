from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("stockpiles", views.stockpiles, name="stockpiles"),
    path("stockpiles/create", views.create_stockpile, name="create_stockpile"),
    path("stockpiles/<str:stockpile_id>", views.stockpile, name="stockpile"),
    path("users", views.users, name="users"),
    path("users/<str:user_id>", views.user, name="user"),
    path("symbols", views.symbols, name="symbols"),
    path("symbols/update", views.update_symbols, name="update_symbols"),
    path("symbols/<str:stock_symbol>", views.symbol, name="symbol"),
    path("stocks", views.stocks, name="stocks"),
    path("stocks/<str:stock_symbol>", views.stock, name="stock"),
]

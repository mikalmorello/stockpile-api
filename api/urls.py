from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("stockpiles", views.stockpiles, name="stockpiles"),
    path("stockpiles/create", views.create_stockpile, name="create_stockpile"),
    path("stockpiles/<str:stockpile_id>", views.stockpile, name="stockpile"),
    path("users", views.users, name="users"),
    path("users/active", views.active_user, name="active_user"),
    path("users/<str:user_id>", views.user, name="user"),
    path("symbols", views.symbols, name="symbols"),
    path("symbols/update", views.update_symbols, name="update_symbols"),
    path("symbols/<str:stock_symbol>", views.symbol, name="symbol"),
    path("stocks", views.stocks, name="stocks"),
    path("stocks/update", views.update_stocks, name="update_stocks"),
    path("stocks/<str:stock_symbol>", views.stock, name="stock"),
]

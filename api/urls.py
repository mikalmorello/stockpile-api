from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

app_name = "api"

urlpatterns = [
    # path('token', obtain_auth_token, name="obtain-token"),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("stockpiles", views.StockpilesView.as_view(), name="stockpiles"),
    path("stockpiles/create", views.create_stockpile, name="create_stockpile"),
    path("stockpiles/<str:stockpile_id>",
         views.StockpileView.as_view(), name="stockpile"),
    path("users", views.UsersView.as_view(), name="users"),
    path("users/active", views.active_user, name="active_user"),
    path("users/<str:user_id>", views.UserView.as_view(), name="user"),
    path("symbols", views.SymbolsView.as_view(), name="symbols"),
    path("symbols/update", views.update_symbols, name="update_symbols"),
    path("symbols/<str:stock_symbol>", views.SymbolView.as_view(), name="symbol"),
    path("stocks", views.StocksView.as_view(), name="stocks"),
    path("stocks/update", views.update_stocks, name="update_stocks"),
    path("stocks/<str:stock_symbol>", views.StockView.as_view(), name="stock"),
]

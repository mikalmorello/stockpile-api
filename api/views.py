import json
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from . import util

from .models import User, Stockpile, Symbol, Stock

# Rest Framework
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, StockpileSerializer, SymbolSerializer, StockSerializer


def index(request):
    user = request.user
    return render(request, "api/index.html", {
        "title": 'title',
        "user": user,
    })


def login_view(request):
    """
    Handle user login
    """
    # For a post request, attempt login
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            # Redirect user to posts view
            return HttpResponseRedirect(reverse("api:index"))
        else:
            # Render login view with error message
            return render(request, "api/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        # Render login view
        return render(request, "api/login.html")


def logout_view(request):
    """
    Handle user logout
    """
    # Process logout request
    logout(request)

    # Redirect user to posts view
    return HttpResponseRedirect(reverse("api:index"))


def register(request):
    """
    Handle user registration
    """
    # For a post request, attempt registration
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "api/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "api/register.html", {
                "message": "Username already taken."
            })

        # Process login request
        login(request, user)
        # Redirect user to posts view
        return HttpResponseRedirect(reverse("api:index"))
    else:
        # Render register view
        return render(request, "api/register.html")


class UsersView(APIView):
    def get(self, request, *args, **kwargs):
        # Get users data
        users = User.objects.all()
        # Serialize users
        serializer = UserSerializer(users, many=True)
        # Return response
        return Response(serializer.data)


class UserView(APIView):
    def get(self, request, *args, **kwargs):
        # Get URL parameter
        user_id = kwargs.get("user_id")
        # Get userdata
        user = User.objects.get(id=user_id)
        # Serialize user
        serializer = UserSerializer(user)
        # Return response
        return Response(serializer.data)


class StockpilesView(APIView):
    def get(self, request, *args, **kwargs):
        # Get stockpiles data
        stockpiles = Stockpile.objects.all()
        # Serialize stockpiles
        serializer = StockpileSerializer(stockpiles, many=True)
        # Return response
        return Response(serializer.data)


class StockpileView(APIView):
    def get(self, request, *args, **kwargs):
        # Get URL parameter
        stockpile_id = kwargs.get("stockpile_id")
        # Get stockpile data
        stockpile = Stockpile.objects.get(id=stockpile_id)
        # Serialize stockpile
        serializer = StockpileSerializer(stockpile)
        # Return response
        return Response(serializer.data)


@csrf_exempt
def create_stockpile(request):
    print(request)
    # Get the form submission
    if request.method == "POST":
        # Submission data
        submission = json.loads(request.body)
        # Create stockpile
        util.create_stockpile(submission)

    return render(request, "api/test.html", {
        "title": "title"
    })


class SymbolsView(APIView):
    def get(self, request, *args, **kwargs):
        # Get symbols
        symbols = Symbol.objects.all()
        # Serialize symbols
        serializer = SymbolSerializer(symbols, many=True)
        # Return response
        return Response(serializer.data)


class SymbolView(APIView):
    def get(self, request, *args, **kwargs):
        # Get URL parameter
        stock_symbol = kwargs.get("stock_symbol")
        # Get symbol
        symbol = Symbol.objects.get(symbol=stock_symbol)
        # Serialize symbol
        serializer = SymbolSerializer(symbol)
        # Return response
        return Response(serializer.data)


def update_symbols(request):
    # Update stock symbols
    util.update_symbols()


class StocksView(APIView):
    def get(self, request, *args, **kwargs):
        # Get Stocks
        stocks = Stock.objects.all()
        # Serialize stocks
        serializer = StockSerializer(stocks, many=True)
        # Return response
        return Response(serializer.data)


class StockView(APIView):
    def get(self, request, *args, **kwargs):
        # Get URL parameter
        stock_symbol = kwargs.get("stock_symbol")

        # Check if stock exists
        if Stock.objects.filter(symbol=stock_symbol.upper()).exists():
            # If the stock exists, update its data
            stock = Stock.objects.get(symbol=stock_symbol.upper())

        else:
            # Create a new stock
            stock = util.create_stock(stock_symbol)

        # Serialize stock
        serializer = StockSerializer(stock)
        # Return response
        return Response(serializer.data)


def update_stocks(request):
    # Update stocks data
    util.update_stocks()


@csrf_exempt
def active_user(request):
    # Get active user
    user = request.user
    # For a GET request
    if request.method == "GET":
        return JsonResponse(user.serialize(), safe=False)

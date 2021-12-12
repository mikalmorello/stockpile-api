import json
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import util

# Import models
from .models import User, Stockpile, Symbol, Stock

# Rest Framework
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import UserSerializer, StockpileSerializer, SymbolSerializer, StockSerializer

# Import token libraries
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Customize tokens


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        return token

# Token class


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


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
    """
    Handle users
    """
    # Set permissions
    permission_classes = (IsAuthenticated,)

    # Get Users
    def get(self, request, *args, **kwargs):
        # Get users data
        users = User.objects.all()
        # Serialize users
        serializer = UserSerializer(users, many=True)
        # Return response
        return Response(serializer.data)


class UserView(APIView):
    """
    Handle user
    """
    # Set permissions
    permission_classes = (IsAuthenticated,)

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
    """
    Handle stockpiles
    """
    # Set permissions
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        print("user is")
        print(request.user)
        # Get stockpiles data
        stockpiles = Stockpile.objects.all()
        # Serialize stockpiles
        serializer = StockpileSerializer(stockpiles, many=True)
        # Return response
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request, format=None):
        print("REQUEST")
        submission = json.loads(request.body)
        util.create_stockpile(submission)


class UserStockpilesView(APIView):
    """
    Handle users
    """
    # Set permissions
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        # get the user
        print("user is")
        print(request.user)
        user = request.user
        # Get list of users stockpiles
        stockpiles = user.created.all()
        # Get stockpiles data
        print(stockpiles)
        # Serialize stockpiles
        serializer = StockpileSerializer(stockpiles, many=True)
        # Return response
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request, format=None):
        print("REQUEST")
        submission = json.loads(request.body)
        util.create_stockpile(submission)


class CreateStockpileView(APIView):
    """
    Handle create stockpile
    """
    # Set permissions
    permission_classes = (IsAuthenticated,)

    @csrf_exempt
    def post(self, request, format=None):
        print("CREATE STOCKPILE")
        # User information
        print("create user is")
        print(request.user)
        # Get the user
        user = request.user

        # Get submission data
        submission = json.loads(request.body)

        # Create stockpile
        stockpile = util.create_stockpile(submission, user)

        # Create new stockpile
        newStockpile = Stockpile(
            title=stockpile['title'],
            creator=user,
        )

        # Save stockpile
        newStockpile.save()

        # Set stockpile stocks
        newStockpile.stocks.set(stockpile['stocks'])

        # return Response(newStockpile)
        return JsonResponse({"message": "Stockpile created."}, status=201)


class StockpileView(APIView):
    """
    Handle stockpile
    """
    # Set permissions
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        # Get URL parameter
        stockpile_id = kwargs.get("stockpile_id")
        # Get stockpile data
        stockpile = Stockpile.objects.get(id=stockpile_id)
        # Serialize stockpile
        serializer = StockpileSerializer(stockpile)
        # Return response
        return Response(serializer.data)

    def delete(self, request,  *args, **kwargs):
        # Get URL parameter
        stockpile_id = kwargs.get("stockpile_id")
        # Get stockpile data
        stockpile = Stockpile.objects.get(id=stockpile_id)
        # Delete object
        stockpile.delete()
        # return response
        return Response(status=status.HTTP_204_NO_CONTENT)


class SymbolsView(APIView):
    """
    Handle symbols
    """

    def get(self, request, *args, **kwargs):
        # Get symbols
        symbols = Symbol.objects.all()
        # Serialize symbols
        serializer = SymbolSerializer(symbols, many=True)
        # Return response
        return Response(serializer.data)


class SymbolView(APIView):
    """
    Handle symbol
    """

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
    """
    Update available stock symbols
    """
    # Update stock symbols
    util.update_symbols()


class StocksView(APIView):
    """
    Handle stocks
    """

    def get(self, request, *args, **kwargs):
        # Get Stocks
        stocks = Stock.objects.all()
        # Serialize stocks
        serializer = StockSerializer(stocks, many=True)
        # Return response
        return Response(serializer.data)


class StockView(APIView):
    """
    Handle stock
    """

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
    """
    Handle update stocks data
    """
    # Update stocks data
    util.update_stocks()

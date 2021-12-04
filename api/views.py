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


def users(request):
    # Get users
    users = User.objects.all()

    # For a GET request
    if request.method == "GET":
        return JsonResponse([user.serialize() for user in users], safe=False)


def user(request, user_id):
    # Get User
    user = User.objects.get(id=user_id)

    # For a GET request
    if request.method == "GET":
        return JsonResponse(user.serialize())


def stockpiles(request):
    # Get stockpiles
    stockpiles = Stockpile.objects.all()

    # For GET request
    if request.method == 'GET':
        return JsonResponse([stockpile.serialize() for stockpile in stockpiles], safe=False)


def stockpile(request, stockpile_id):
    # Refresh stockpile
    stockpile = Stockpile.objects.get(id=stockpile_id)

    # For a GET request
    if request.method == "GET":
        return JsonResponse(stockpile.serialize())


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


def symbols(request):
    # Get Symbols
    symbols = Symbol.objects.all()

    # For a GET request
    if request.method == "GET":
        return JsonResponse([symbol.serialize() for symbol in symbols], safe=False)


def symbol(request, stock_symbol):
    # Get Symbols
    symbol = Symbol.objects.get(symbol=stock_symbol.upper())

    # For a GET request
    if request.method == "GET":
        return JsonResponse(symbol.serialize(), safe=False)


def update_symbols(request):
    # Update stock symbols
    util.update_symbols()


def stocks(request):
    # Get Stocks
    stocks = Stock.objects.all()

    # For a GET request
    if request.method == "GET":
        return JsonResponse([stock.serialize() for stock in stocks], safe=False)


def stock(request, stock_symbol):

    # For a GET request
    if request.method == "GET":

        # Check if stock exists
        if Stock.objects.filter(symbol=stock_symbol.upper()).exists():
            # If the stock exists, update its data
            stock = Stock.objects.get(symbol=stock_symbol.upper())

            # Return json
            return JsonResponse(stock.serialize(), safe=False)
        else:
            # Create a new stock
            new_stock = util.create_stock(stock_symbol)

            # Return json
            return JsonResponse(new_stock.serialize(), safe=False)


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

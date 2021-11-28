import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import util

from .models import User, Stockpile, Symbol, Stock


def index(request):
    return render(request, "api/index.html", {
        "title": 'title',
    })


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
    stockpiles = util.refresh_stockpiles()

    # For GET request
    if request.method == 'GET':
        return JsonResponse([stockpile.serialize() for stockpile in stockpiles], safe=False)


def stockpile(request, stockpile_id):
    # Refresh stockpile
    stockpile = util.refresh_stockpile(stockpile_id)

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
        # Get the title
        title = submission.get("title")
        # Get the user
        creator = request.user
        # Get stocks

        print(submission)
        print(title)

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
            stock = util.refresh_stock(stock_symbol)

            # Return json
            return JsonResponse(stock.serialize(), safe=False)
        else:
            # Create a new stock
            new_stock = util.create_stock(stock_symbol)

            # Return json
            return JsonResponse(new_stock.serialize(), safe=False)

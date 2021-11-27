from django.shortcuts import render
from django.http import JsonResponse
from . import util

from .models import User, Stockpile, Symbol, Stock


def index(request):
    return render(request, "api/index.html", {
        "title": 'title',
    })


def stockpiles(request):
    # Get stockpiles
    stockpiles = Stockpile.objects.all()

    # For GET request
    if request.method == 'GET':
        return JsonResponse([stockpile.serialize() for stockpile in stockpiles], safe=False)


def stockpile(request, stockpile_id):
    # Get stockpile
    stockpile = Stockpile.objects.get(id=stockpile_id)
    stocks = stockpile.stocks.all()

    for stock in stocks:
        util.refresh_stock(stock.symbol)

    # For a GET request
    if request.method == "GET":
        return JsonResponse(stockpile.serialize())


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

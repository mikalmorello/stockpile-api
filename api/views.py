from django.shortcuts import render
from django.http import JsonResponse
from decouple import config
import requests
import datetime
import os
from django.conf import settings
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
    # print(stocks)
    symbols = []
    # # Add stock data to each symbol
    # for symbol in stocks:
    #     # Get Stock
    #     stock = util.get_stock(symbol)
    #     # print(stock)

    # print(stockpile)

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
    # Get Stocks
    symbols = Symbol.objects.all()

    # Get Nasdaq symbols files
    fileObject = open(os.path.join(settings.BASE_DIR, 'nasdaqlisted.txt'), "r")
    # Split file by line break
    listings = fileObject.readlines()
    # Remove the first header row
    listings = listings[1:]
    # Remove the date added at the end
    listings = listings[:-1]

    # Loop through symbols
    for listing in listings:
        # Remove any empty spaces
        listing = listing.strip()
        # Split symbol data on divider
        listing = listing.split("|")
        # Create new listing symbol
        listing_symbol = listing[0]
        listing_name = listing[1]

        # print(new_symbol)
        if symbols.filter(symbol=listing_symbol).exists():
            # If symbol already exists, don't do anything
            pass
        else:
            # Otherwise add symbol
            new_symbol = Symbol(symbol=listing_symbol, name=listing_name)
            new_symbol.save()
    return render(request, "api/test.html", {
        "title": "symbols",
    })


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

            # Get Stock
            stock = Stock.objects.get(symbol=stock_symbol.upper())
            date_of_today = datetime.date.today()
            stock_date = stock.last_refreshed.date()

            print(datetime.datetime.now())
            # If the stock hasn't been refreshed today
            if not date_of_today == stock_date:
                # Refresh stock data
                stockdata = util.get_stockdata(stock_symbol)

                # Update the stock
                stock.daily = stockdata
                stock.refreshed = datetime.datetime.now()
                stock.save()

            # Return json
            return JsonResponse(stock.serialize(), safe=False)
        else:
            print('stock is new')
            # Get Stockdata
            stockdata = util.get_stockdata(stock_symbol)

            # Create new stock
            new_stock = Stock(symbol=stock_symbol.upper(),
                              daily=stockdata, change_day=0, change_week=0)
            new_stock.save()

            # Return json
            return JsonResponse(new_stock.serialize(), safe=False)

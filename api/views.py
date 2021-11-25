from django.shortcuts import render
from django.http import JsonResponse
from decouple import config
import requests
import os
from django.conf import settings

from .models import User, Stockpile, Symbol


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


def stock(request, symbol_key):
    # Get Stock
    # AlphaVantage API Key
    API_KEY = config('ALPHAVANTAGE_API_KEY')
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol_key}&apikey={API_KEY}'
    r = requests.get(url)
    # stock = r.json()
    data = r.json()

    stock = {

        "symbol": data["Meta Data"]["2. Symbol"],
        "last_refreshed": data["Meta Data"]["3. Last Refreshed"],
        "daily":
        [
            {
                "date": list(data["Time Series (Daily)"].keys())[0],
                "price": list(data["Time Series (Daily)"].values())[0]["5. adjusted close"]
            },
            {
                "date": list(data["Time Series (Daily)"].keys())[1],
                "price": list(data["Time Series (Daily)"].values())[1]["5. adjusted close"]
            },
            {
                "date": list(data["Time Series (Daily)"].keys())[2],
                "price": list(data["Time Series (Daily)"].values())[2]["5. adjusted close"]
            },
            {
                "date": list(data["Time Series (Daily)"].keys())[3],
                "price": list(data["Time Series (Daily)"].values())[3]["5. adjusted close"]
            },
            {
                "date": list(data["Time Series (Daily)"].keys())[4],
                "price": list(data["Time Series (Daily)"].values())[4]["5. adjusted close"]
            },
        ]

    }

    print(list(data["Time Series (Daily)"].keys())[0])

    # For a GET request
    if request.method == "GET":
        return JsonResponse(stock, safe=False)

    return render(request, "api/test.html", {
        "title": "stock name",
        "symbol_key": symbol_key,
        "api": API_KEY
    })


def symbols(request):
    # Get Symbols
    symbols = Symbol.objects.all()

    # For a GET request
    if request.method == "GET":
        return JsonResponse([symbol.serialize() for symbol in symbols], safe=False)


def update_symbols(request):

    # Get Nasdaq symbols files
    fileObject = open(os.path.join(settings.BASE_DIR, 'nasdaqlisted.txt'), "r")
    # Split file by line break
    symbols = fileObject.readlines()
    # Remove the first header row
    symbols = symbols[1:]
    # Remove the date added at the end
    symbols = symbols[:-1]

    # Loop through symbols
    for symbol in symbols:
        # Remove any empty spaces
        symbol = symbol.strip()
        # Split symbol data on divider
        symbol = symbol.split("|")
        # Create new symbol
        new_symbol = {
            "symbol": symbol[0],
            "name": symbol[1]
        }
        print(new_symbol)
    return render(request, "api/test.html", {
        "title": "symbols",
    })

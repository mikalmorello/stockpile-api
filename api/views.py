from django.shortcuts import render
from django.http import JsonResponse
import requests

from .models import User, Stockpile


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


def stock(request, stock_key):
    # Get Stock
    # ADD APIKEY
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&apikey='
    # params = {'year': year, 'author': author}
    # r = requests.get(url, params=params)
    r = requests.get(url)
    stock = r.json()

    # For a GET request
    if request.method == "GET":
        return JsonResponse(stock)

    return render(request, "api/test.html", {
        "title": "stock name",
        "stock_key": stock_key
    })

from django.shortcuts import render
from django.http import JsonResponse

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

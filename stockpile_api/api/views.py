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

    return render(request, "api/stockpiles.html", {
        "title": "stockpiles",
        "stockpiles": stockpiles
    })


def stockpile(request, stockpile_id):
    # Get stockpile
    stockpile = Stockpile.objects.get(id=stockpile_id)

    # For a GET request
    if request.method == "GET":
        return JsonResponse(stockpile.serialize())

    # Render stockpile view
    return render(request, "api/stockpile.html", {
        "stockpile": stockpile,
        "id": stockpile_id
    })

from rest_framework import serializers

from .models import User, Stockpile, Symbol, Stock


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email'
        )


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = (
            'id', 'symbol', 'last_refreshed', 'daily', 'day_change', 'week_change'
        )


class StockpileSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    stocks = StockSerializer(read_only=True,  many=True)

    class Meta:
        model = Stockpile
        fields = (
            'id', 'title', 'stocks', 'date_created', 'creator'
        )


class SymbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symbol
        fields = (
            'id', 'symbol', 'name'
        )

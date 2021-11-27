# Dependencies
import requests
import datetime
import os
from decouple import config
from django.conf import settings


# Impprt model data
from .models import User, Stockpile, Symbol, Stock


# Get stock data
def get_stockdata(stock_symbol):
    API_KEY = config('ALPHAVANTAGE_API_KEY')
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={stock_symbol}&apikey={API_KEY}'
    r = requests.get(url)
    data = r.json()

    stockdata = [
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

    # Return the stock data
    return stockdata


# Update a stock
def refresh_stock(stock_symbol):
    print(f"--- {stock_symbol} Checked ---")
    # Get Stock
    stock = Stock.objects.get(symbol=stock_symbol.upper())
    # Get todays date
    todays_date = datetime.date.today()
    # Get the stocks last update date
    stock_date = stock.last_refreshed.date()

    # If the stock hasn't been refreshed today
    # if not stock_date == todays_date:
    if stock_date == todays_date:
        print(f"--- {stock_symbol} Refreshed ---")
        # Refresh stock data
        stockdata = get_stockdata(stock.symbol)

        # Get the daily change
        latest_price = float(stockdata[0]['price'])
        previous_price = float(stockdata[1]['price'])
        print(latest_price)
        print(previous_price)
        percent_change = str(
            round((((latest_price - previous_price) / previous_price) * 100), 2))
        print(percent_change)

        # Get the stock weekly change

        # Update the stock data
        stock.daily = stockdata
        # Update the last refreshed data
        stock.refreshed = datetime.datetime.now()
        # Save the stock
        stock.save()

    # Return the stock
    return stock


# Refresh stockpile
def refresh_stockpile(stockpile_id):
    # Get stockpile
    stockpile = Stockpile.objects.get(id=stockpile_id)
    print(stockpile)

    # Refresh associated stocks
    for stock in stockpile.stocks.all():
        refresh_stock(stock.symbol)

    # Return stockpile
    return stockpile


# Refresh stockpiles
def refresh_stockpiles():
    # Get stockpiles
    stockpiles = Stockpile.objects.all()

    # Refresh each stockpile
    for stockpile in stockpiles:
        refresh_stockpile(stockpile.id)

    # Return stockpiles
    return stockpiles


# Create a stock
def create_stock(stock_symbol):
    print(f"--- {stock_symbol} Created ---")
    # Get the stock data
    stockdata = get_stockdata(stock_symbol)

    # Create new stock
    stock = Stock(symbol=stock_symbol.upper(),
                  daily=stockdata, change_day=0, change_week=0)
    stock.save()

    # Return the stock
    return stock


def update_symbols():
    # Get Symbols
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

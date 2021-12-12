# Dependencies
import requests
import datetime
import time
import os
from decouple import config
from django.conf import settings


# Impprt model data
from .models import User, Stockpile, Symbol, Stock


def get_stockdata(stock_symbol):
    """
    Handle stock data from AlphaVantage
    """
    # Get environment variable
    API_KEY = config('ALPHAVANTAGE_API_KEY')
    # AlphaVantage API endpoint
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={stock_symbol}&apikey={API_KEY}'
    # Get "daily"data from AlphaVantage for the related stock
    r = requests.get(url)
    data = r.json()

    # Get the last 5 days of stock information
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
        {
            "date": list(data["Time Series (Daily)"].keys())[5],
            "price": list(data["Time Series (Daily)"].values())[5]["5. adjusted close"]
        },
    ]

    # Return the stock data
    return stockdata


def refresh_stock(stock_symbol):
    """
    Refresh stock data from AlphaVantage
    """
    # Get Stock
    stock = Stock.objects.get(symbol=stock_symbol.upper())
    # Get todays date
    todays_date = datetime.date.today()
    # Get the stocks last update date
    stock_date = stock.last_refreshed.date()

    # If the stock hasn't been refreshed today
    if not stock_date == todays_date:
        # Refresh stock data
        stockdata = get_stockdata(stock.symbol)

        # Price variables
        latest_price = stockdata[0]['price']
        previous_price = stockdata[1]['price']
        lastweek_price = stockdata[5]['price']

        # Get day change
        day_change = calculate_change(latest_price, previous_price)

        # Get week change
        week_change = calculate_change(latest_price, lastweek_price)

        # Update the stock data
        stock.daily = stockdata
        # Update the stock day change metrics
        stock.day_change = day_change
        # Update the stock week change metrics
        stock.week_change = week_change
        # Save the stock
        stock.save()

    # Return the stock
    return stock


# Create a stockpile
def create_stockpile(submission, user):
    """
    Create a stockpile
    """
    # Get the stockpile title
    title = submission.get("title")
    # Get selected symbols
    symbols = submission["stocks"]
    # Set max limit for number of selected symbols
    symbolsLimit = 5

    # Create a list of stocks
    stocks = []

    # Check the symbols length against the max limit
    if len(symbols) > symbolsLimit:
        # Slice off symbols that exceed the limit
        symbols = symbols[:symbolsLimit]
        # Print out error message
        print(
            f'You have exceeded the max number of stocks allowed in a stockpile ({symbolsLimit})')

    # Loop through selected symbols
    for symbol in symbols:
        # Set the stock symbol
        stock_symbol = symbol["value"]

        # Check if stock exists in database
        if Stock.objects.filter(symbol=stock_symbol.upper()).exists():
            # If the stock exists, refresh it's data
            stock = refresh_stock(stock_symbol)
            stocks.append(stock)
        else:
            # Create a new stock
            new_stock = create_stock(stock_symbol)
            # Append stock data
            stocks.append(new_stock)

    # Create new stockpile
    stockpile = {
        'title': title,
        'creator': user,
        'stocks': stocks
    }

    # Return the stockpile data
    return stockpile

# Refresh a stockpile


def refresh_stockpile(stockpile_id):
    # Get stockpile
    stockpile = Stockpile.objects.get(id=stockpile_id)

    # Number of stocks
    number_of_stocks = len(stockpile.stocks.all())

    # Price variables
    day_percent_change = 0
    week_percent_change = 0

    if(number_of_stocks > 0):

        # Loop through stocks
        for stock in stockpile.stocks.all():
            # Add stocks day % change to total
            day_percent_change = day_percent_change + \
                float(stock.day_change['percent'])
            # Add stocks week % change to total
            week_percent_change = week_percent_change + \
                float(stock.week_change['percent'])

        # Calculate stockpiles day % change
        day_percent_change = round(
            day_percent_change / number_of_stocks, 2)
        # Calculate stockpiles week % change
        week_percent_change = round(
            week_percent_change / number_of_stocks, 2)

    # Update the stockpile day change metrics
    stockpile.day_change = day_percent_change
    # Update the stockpile week change metrics
    stockpile.week_change = week_percent_change
    # Save the stockpile
    stockpile.save()


def create_stock(stock_symbol):
    """
    Create a stock
    """
    # Get the stock data
    stockdata = get_stockdata(stock_symbol)

    # Price variables
    latest_price = stockdata[0]['price']
    previous_price = stockdata[1]['price']
    lastweek_price = stockdata[5]['price']

    # Get day change
    day_change = calculate_change(latest_price, previous_price)

    # Get week change
    week_change = calculate_change(latest_price, lastweek_price)

    # Create new stock
    stock = Stock(symbol=stock_symbol.upper(),
                  daily=stockdata, day_change=day_change, week_change=week_change)

    # save the stock
    stock.save()

    # Return the stock
    return stock


def update_symbols():
    """
    Update symbols list from local nasdaqlisted.txt file
    """
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

        # Check if symbol exists
        if symbols.filter(symbol=listing_symbol).exists():
            # If symbol already exists, don't do anything
            pass
        else:
            # Otherwise create symbol
            new_symbol = Symbol(symbol=listing_symbol, name=listing_name)
            # Save symbol to the database
            new_symbol.save()


def calculate_change(latest_price, previous_price):
    """
    Calculate amount and percent change
    """
    # Convert any strings to numbers
    latest_price = float(latest_price)
    previous_price = float(previous_price)

    # Calculate price change
    price_change = round(latest_price - previous_price, 2)

    # Calculate percent change
    percent_change = str(
        round(((price_change / previous_price) * 100), 2))

    # Create change object
    change = {
        "price": price_change,
        "percent": percent_change,
    }

    # Return changes
    return change


def update_stocks():
    """
    Refresh stock symbols within AlphaVantage rate limites
    """
    # Get stocks
    stocks = Stock.objects.all()
    # For each stock
    for stock in stocks:
        # If using free AlphaVantage API use delay to handle rate limiting (5 calls per min)
        time.sleep(12)
        # List stock symbol
        print(stock.symbol)
        # Update stock data
        refresh_stock(stock.symbol)

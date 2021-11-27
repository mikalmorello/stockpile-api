# Dependencies
import requests
from decouple import config

# Get stock data


def get_stockdata(symbol_key):
    API_KEY = config('ALPHAVANTAGE_API_KEY')
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol_key}&apikey={API_KEY}'
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

    return stockdata

import requests
import os
from dotenv import load_dotenv, find_dotenv
import sys
sys.path.append('../helpers')
from utils import checkTickerSymbolValidity

load_dotenv(find_dotenv())

ALPHA_VANTAGE_API_KEY = os.environ.get('ALPHA_VANTAGE_API_KEY')


def getCurrentStockPrice(ticker):
    if not checkTickerSymbolValidity(ticker.lower()):
        return "Invalid ticker symbol!"
    API_URL = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={}&interval=1min&outputsize=full&apikey={}".format(ticker, ALPHA_VANTAGE_API_KEY)
    print("Retrieving current stock price")
    response = requests.get(API_URL).json()
    lastUpdated = response['Meta Data']['3. Last Refreshed']
    latestPrice = response['Time Series (1min)'][lastUpdated]['4. close']
    return latestPrice


print(getCurrentStockPrice("IBM"))

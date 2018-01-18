import requests
import os
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
# from ..helpers.utils import checkTickerSymbolValidity

load_dotenv(find_dotenv())

ALPHA_VANTAGE_API_KEY = os.environ.get('ALPHA_VANTAGE_API_KEY')


def getCurrentStockPrice(ticker, roundPrice=True):
    API_URL = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={}&interval=1min&outputsize=compact&apikey={}'.format(ticker, ALPHA_VANTAGE_API_KEY)
    response = requests.get(API_URL).json()
    lastUpdated = response['Meta Data']['3. Last Refreshed']
    latestPrice = float(response['Time Series (1min)'][lastUpdated]['4. close'])
    if not roundPrice:
        return latestPrice
    return round(latestPrice, 2)


def getKeyStatistics(ticker, roundStats=True):
    API_URL = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&interval=1min&outputsize=compact&apikey={}'.format(ticker, ALPHA_VANTAGE_API_KEY)
    response = requests.get(API_URL).json()

    keyStats = dict()

    lastUpdated = response['Meta Data']['3. Last Refreshed']

    if roundStats:
        keyStats['latestPrice'] = round(float(response['Time Series (Daily)'][lastUpdated[:10]]['4. close']), 2)
    else:
        keyStats['latestPrice'] = float(response['Time Series (Daily)'][lastUpdated[:10]]['4. close'])

    try:
        keyStats['lastRefreshed'] = datetime.strptime(lastUpdated, "%Y-%m-%d %H:%M:%S").strftime("%-I:%-M%p, %B %-d, %Y")
    except ValueError:
        # Market is closed
        keyStats['lastRefreshed'] = datetime.strptime(lastUpdated, "%Y-%m-%d").strftime("4:00PM, %B %-d, %Y (U.S. Markets are Closed)")

    keyStats['latestVolume'] = response['Time Series (Daily)'][lastUpdated[:10]]['5. volume']

    return keyStats


if __name__ == '__main__':
    print(getCurrentStockPrice('IBM'))

import requests
from datetime import datetime


def getCurrentStockPrice(ticker, roundPrice=True):
    API_URL = f'https://api.iextrading.com/1.0/stock/{ticker}/quote'
    response = requests.get(API_URL)
    if response.status_code == requests.codes.ok:
        responseData = response.json()
    latestPrice = float(responseData['latestPrice'])
    return round(latestPrice, 2) if roundPrice else latestPrice


def getKeyStatistics(ticker, roundStats=True):
    API_URL = 'https://api.iextrading.com/1.0/stock/{}/quote'.format(ticker)
    response = requests.get(API_URL).json()

    keyStats = dict()

    # update time of latestPrice in milliseconds since midnight Jan 1, 1970
    lastUpdated = datetime.fromtimestamp(int(str(response['latestUpdate'])[:10]))

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

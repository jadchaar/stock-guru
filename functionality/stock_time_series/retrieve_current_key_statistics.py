import requests
from datetime import datetime


def getCurrentStockPrice(ticker):
    API_URL = f'https://api.iextrading.com/1.0/stock/{ticker}/quote'
    response = requests.get(API_URL)
    if response.status_code == requests.codes.ok:
        responseData = response.json()
    else:
        response.raise_for_status()
    return responseData['latestPrice']


def getKeyStatistics(ticker, roundStats=True):
    API_URL = f'https://api.iextrading.com/1.0/stock/{ticker}/quote'
    response = requests.get(API_URL)
    if response.status_code == requests.codes.ok:
        responseData = response.json()
    else:
        response.raise_for_status()

    keyStats = dict()

    # update time of latestPrice in milliseconds since midnight Jan 1, 1970
    # keyStats['lastUpdated'] = datetime.fromtimestamp(int(str(responseData['latestUpdate'])[:10]))
    keyStats['lastUpdated'] = datetime.fromtimestamp(int(str(responseData['latestUpdate'])[:10])).strftime("%-I:%M%p, %B %-d, %Y")
    keyStats['sector'] = responseData['sector']
    keyStats['latestPrice'] = responseData['latestPrice']
    keyStats['latestVolume'] = responseData['latestVolume']
    keyStats['marketCap'] = responseData['marketCap']
    keyStats['peRatio'] = responseData['peRatio']

    return keyStats


if __name__ == '__main__':
    print(getCurrentStockPrice('IBM'))

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
    # Sanity check for max stock ticker length
    if len(ticker) > 5:
        return

    API_URL = f'https://api.iextrading.com/1.0/stock/{ticker}/quote'
    response = requests.get(API_URL)
    if response.status_code == requests.codes.ok:
        quoteData = response.json()
    else:
        response.raise_for_status()

    API_URL = f'https://api.iextrading.com/1.0/stock/{ticker}/stats'
    response = requests.get(API_URL)
    if response.status_code == requests.codes.ok:
        statsData = response.json()
    else:
        response.raise_for_status()

    # Combine stats and quote data
    responseData = {**statsData, **quoteData}

    keyStats = {}

    # update time of latestPrice in milliseconds since midnight Jan 1, 1970
    # keyStats['lastUpdated'] = datetime.fromtimestamp(int(str(responseData['latestUpdate'])[:10]))
    keyStats['symbol'] = responseData['symbol']
    keyStats['companyName'] = responseData['companyName']
    # keyStats['sector'] = responseData['sector']
    keyStats['lastUpdated'] = str(datetime.fromtimestamp(int(str(responseData['latestUpdate'])[:10])).strftime("%B %-d %-I:%M%p"))
    keyStats['latestPrice'] = responseData['latestPrice']

    # Other important stock meta data
    keyStats['previousClose'] = responseData['previousClose']
    keyStats['open'] = responseData['open']
    keyStats['dayRange'] = f'{responseData["low"]} - {responseData["high"]}'
    keyStats['week52Range'] = f'{responseData["week52Low"]} - {responseData["week52High"]}'
    keyStats['marketCap'] = responseData['marketCap']
    keyStats['latestVolume'] = responseData['latestVolume']
    keyStats['avgTotalVolume'] = responseData['avgTotalVolume']
    keyStats['peRatio'] = responseData['peRatio']
    keyStats['eps'] = responseData['latestEPS']
    keyStats['beta'] = round(responseData['beta'], 2)
    if responseData['dividendRate']:
        keyStats['dividend'] = f'{"{0:.2f}".format(responseData["dividendRate"])} ({"{0:.2f}%".format(responseData["dividendYield"])})'
        keyStats['exDividendDate'] = str(responseData['exDividendDate'])[:10]
    # Need to look into this stat more
    # keyStats['ytdReturn'] = responseData['ytdChange']

    return keyStats


if __name__ == '__main__':
    print(getCurrentStockPrice('IBM'))

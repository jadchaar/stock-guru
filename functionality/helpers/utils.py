import requests
from operator import itemgetter

'''
    Returns True if the symbol is VALID
    Returns False if the symbol is INVALID
'''


def checkTickerSymbolValidity(input):
    API_URL = 'https://api.iextrading.com/1.0/ref-data/symbols'
    response = requests.get(API_URL)
    if response.status_code == requests.codes.ok:
        responseData = response.json()
        # Check if symbol is available in API
        return input in map(itemgetter('symbol'), responseData)
    # Raise error if API cannot be reached
    response.raise_for_status()


def checkTickerNameValidity():
    pass

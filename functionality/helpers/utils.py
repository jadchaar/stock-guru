import json
from os.path import join, dirname

'''
    Returns True if the symbol is VALID
    Returns False if the symbol is INVALID
'''


def checkTickerSymbolValidity(input):
    symbolsPath = join(dirname(__file__), 'symbols.json')
    # with open('symbols.json', 'r') as f:
    with open(symbolsPath, 'r') as f:
        symbols = json.load(f)
        if symbols.get(input) is None:
            return False
        return True


def checkTickerNameValidity():
    pass

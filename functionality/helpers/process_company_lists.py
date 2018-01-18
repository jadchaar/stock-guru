# Data source: http://www.nasdaq.com/screening/company-list.aspx

import csv
import json


def clean_input(i):
    return i.lower()


def clean_stock_ticker(i):
    return i.lower().replace("^", "-")


def read_csv():
    symbol_to_name = dict()
    name_to_symbol = dict()

    # NASDAQ
    with open('NASDAQ_Company_List.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            symbol_to_name[clean_stock_ticker(row['Symbol'])] = row['Name']
            name_to_symbol[row['Name']] = clean_stock_ticker(row['Symbol'])

    # NYSE
    with open('NYSE_Company_List.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            symbol_to_name[clean_stock_ticker(row['Symbol'])] = row['Name']
            name_to_symbol[row['Name']] = clean_stock_ticker(row['Symbol'])

    # AMEX
    with open('AMEX_Company_List.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            symbol_to_name[clean_stock_ticker(row['Symbol'])] = row['Name']
            name_to_symbol[row['Name']] = clean_stock_ticker(row['Symbol'])

    return symbol_to_name, name_to_symbol


def save_json(s, n):
    with open('symbols.json', 'w') as f:
        json.dump(s, f, sort_keys=True)

    with open('names.json', 'w') as f:
        json.dump(n, f, sort_keys=True)


if __name__ == '__main__':
    S_TO_N, N_TO_S = read_csv()
    save_json(S_TO_N, N_TO_S)

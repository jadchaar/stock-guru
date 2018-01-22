from functionality.stock_time_series import retrieve_current_key_statistics
from functionality.helpers import utils
import click


@click.command()
@click.option('--ticker', default='IBM', help='Get current stock price for the specified ticker symbol')
@click.argument('action')
def getCurrentPriceForTicker(ticker, action):
    """ Gets the current stock price for the specified ticker SYMBOL """
    if not utils.checkTickerSymbolValidity(ticker.upper()):
        return click.echo('Invalid ticker symbol!')

    if action == 'gcp':
        # Get Current Price
        currentPrice = retrieve_current_key_statistics.getCurrentStockPrice(ticker)
        click.echo(f'Latest {ticker.upper()} stock price: {currentPrice}')
    elif action == 'gks':
        # Get Key Stats
        keyStats = retrieve_current_key_statistics.getKeyStatistics(ticker)
        click.echo(f'{keyStats["companyName"]} ({keyStats["symbol"]}) as of {keyStats["lastUpdated"]}')
        click.echo(f'* Latest Price: {keyStats["latestPrice"]}')
        click.echo(f'* Previous Close: {keyStats["previousClose"]}')
        click.echo(f'* Open: {keyStats["open"]}')
        click.echo(f'* Day\'s Range: {keyStats["dayRange"]}')
        click.echo(f'* 52 Week Range: {keyStats["week52Range"]}')
        click.echo(f'* Market Cap: {keyStats["marketCap"]}')
        click.echo(f'* Volume: {keyStats["latestVolume"]}')
        click.echo(f'* Avg Volume: {keyStats["avgTotalVolume"]}')
        click.echo(f'* P/E Ratio: {keyStats["peRatio"]}')
        click.echo(f'* EPS: {keyStats["eps"]}')
        click.echo(f'* Beta: {keyStats["beta"]}')
        if 'dividend' in keyStats:
            click.echo(f'* Dividend: {keyStats["dividend"]}')
            click.echo(f'* Ex-Dividend Date: {keyStats["exDividendDate"]}')
    else:
        click.echo('Invalid action. Please try again.')


if __name__ == '__main__':
    click.echo('~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~')
    click.echo('~ ~ ~ ~ ~ ~ ~ Welcome to the Stock Guru!  ~ ~ ~ ~ ~ ~')
    click.echo('~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~\n')
    # print(retrieve_current_prices.getCurrentStockPrice('IBM'))
    getCurrentPriceForTicker()

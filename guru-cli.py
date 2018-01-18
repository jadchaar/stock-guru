from functionality.stock_time_series import retrieve_current_key_statistics
from functionality.helpers import utils
import click


@click.command()
@click.option('--ticker', default='IBM', help='Get current stock price for the specified ticker symbol')
@click.argument('action')
def getCurrentPriceForTicker(ticker, action):
    """ Gets the current stock price for the specified ticker SYMBOL """
    if not utils.checkTickerSymbolValidity(ticker.lower()):
        click.echo('Invalid ticker symbol!')

    if action == 'gcp':
        # Get Current Price
        click.echo('Retrieving data...')
        currentPrice = retrieve_current_key_statistics.getCurrentStockPrice(ticker)
        click.echo(f'Latest {ticker.upper()} stock price: {currentPrice}')
    elif action == 'gks':
        # Get Key Stats
        click.echo('Retrieving data...')
        keyStats = retrieve_current_key_statistics.getKeyStatistics(ticker)
        click.echo(f'Key Statistics for {ticker.upper()}')
        click.echo(f'Last Updated: {keyStats["lastRefreshed"]}')
        click.echo(f'Latest Price: {keyStats["latestPrice"]}')
        click.echo(f'Volume: {keyStats["latestVolume"]}')
    else:
        click.echo('Invalid action. Please try again.')


if __name__ == '__main__':
    click.echo('~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~')
    click.echo('~ ~ ~ ~ ~ ~ ~ Welcome to the Stock Guru!  ~ ~ ~ ~ ~ ~')
    click.echo('~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~\n')
    # print(retrieve_current_prices.getCurrentStockPrice('IBM'))
    getCurrentPriceForTicker()

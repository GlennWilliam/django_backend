from django.core.management.base import BaseCommand
from stocks.views import fetch_stock_data

class Command(BaseCommand):
    help = 'Fetch stock data from Alpha Vantage'

    def handle(self, *args, **kwargs):
        symbol = input("Enter the stock symbol: ")
        fetch_stock_data(symbol)
        self.stdout.write(self.style.SUCCESS(f'Successfully fetched data for {symbol}'))
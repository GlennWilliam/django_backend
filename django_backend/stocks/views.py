from django.shortcuts import render

import requests
from django.conf import settings
from .models import StockData
from django.http import JsonResponse
from .models import StockData, PredictedStockPrice
from .ml_model import load_model, predict_future_prices
import pandas as pd
from datetime import timedelta
import pickle

API_KEY = '' # Your API key here

def fetch_stock_data(symbol='AAPL'):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={API_KEY}'
    
    response = requests.get(url)
    data = response.json()
    
    # Extract time series data
    time_series = data.get("Time Series (Daily)", {})
    
    for date, prices in time_series.items():
        StockData.objects.update_or_create(
            symbol=symbol,
            date=date,
            defaults={
                'open_price': prices["1. open"],
                'high_price': prices["2. high"],
                'low_price': prices["3. low"],
                'close_price': prices["4. close"],
                'volume': prices["5. volume"],
            }
        )

from django.shortcuts import render
from .models import StockData
from .backtest import backtest  # Import the backtesting logic
import pandas as pd

def backtest_view(request):
    if request.method == 'POST':
        # Get user inputs from form
        stock_symbol = request.POST['symbol']
        initial_investment = float(request.POST['investment'])
        short_window = int(request.POST['short_window'])
        long_window = int(request.POST['long_window'])

        # Fetch stock data for the symbol
        stock_data = StockData.objects.filter(symbol=stock_symbol).order_by('date')
        prices = pd.DataFrame(list(stock_data.values('date', 'close_price')))

        # Perform backtesting
        results = backtest(prices, initial_investment, short_window, long_window)

        # Pass the results to the template
        return render(request, 'backtest_results.html', {'results': results})

    return render(request, 'backtest_form.html')



from django.http import JsonResponse
from .models import StockData
from .ml_model import load_model, predict_future_prices
import pandas as pd
from datetime import timedelta

def predict_stock_prices(request, stock_symbol):
    # Order the queryset by date and apply the slice after converting it to a queryset
    stock_data = StockData.objects.filter(symbol=stock_symbol).order_by('date').values('date', 'close_price')[:200]

    # Convert to DataFrame directly from the queryset (which is now in dictionary form)
    prices_df = pd.DataFrame(list(stock_data))

    # Load the pre-trained model
    model = load_model()

    # Predict the stock prices for the next 30 days
    predictions = predict_future_prices(prices_df, model, days=30)
    
    # Prepare the response data
    response_data = []
    last_date = prices_df['date'].max()  # Get the last date

    for i, prediction in enumerate(predictions):
        predicted_date = last_date + timedelta(days=i+1)
        response_data.append({
            'predicted_date': predicted_date,
            'predicted_price': float(prediction),
        })
    
    # Return the predictions as a JSON response
    return JsonResponse({'predictions': response_data})


from django.http import JsonResponse, FileResponse, HttpResponseBadRequest
from .models import StockData
from .ml_model import load_model, predict_future_prices
from .utils import generate_stock_plot, generate_pdf_report  # Import the correct generate_pdf_report function
import pandas as pd

def generate_report(request, stock_symbol):
    # Fetch the most recent 200 days of stock data
    stock_data = StockData.objects.filter(symbol=stock_symbol).order_by('-date').values('date', 'close_price')[:200]
    stock_data = list(reversed(stock_data))
    
    # Check if stock data is empty
    if not stock_data:
        return HttpResponseBadRequest("No stock data available for the given symbol.")
    
    # Convert to DataFrame
    prices_df = pd.DataFrame(stock_data)

    # Load the pre-trained model
    model = load_model()

    # Predict the stock prices for the next 30 days
    predictions = predict_future_prices(prices_df, model, days=30)

    # Generate the plot image (base64-encoded)
    try:
        img_base64 = generate_stock_plot(prices_df['date'], prices_df['close_price'], predictions)
    except ValueError as e:
        return HttpResponseBadRequest(f"Error generating plot: {e}")
    
    # Metrics (you should calculate these based on your logic)
    metrics = {
        'total_return': 10.5,  # Example
        'max_drawdown': -5.2,  # Example
        'trades_executed': 15  # Example
    }
    
    # If request format is PDF, generate a PDF report
    if request.GET.get('format') == 'pdf':
        # Pass only metrics and img_base64 to the function
        pdf_buffer = generate_pdf_report(metrics, img_base64)  
        return FileResponse(pdf_buffer, as_attachment=True, filename='stock_report.pdf')

    # Else, return a JSON response with the metrics and base64-encoded plot image
    return JsonResponse({
        'metrics': metrics,
        'plot_image': img_base64
    })


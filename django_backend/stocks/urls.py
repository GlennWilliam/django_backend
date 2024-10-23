from django.urls import path
from .views import backtest_view
from .views import predict_stock_prices
from .views import generate_report


urlpatterns = [
    path('backtest/', backtest_view, name='backtest'),  # The backtesting page
    path('predict/<str:stock_symbol>/', predict_stock_prices, name='predict_stock_prices'),
    path('report/<str:stock_symbol>/', generate_report, name='generate_report')
]
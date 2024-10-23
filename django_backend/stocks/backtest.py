import pandas as pd

def moving_average(prices, window):
    return prices.rolling(window=window).mean()

def backtest(prices, initial_investment, short_window=50, long_window=200):
    """
    Backtest a simple moving average strategy.

    :param prices: DataFrame with 'date' and 'close' price.
    :param initial_investment: Initial investment amount.
    :param short_window: Period for short moving average (e.g., 50 days).
    :param long_window: Period for long moving average (e.g., 200 days).
    :return: Summary of performance including total return, max drawdown, and trades executed.
    """
    
    # Calculate short and long moving averages
    prices['short_ma'] = moving_average(prices['close_price'], short_window)
    prices['long_ma'] = moving_average(prices['close_price'], long_window)

    # Initialize variables for backtesting
    cash = initial_investment
    stock_holding = 0
    portfolio_value = []
    trades = 0

    for i in range(len(prices)):
        close_price = float(prices['close_price'][i])  # Convert Decimal to float
        if prices['short_ma'][i] < prices['long_ma'][i] and cash > 0:  # Buy signal
            stock_holding = cash / close_price
            cash = 0  # Use all cash to buy stock
            trades += 1
        elif prices['short_ma'][i] > prices['long_ma'][i] and stock_holding > 0:  # Sell signal
            cash = stock_holding * close_price
            stock_holding = 0
            trades += 1

        # Calculate portfolio value
        portfolio_value.append(cash + (stock_holding * close_price))

    # Calculate performance metrics
    total_return = ((portfolio_value[-1] - initial_investment) / initial_investment) * 100
    max_drawdown = min(portfolio_value) / initial_investment * 100 - 100

    return {
        'total_return': total_return,
        'max_drawdown': max_drawdown,
        'trades_executed': trades,
        'final_portfolio_value': portfolio_value[-1]
    }
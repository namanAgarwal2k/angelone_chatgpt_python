# strategies/backtest.py

import pandas as pd
from utils.session_manager import SmartConnectSingleton
from datetime import datetime, timedelta

def fetch_historical_data(symbol,symbolToken, exchange="NSE", interval="ONE_MINUTE", days=10):
    """Fetch historical data from Angel One for a given symbol."""
    obj = SmartConnectSingleton.get_instance()

    # Define date range
    to_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d %H:%M')

    params = {
        "exchange": exchange,
        "tradingsymbol": symbol,
        "symboltoken": symbolToken,  # Replace with correct symbol token
        "interval": interval,
        "fromdate": from_date,
        "todate": to_date
    }
    
    # Fetch data
    market_data = obj.getCandleData(params)
    df = pd.DataFrame(market_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df


def calculate_momentum(df, window=10):
    """Calculate momentum based on price difference over a window."""
    df['momentum'] = df['close'].diff(window)
    return df['momentum'].iloc[-1]  # Return latest momentum value


def select_symbols_by_momentum(symbol_list, threshold=5):
    """Select symbols whose momentum is above a given threshold."""
    selected_symbols = []
    for symbol in symbol_list:
        df = fetch_historical_data(symbol)
        momentum = calculate_momentum(df)
        if momentum > threshold:
            selected_symbols.append(symbol)
    return selected_symbols


def run_backtest(strategy, symbol_list, **kwargs):
    """Run backtest on selected symbols based on the momentum filter."""
    selected_symbols = select_symbols_by_momentum(symbol_list)
    
    for symbol in selected_symbols:
        print(f"Running backtest on {symbol} with {strategy.__name__}")
        strategy(symbol, **kwargs)


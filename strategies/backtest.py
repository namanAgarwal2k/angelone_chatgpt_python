# strategies/backtest.py

import pandas as pd
from utils.session_manager import SmartConnectSingleton
from datetime import datetime, timedelta

# yei hame data de dega sara date wise
def fetch_historical_data(session, symbol_token, interval, from_date, to_date):
    try:
        params = {
            "exchange": "NSE",
            "symboltoken": symbol_token,
            "interval": interval,
            "fromdate": from_date,
            "todate": to_date
        }
        response = session.getCandleData(params)
        if response['status']:
            data = response['data']
            df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        else:
            print("Error fetching data:", response['message'])
            return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

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


# # strategies/strategy1.py
# def simple_moving_average_strategy(data):
#     short_window = 5
#     long_window = 20
    
#     # Assuming 'data' is a Pandas DataFrame with a 'close' price column
#     data['short_mavg'] = data['close'].rolling(window=short_window).mean()
#     data['long_mavg'] = data['close'].rolling(window=long_window).mean()

#     # Buy when short MA crosses above long MA; sell when it crosses below
#     if data['short_mavg'].iloc[-1] > data['long_mavg'].iloc[-1]:
#         return "BUY"
#     elif data['short_mavg'].iloc[-1] < data['long_mavg'].iloc[-1]:
#         return "SELL"
#     return "HOLD"


# strategies/strategy1.py

from utils.session_manager import SmartConnectSingleton
from strategies.backtest import fetch_historical_data, calculate_momentum

def strategy1(symbol, days=10):
    """Example momentum-based trading strategy."""
    obj = SmartConnectSingleton.get_instance()
    
    # Fetch historical data
    df = fetch_historical_data(symbol, days=days)
    
    # Calculate buy/sell signals based on momentum
    df['momentum'] = df['close'].diff(5)
    buy_signals = df[df['momentum'] > 0]
    
    # Example output (log buy signals)
    if not buy_signals.empty:
        print(f"Buy signal for {symbol} at {buy_signals['timestamp'].iloc[-1]}")

    # Store or log trade data for analysis

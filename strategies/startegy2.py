import time
from datetime import datetime,timedelta
from ta.volatility import AverageTrueRange
import pandas as pd
from strategies.backtest import fetch_historical_data
from utils.session_manager import SmartConnectSingleton


symbol = "TATAMOTORS-EQ" 
symbolToken= "3456"
exchange="NSE"
obj = SmartConnectSingleton.get_instance()


# def calculate_supertrend(df, period=7, multiplier=3):
#     if len(df) < period:
#         print("Not enough data to calculate ATR")
#         return df  # or handle it as needed   
#     atr = AverageTrueRange(df['high'], df['low'], df['close'], window=period).average_true_range()
#     hl2 = (df['high'] + df['low']) / 2
#     df['supertrend_green'] = hl2 - (multiplier * atr)  # Lower line for buy signal
#     df['supertrend_red'] = hl2 + (multiplier * atr)    # Upper line for sell signal
#     return df

import pandas as pd
from ta.volatility import AverageTrueRange

def calculate_supertrend(df, period=7, multiplier=3):
    # Check if there's enough data to calculate ATR
    if len(df) < period:
        print("Not enough data to calculate ATR")
        return df

    # Calculate ATR
    atr = AverageTrueRange(df['high'], df['low'], df['close'], window=period).average_true_range()
    hl2 = (df['high'] + df['low']) / 2

    # Initialize columns
    df.loc[:, 'supertrend_green'] = hl2 - (multiplier * atr)
    df.loc[:, 'supertrend_red'] = hl2 + (multiplier * atr)
    df.loc[:, 'supertrend'] = df['supertrend_green']  # Initialize with 'supertrend_green' values
    df.loc[:, 'supertrend_direction'] = True  # Assume an initial uptrend

    # Loop through data to calculate supertrend values
    for i in range(1, len(df)):
        if df.loc[i - 1, 'supertrend_direction']:  # Uptrend
            # Ensure previous supertrend value is not None
            prev_supertrend = df.loc[i - 1, 'supertrend'] if pd.notna(df.loc[i - 1, 'supertrend']) else df.loc[i, 'supertrend_green']
            df.loc[i, 'supertrend'] = max(df.loc[i, 'supertrend_green'], prev_supertrend)
            if df.loc[i, 'close'] < df.loc[i, 'supertrend']:
                df.loc[i, 'supertrend_direction'] = False
        else:  # Downtrend
            prev_supertrend = df.loc[i - 1, 'supertrend'] if pd.notna(df.loc[i - 1, 'supertrend']) else df.loc[i, 'supertrend_red']
            df.loc[i, 'supertrend'] = min(df.loc[i, 'supertrend_red'], prev_supertrend)
            if df.loc[i, 'close'] > df.loc[i, 'supertrend']:
                df.loc[i, 'supertrend_direction'] = True

    print(df)
    return df
   

# no need of this alreadu in backtest file
def fetch_data(symbol, interval="ONE_MINUTE", duration=10):
    try:
        historicDataParams= {
            "exchange": "NSE",
            "symboltoken": "3456",
            "interval": "THREE_MINUTE",
           "fromdate": (datetime.now()-timedelta(days=duration)).strftime('%Y-%m-%d %H:%M'),
            "todate": datetime.now().strftime('%Y-%m-%d %H:%M')

            # "exchange":exchange,
            # "symbolToken":symbolToken,
            # "interval":interval,"fromdate": (datetime.now()-timedelta(days=duration)).strftime('%Y-%m-%d %H:%M'),
            # "todate": datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        response=obj.getCandleData(historicDataParams)
        print(response)
        return response
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def check_supertrend_conditions(df):
    current_bar = df.iloc[-1]
    previous_bar = df.iloc[-2]
    
    # Buy Signal: Price just closed below green line
    buy_price = current_bar['supertrend_green'] * 1.01
    if (previous_bar['close'] > previous_bar['supertrend_green'] and
        current_bar['close'] < current_bar['supertrend_green']):
        return "BUY", buy_price
    
    # Sell Signal: Price just closed above red line
    sell_price = current_bar['supertrend_red'] * 0.99
    if (previous_bar['close'] < previous_bar['supertrend_red'] and
        current_bar['close'] > current_bar['supertrend_red']):
        return "SELL", sell_price
    
    return None, None

def send_whatsapp_message(message):
    # Placeholder function for WhatsApp notification
    print("Sending WhatsApp message:", message)

def is_market_open():
    now = datetime.now()
    market_start = now.replace(hour=9, minute=15, second=0, microsecond=0)
    market_end = now.replace(hour=15, minute=20, second=0, microsecond=0)
    return market_start <= now <= market_end

def run_strategy2():
    if not obj:
        print(obj)
        return

    consecutive_losses = 0
    last_trade_time = None
    pending_order = False  # Track if there's a pending order


    if not is_market_open():
        print("Market closed.")
        # return

    df = fetch_data(symbol=symbol)
    if df is None or len(df) < 2:
        time.sleep(60)

    historical_data = fetch_historical_data(session=obj,symbol_token=symbolToken,interval="ONE_MINUTE",from_date = "2024-09-01 09:15",
to_date = "2024-09-30 15:30" )
    print(historical_data)

    # Apply the Supertrend calculation
    historical_data = calculate_supertrend(historical_data)

    signal, price = check_supertrend_conditions(historical_data)

    if signal and not pending_order:
        # Check for loss limits
        if consecutive_losses >= 3:
            send_whatsapp_message("3 consecutive losses. Stopping trades for the day.")
            return

        stop_loss = price * 0.95 if signal == "BUY" else price * 1.05
        target = price * 1.05 if signal == "BUY" else price * 0.95
        trade_response = place_order(obj, symbol, price, stop_loss, target, signal)

        if trade_response["status"]:
            print("Order executed:", trade_response)
            last_trade_time = datetime.now()
            pending_order = True  # Set pending order flag
        else:
            consecutive_losses += 1
            print("Trade failed. Loss count:", consecutive_losses)
            send_whatsapp_message(f"Trade executed at {price} but failed. Loss count: {consecutive_losses}")

    # If an order is no longer active (e.g., filled or cancelled), reset the pending_order flag
    if check_order_status(obj) == "completed":
        pending_order = False

    time.sleep(10)  # Run every 10 seconds for real-time checks

def place_order(obj, symbol, price, stop_loss, target, signal):
    try:
        order_params = {
            "variety": "NORMAL",
            "tradingsymbol": symbol,
            "transaction_type": "BUY" if signal == "BUY" else "SELL",
            "quantity": 1,
            "order_type": "LIMIT",
            "price": price,
            "stoploss": stop_loss,
            "target": target
        }
        response = obj.placeOrder(order_params)
        return response
    except Exception as e:
        print(f"Order placement error: {e}")
        return {"status": False}

def check_order_status(obj):
    # Check order status
    order_status = obj.orderBook()
    if order_status.get("status") == "COMPLETE":
        return "completed"
    return "pending"

# if __name__ == "__main__":
#     run_strategy2()

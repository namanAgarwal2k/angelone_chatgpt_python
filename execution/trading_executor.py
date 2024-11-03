# execution/trading_executor.py

from utils.logger import log_trade
from datetime import datetime
from utils.session_manager import SmartConnectSingleton

def place_order(symbol,symboltoken, quantity, price, order_type="BUY", exchange="NSE"):
    """Place an order with Angel One SmartConnect API."""
    obj = SmartConnectSingleton.get_instance()

    order_params = {
        "variety": "NORMAL",             # Normal order variety
        "tradingsymbol": symbol,         # Trading symbol for the stock
        "symboltoken": symboltoken,           # Replace with the correct symbol token
        "transactiontype": order_type,   # BUY or SELL
        "exchange": exchange,            # NSE/BSE/MCX
        "ordertype": "LIMIT",            # Order type (LIMIT/MARKET)
        "producttype": "INTRADAY",       # Intraday or delivery
        "duration": "DAY",               # Valid for the day
        "price": price,                  # Price for limit order
        "squareoff": 0,                  # Square off value
        "stoploss": 0,                   # Stoploss value
        "quantity": quantity             # Quantity to trade
    }

    try:
        order_id = obj.placeOrder(order_params)
        print(f"Order placed successfully. Order ID: {order_id}")
        return order_id
    except Exception as e:
        print(f"Failed to place order: {str(e)}")
        return None


def execute_trade(symbol,symboltoken, quantity, price, live=False):
    """Execute trade in live or paper mode."""
    if live:
        # Place live order using place_order function
        order_id = place_order(symbol,symboltoken, quantity, price)
    # else:
    #     # Simulate paper trading
    #     order_id = "paper_" + str(datetime.now().timestamp())
    #     log_trade(order_id, symbol, quantity, price, 'paper')

    # if order_id:
    #     print(f"Trade executed for {symbol} (ID: {order_id})")
    else:
        print(f"Trade failed for {symbol}")

    return order_id

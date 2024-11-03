# execution/paper_execution.py

from datetime import datetime


def execute_paper_order(symbol,symboltoken, quantity, price, live=False):
    # Simulate the execution of an order for paper trading
    order_id = "paper_" + str(datetime.now().timestamp())
    print(f"Paper Trade executed for {symbol} (ID: {order_id})")

# write code to execute paper trade with strategy2 in which you will buy bank nifty option strike price whether ATM call or put option of current week expiry where time frame is 5 and 15 minutes 

# first we will make supertrend stategy in which in 1 min frame on banknifty price chart we will execute a buy order when bar goes below green line (buy price-> 1% of green line price, stoploss-5% of buy price, target 5% above buy price) (precautions-> if execute do not enter for next 3 mins or do more research , do not trade if bar is not coming from upwards if its green line and opposite for red line NOTE-> if trade take more than 3 loss stop for the day send whatsapp message)

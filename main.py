# main.py

from execution.paper_execution import execute_paper_order
from strategies.backtest import run_backtest
from strategies.startegy1 import strategy1
from strategies.startegy2 import run_strategy2
from execution.trading_executor import execute_trade
from utils.session_manager import SmartConnectSingleton

def main():
    # Initialize session
    session = SmartConnectSingleton.get_instance()

    # Choose between backtesting or live trading
    mode = input("Enter mode (backtest/live/paper): ").strip().lower()

    if mode == 'backtest':
        print("Running Backtest...")
        # List of symbols to backtest
        symbol_list = ['RELIANCE', 'TCS', 'INFY']  # Add your list of symbols here
        # run_backtest(run_strategy2, symbol_list)
        run_strategy2()

    elif mode == 'live':
        print("Running Live Trading...")
        # Example live trade
        symbol = "TATAMOTORS-EQ"
        symboltoken= "3456"
        quantity = 10
        price = 2500
        execute_trade(symbol,symboltoken, quantity, price, live=True)
    
    elif mode == 'paper':
        print("Running Paper Trading...")
        # Example paper trade
        symbol = "TATAMOTORS-EQ"
        symboltoken= "3456"
        quantity = 10
        price = 2500
        execute_paper_order(symbol,symboltoken, quantity, price, live=False)
    
    else:
        print("Invalid mode selected. Please choose 'backtest', 'live', or 'paper'.")

if __name__ == "__main__":
    main()

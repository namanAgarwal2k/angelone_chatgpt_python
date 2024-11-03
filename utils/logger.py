
# utils/logger.py

import csv
from datetime import datetime

def log_trade(order_id, symbol, quantity, price, trade_type):
    """Log the trade details into a CSV file."""
    log_file = f"trades_{trade_type}.csv"  # Separate files for live, paper, backtesting
    
    with open(log_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), order_id, symbol, quantity, price])
    
    print(f"Trade logged for {symbol} - {trade_type}")

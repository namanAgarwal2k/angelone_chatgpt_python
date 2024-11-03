# data/paper_data.py

import random

def fetch_paper_data():
    # Generate mock market data for paper trading
    return {
        "symbol": "RELIANCE",
        "price": round(random.uniform(900, 1100), 2),
        "volume": random.randint(100, 1000)
    }

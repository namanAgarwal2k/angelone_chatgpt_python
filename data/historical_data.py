# data/historical_data.py
import pandas as pd

def fetch_historical_data(file_path):
    # Load historical data from a CSV or database
    data = pd.read_csv(file_path)
    return data

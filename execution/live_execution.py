# execution/live_execution.py
import requests
import json

def execute_live_order(signal):
    order = {
        "symbol": "RELIANCE",
        "order_type": signal,
        "quantity": 10,
        "price": "market"
    }
    
    url = "https://api.angelbroking.com/order"
    headers = {"Authorization": "Bearer YOUR_API_TOKEN"}
    
    response = requests.post(url, headers=headers, json=order)
    
    if response.status_code == 200:
        print(f"Live order executed: {signal}")
    else:
        print(f"Error executing live order: {response.status_code}")

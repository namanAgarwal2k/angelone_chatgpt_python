# data/live_data.py
import requests
import json

def fetch_live_data():
    url = "https://api.angelbroking.com/marketData"  # Example API endpoint
    headers = {"Authorization": "Bearer YOUR_API_TOKEN"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return json.loads(response.content)
    else:
        print("Error fetching live data")
        return None

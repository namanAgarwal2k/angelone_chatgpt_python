
# # # The json.load() function reads the JSON data as a dictionary or list, which can be converted to a DataFrame for easy filtering.
# # The filtering steps are the same as before, allowing you to extract the symbol and symbol token for Bank Nifty options based on your criteria.


# import json
# import pandas as pd

# # Load the JSON instrument file
# instrument_file_path = 'path_to_instrument_master.json'

# with open(instrument_file_path, 'r') as f:
#     data = json.load(f)

# # If the data is structured as a list of dictionaries, you can convert it to a DataFrame
# df = pd.DataFrame(data)

# # Check the structure of the DataFrame to confirm it's loaded correctly
# print(df.head())

# # Now, filter for Bank Nifty options
# df = df[df['symbol'].str.startswith('BANKNIFTY')]

# # Specify criteria for the option
# expiry_date = '2023-11-09'  # Example expiry date in YYYY-MM-DD format
# strike_price = 43000         # Example strike price
# option_type = 'CE'           # CE for Call, PE for Put

# # Filter based on expiry, strike, and option type
# option_df = df[(df['expiry'] == expiry_date) & 
#                (df['strike'] == strike_price) & 
#                (df['symbol'].str.endswith(option_type))]

# if not option_df.empty:
#     symbol = option_df.iloc[0]['symbol']
#     symbol_token = option_df.iloc[0]['symboltoken']
#     print(f"Symbol: {symbol}, Symbol Token: {symbol_token}")
# else:
#     print("No matching option found for the specified criteria.")




# BELOW CSV FILE CODE


import pandas as pd

# Load the instrument CSV file
instrument_file_path = 'openApiScripMaster.csv'
df = pd.read_csv(instrument_file_path)

# Filter for Bank Nifty options only
df = df[df['symbol'].str.startswith('BANKNIFTY')]

# Specify the expiry date, strike price, and option type (e.g., CE for call, PE for put)
expiry_date = '2023-11-09'  # Example expiry date in YYYY-MM-DD format
strike_price = 43000  # Example strike price
option_type = 'CE'  # CE for Call, PE for Put

# Find the matching row for the specified option
option_df = df[(df['expiry'] == expiry_date) & 
               (df['strike'] == strike_price) & 
               (df['symbol'].str.endswith(option_type))]

if not option_df.empty:
    symbol = option_df.iloc[0]['symbol']
    symbol_token = option_df.iloc[0]['symboltoken']
    print(f"Symbol: {symbol}, Symbol Token: {symbol_token}")
else:
    print("No matching option found for the specified criteria.")

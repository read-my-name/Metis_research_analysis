import requests
import pandas as pd
from datetime import datetime

# Etherscan API details
API_URL = 'https://api.etherscan.io/v2/api'
API_KEY = 'YOUR_API_KEY'  # Replace with your actual API key

# Define the parameters for the query
contract_address = '0x9E32b13ce7f2E80A01932B42553652E053D6ed8e'
dex_address = '0x1c98562A2FaB5aF19D8Fb3291a36AC3C618835D9'  
cex_address = '0x5bdf85216ec1e38D6458C870992A69e38e03F7Ef'
offset = 100  # Number of records per page

# Define the start and end dates
start_date = datetime(2024, 9, 1)
end_date = datetime(2024, 12, 31)

# Function to convert timestamp to datetime
def convert_timestamp_to_datetime(timestamp):
    return datetime.utcfromtimestamp(int(timestamp))

def get_block_number(api_key, date, closest):
    url = "https://api.etherscan.io/api"
    
    # If date is a datetime object, convert it to a timestamp directly
    if isinstance(date, datetime):
        timestamp = int(date.timestamp())
    else:
        timestamp = int(datetime.strptime(date, "%Y-%m-%d %H:%M:%S").timestamp())
    
    params = {
        "module": "block",
        "action": "getblocknobytime",
        "timestamp": timestamp,
        "closest": closest,  # 'before' or 'after'
        "apikey": api_key
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        try:
            response_json = response.json()
            if response_json.get("status") == "1" and "result" in response_json:
                # The result is now a string directly representing the block number
                block_number = int(response_json["result"])  # Directly convert the string to an integer
                return block_number
            else:
                print(f"Error from API: {response_json.get('message', 'Unknown error')}")
        except (KeyError, TypeError, ValueError) as e:
            print(f"Error: Unexpected response structure. {e}")
    else:
        print(f"HTTP Error: {response.status_code}")
    return None

# Function to get transactions from Etherscan API
def get_transactions():
    transactions = []
    page = 1
    
    start_block = get_block_number(API_KEY, start_date, "after")
    end_block = get_block_number(API_KEY, end_date, "before")

    print(f"Starting Block (after {start_date}): {start_block}")
    print(f"Ending Block (before {end_date}): {end_block}")

    while True:
        params = {
            'chainid': 1,
            'module': 'account',
            'action': 'tokentx',
            'contractaddress': contract_address,
            'address': cex_address,
            'startblock': start_block,
            'endblock': end_block,
            'page': page,
            'offset': offset,
            'sort': 'asc',
            'apikey': API_KEY
        }

        response = requests.get(API_URL, params=params)
        data = response.json()

        if data['status'] == '1':  # Success
            transactions += data['result']
            if len(data['result']) < offset:
                break
            page += 1  # Go to the next page
        else:
            print(f"Error: {data['message']}")
            break

    return transactions

# Function to filter transactions based on date range
def filter_transactions_by_date(transactions):
    filtered_transactions = []
    for tx in transactions:
        timestamp = int(tx['timeStamp'])
        tx_datetime = convert_timestamp_to_datetime(timestamp)
        
        # Check if the transaction is within the date range
        if start_date <= tx_datetime <= end_date:
            filtered_transactions.append(tx)
    
    return filtered_transactions

# Retrieve and filter the transactions
transactions = get_transactions()
filtered_transactions = filter_transactions_by_date(transactions)

# Convert the filtered transactions to a pandas DataFrame
data = []
for tx in filtered_transactions:
    data.append({
        'transaction_hash': tx['hash'],
        'block_number': tx['blockNumber'],
        'from_address': tx['from'],
        'to_address': tx['to'],
        'value': tx['value'],
        'token_name': tx['tokenName'],
        'token_symbol': tx['tokenSymbol'],
        'timestamp': convert_timestamp_to_datetime(tx['timeStamp']),
        'gas': tx['gas'],
        'gas_price': tx['gasPrice'],
        'nonce': tx['nonce'],
        'input_data': tx['input'],
    })

df = pd.DataFrame(data)

# Define the output file path
output_file = 'data/market_behaviour/cex_metis_transactions.csv'

# Save the DataFrame to a CSV file
df.to_csv(output_file, index=False)

print(f"Transaction data has been saved to {output_file}")

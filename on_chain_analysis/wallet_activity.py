import pandas as pd
import requests
import time
import os

# File paths
input_file_path = "data/wallet_activity/Metis_top_holder.csv"
output_file_path = "data/wallet_activity/Metis_top_holder_tx.csv"

# Read the top holders list
top_holders_df = pd.read_csv(input_file_path)

# Extract wallet addresses from the CSV file
wallet_addresses = top_holders_df['address'].tolist()

# API details
base_url_from = "https://api.routescan.io/v2/network/mainnet/evm/all/transactions"
base_url_to = "https://api.routescan.io/v2/network/mainnet/evm/all/transactions"
timestamp_from = "2024-12-01T00:00:29"
timestamp_to = "2024-12-31T00:00:29"
chain_id = "1088"

# Function to fetch transactions for a wallet
def fetch_transactions(wallet_address, is_from=True):
    url = base_url_from if is_from else base_url_to
    params = {
        "includedChainIds": chain_id,
        "timestampFrom": timestamp_from,
        "timestampTo": timestamp_to,
        "fromAddresses" if is_from else "toAddresses": wallet_address,
        "sort": "desc",
        "limit": 50
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("items", [])
    else:
        print(f"Error fetching data for {wallet_address}: {response.status_code}")
        return []

# Store all transactions
all_transactions = []

# Fetch transactions for each wallet address
for wallet in wallet_addresses:
    print(f"Fetching transactions for wallet: {wallet}")
    
    # Fetch transactions where wallet is the sender
    from_transactions = fetch_transactions(wallet, is_from=True)
    
    # Fetch transactions where wallet is the recipient
    to_transactions = fetch_transactions(wallet, is_from=False)
    
    # Combine both sender and recipient transactions
    combined_transactions = from_transactions + to_transactions
    
    if combined_transactions:
        for tx in combined_transactions:
            # Extract relevant fields from each transaction
            all_transactions.append({
                'Wallet': wallet,
                'TransactionHash': tx.get('id', 'NA'),
                'Timestamp': tx.get('timestamp', 'NA'),
                'From': tx.get('from', 'NA'),
                'To': tx.get('to', 'NA'),
                'Value': tx.get('value', 'NA'),
                'ChainId': tx.get('chainId', 'NA')
            })
    else:
        # If no transactions are retrieved, create a placeholder row with NA
        all_transactions.append({
            'Wallet': wallet, 
            'TransactionHash': 'NA', 
            'Timestamp': 'NA', 
            'From': 'NA', 
            'To': 'NA', 
            'Value': 'NA', 
            'ChainId': 'NA'
        })

    # Pause to avoid hitting the rate limit
    time.sleep(1)

# Save transactions to a CSV file
if all_transactions:
    transactions_df = pd.DataFrame(all_transactions)
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)  # Ensure directory exists
    transactions_df.to_csv(output_file_path, index=False)
    print(f"Transactions saved to {output_file_path}")
else:
    print("No transactions retrieved.")

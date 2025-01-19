import json
import requests
import csv
from datetime import datetime

# Load the wallet addresses from the JSON file
def load_wallets_from_json(json_file_path):
    try:
        with open(json_file_path, "r") as file:
            wallets = json.load(file)
            print("Wallets loaded successfully!")
            return wallets
    except FileNotFoundError:
        print(f"Error: File not found at {json_file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON. {e}")
        return None

# Function to retrieve the block number for a given date
def get_block_number(api_key, date, closest):
    url = "https://api.etherscan.io/api"
    params = {
        "module": "block",
        "action": "getblocknobytime",
        "timestamp": int(datetime.strptime(date, "%Y-%m-%d %H:%M:%S").timestamp()),
        "closest": closest,  # 'before' or 'after'
        "apikey": api_key
    }
    response = requests.get(url, params=params)

    # Log the response for debugging purposes
    print(f"API Response for {date}: {response.text}")

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

# Function to retrieve records related to wallet addresses between the block range
def retrieve_wallet_records(api_key, start_block, end_block, wallet_addresses):
    url = "https://api.etherscan.io/api"
    records = []

    for wallet_address in wallet_addresses:
        params = {
            "module": "account",
            "action": "txlist",
            "address": wallet_address,
            "startblock": start_block,
            "endblock": end_block,
            "page": 1,
            "offset": 100,
            "sort": "asc",
            "apikey": api_key
        }

        response = requests.get(url, params=params)

        # Log the response for debugging purposes
        print(f"API Response for wallet {wallet_address}: {response.text}")
        
        if response.status_code == 200:
            try:
                response_json = response.json()
                if response_json.get("status") == "1" and "result" in response_json:
                    transactions = response_json["result"]
                    if transactions:
                        for tx in transactions:
                            # Extract the required fields and add wallet address as 'id'
                            record = {
                                "id": wallet_address,  # Move wallet address to 'id' as the first column
                                "timestamp": tx["timeStamp"],
                                "from": tx["from"],
                                "to": tx["to"],
                                "contractAddress": tx["contractAddress"],
                                "value": tx["value"],
                                "tokenSymbol": tx.get("tokenSymbol", ""),  # Safely handle missing keys
                                "tokenName": tx.get("tokenName", ""),  # Safely handle missing keys
                            }
                            records.append(record)
                    else:
                        print(f"No transactions found for wallet {wallet_address}")
                else:
                    print(f"Error from API for wallet {wallet_address}: {response_json.get('message', 'Unknown error')}")
            except (KeyError, TypeError, ValueError) as e:
                print(f"Error parsing transaction response for wallet {wallet_address}: {e}")
        else:
            print(f"HTTP Error for wallet {wallet_address}: {response.status_code}")
    
    return records

# Function to save the records to a CSV file
def save_to_csv(records, csv_file_path):
    if records:
        keys = records[0].keys()  # Get the headers from the first record
        with open(csv_file_path, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(records)
        print(f"Records saved to {csv_file_path}")
    else:
        print("No records to save.")

# Main function to execute the process
def main():
    # Load configuration
    api_key = "YOUR_API_KEY"
    json_file_path = "/content/drive/MyDrive/Metis/data/top_holders_metis.json"
    csv_file_path = "/content/drive/MyDrive/Metis/data/filtered_wallet_records.csv"

    # Load wallet addresses from the JSON file
    wallets = load_wallets_from_json(json_file_path)
    if wallets is None:
        return

    # Extract wallet addresses from the JSON data
    wallet_addresses = [wallet['address'] for wallet in wallets.get("named_wallets", [])]
    wallet_addresses += [wallet['address'] for wallet in wallets.get("unnamed_wallets", [])]

    # Get starting and ending block numbers for the date range
    start_date = "2024-11-01 00:00:00"
    end_date = "2024-12-31 23:59:59"
    
    start_block = get_block_number(api_key, start_date, "after")
    end_block = get_block_number(api_key, end_date, "before")

    if start_block and end_block:
        print(f"Starting Block (after {start_date}): {start_block}")
        print(f"Ending Block (before {end_date}): {end_block}")
        
        # Retrieve wallet records between the start and end blocks
        records = retrieve_wallet_records(api_key, start_block, end_block, wallet_addresses)
        
        # Save the records to a CSV file
        save_to_csv(records, csv_file_path)
    else:
        print("Failed to retrieve block numbers.")

if __name__ == "__main__":
    main()

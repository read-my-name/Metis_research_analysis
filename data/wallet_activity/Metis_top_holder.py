import requests
import csv
import os

# Create a folder named 'data' if it doesn't exist
os.makedirs("data", exist_ok=True)

# File path for storing CSV data
output_file = "data/wallet_activity/Metis_top_holder.csv"

# Initialize the URL
url = "https://api.routescan.io/v2/network/mainnet/evm/all/addresses?includedChainIds=1088&sort=balanceValueUsd,desc&limit=50"

# Define the headers for the API request (if required)
headers = {
    "Content-Type": "application/json",
}

# Open the CSV file for writing
with open(output_file, mode="w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write the header row to the CSV file
    csv_writer.writerow(["chainId", "address", "balance", "balanceValueUsd"])

    try:
        # Make a GET request to the API
        response = requests.get(url, headers=headers)

        # Check for HTTP errors
        response.raise_for_status()

        # Parse the JSON response
        data = response.json()

        # Process each item in the response
        for item in data.get("items", []):
            csv_writer.writerow([
                item.get("chainId"),
                item.get("address"),
                item.get("balance"),
                item.get("balanceValueUsd"),
            ])

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data: {e}")

print(f"Top holders have been successfully stored in {output_file}")

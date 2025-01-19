import requests
import csv
import os

# Create a folder named 'data' if it doesn't exist
os.makedirs("data", exist_ok=True)

# File path for storing CSV data
output_file = "data/smart_contracts/smart_contracts.csv"

# Initialize the base URL
base_url = "https://api.routescan.io/v2/network/mainnet/evm/all/contracts?verified=true&includedChainIds=1088&limit=50"

# Define the headers for the API request (if required)
headers = {
    "Content-Type": "application/json",
}

# Open the CSV file for writing
with open(output_file, mode="w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write the header row to the CSV file
    csv_writer.writerow([
        "chainId", "address", "createTimestamp", "txHash", "creator", "name", "verified", 
        "verifiedAt", "txCount", "compilerName", "compilerVersion", "optimizerEnabled", "optimizerRuns"
    ])

    print("Fetching smart contracts...")
    url = base_url

    while url:
        try:
            # Make a GET request to the API
            response = requests.get(url, headers=headers)

            # Check for HTTP errors
            response.raise_for_status()

            # Parse the JSON response
            data = response.json()

            # Process each contract in the response
            for contract in data.get("items", []):
                create_op = contract.get("createOperation", {})
                compiler_settings = contract.get("compilerSettings", {}).get("optimizer", {})

                csv_writer.writerow([
                    contract.get("chainId"),
                    contract.get("address"),
                    create_op.get("timestamp"),
                    create_op.get("txHash"),
                    create_op.get("from"),
                    contract.get("name"),
                    contract.get("verified"),
                    contract.get("verifiedAt"),
                    contract.get("txCount"),
                    contract.get("compilerName"),
                    contract.get("compilerVersion"),
                    compiler_settings.get("enabled"),
                    compiler_settings.get("runs")
                ])

            # Get the next link from the "link" section
            next_link = data.get("link", {}).get("next")

            # Update the URL for the next request or stop if there's no next link
            if next_link:
                url = f"https://api.routescan.io{next_link}"
            else:
                url = None

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching data: {e}")
            break

print(f"Smart contracts have been successfully stored in {output_file}")

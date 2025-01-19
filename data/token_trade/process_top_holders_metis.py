import csv
import json

# Define the file path for the CSV and the output JSON
csv_file_path = "data/token_trade/top_holder_$METIS.csv"
json_output_path = "data/token_trade/top_holders_metis.json"

# Initialize a list to store the wallet data
wallet_data = []

# Read the CSV file and process the data
with open(csv_file_path, mode="r", encoding="utf-8") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    # Loop through each row in the CSV
    for row in csv_reader:
        # Extract relevant data from each row
        address = row['Address']
        name = row['Address_Nametag'] if row['Address_Nametag'] else None
        quantity = float(row['Quantity'].replace(',', ''))  # Ensure proper formatting of quantity
        
        # Add the data to the wallet_data list
        wallet_data.append({
            'address': address,
            'name': name,
            'quantity': quantity,
            'percentage': row['Percentage'],
            'value': row['Value']
        })

# Sort the wallets by quantity in descending order to find the top unnamed wallets
unnamed_wallets = [wallet for wallet in wallet_data if wallet['name'] is None]
unnamed_wallets.sort(key=lambda x: x['quantity'], reverse=True)

# Select the top 2 unnamed wallets
top_unnamed_wallets = unnamed_wallets[:2]

# Prepare the final data for the JSON file
top_wallets = {
    'named_wallets': [wallet for wallet in wallet_data if wallet['name']],
    'top_unnamed_wallets': top_unnamed_wallets
}

# Write the result to a JSON file
with open(json_output_path, 'w', encoding='utf-8') as json_file:
    json.dump(top_wallets, json_file, indent=4)

print(f"Top wallets data saved to {json_output_path}")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.dates import DateFormatter
import json

# Load CSV file into a pandas DataFrame
csv_file = 'data/market_behaviour/filtered_wallet_records.csv'
df = pd.read_csv(csv_file)

# Load the JSON file containing the wallet name mappings
json_file = 'data/token_trade/top_holders_$metis.json'

with open(json_file, 'r') as f:
    wallet_data = json.load(f)

# Create a dictionary mapping wallet addresses to names
wallet_name_mapping = {}

# Process named wallets
for wallet in wallet_data['named_wallets']:
    wallet_name_mapping[wallet['address'].lower()] = wallet['name']

# Process unnamed wallets (they don't have names, so map to 'Unknown')
for wallet in wallet_data['unnamed_wallets']:
    wallet_name_mapping[wallet['address'].lower()] = wallet['name'] or 'Whale'

# Ensure that the 'value' column is numeric
df['value'] = pd.to_numeric(df['value'], errors='coerce')

# Step 1: Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

# Step 2: Group by wallet address and filter addresses with more than 5 transactions
transaction_counts = df.groupby('from')['timestamp'].count()
wallets_more_than_5 = transaction_counts[transaction_counts > 5].index

# Filter the data for wallets with more than 5 transactions
df_filtered = df[df['from'].isin(wallets_more_than_5)].copy()  # Use .copy() to avoid the warning

# Add a new column for the wallet name using .loc to avoid SettingWithCopyWarning
df_filtered.loc[:, 'wallet_name'] = df_filtered['from'].apply(lambda x: wallet_name_mapping.get(x.lower(), 'Whale'))

# Step 3: Determine the number of subplots needed
num_wallets = len(df_filtered['wallet_name'].unique())
cols = 3  # Number of columns in the subplot grid
rows = (num_wallets // cols) + (1 if num_wallets % cols != 0 else 0)  # Calculate rows needed

# Dynamically adjust figure size based on the number of rows and columns
fig_width = 5 * cols  # Width per subplot multiplied by the number of columns
fig_height = 5 * rows  # Height per subplot multiplied by the number of rows

# Step 4: Create subplots with dynamic size
fig, axes = plt.subplots(rows, cols, figsize=(fig_width, fig_height))
axes = axes.flatten()  # Flatten to easily access each subplot

# Step 5: Loop through each unique wallet name and plot on the respective subplot
for idx, wallet in enumerate(df_filtered['wallet_name'].unique()):
    wallet_data = df_filtered[df_filtered['wallet_name'] == wallet]
    
    # Plot on the corresponding subplot
    ax = axes[idx]
    ax.plot(wallet_data['timestamp'], wallet_data['value'], label=f"Wallet {wallet}")
    
    # Customize the plot for the current wallet
    ax.set_title(f"{wallet} Wallet")
    ax.set_xlabel("DateTime")
    ax.set_ylabel("Value")
    ax.legend(title="Wallet Name")
    ax.tick_params(axis='x', rotation=45)

    # Shorten datetime format to yyyy-mm-dd
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))

# Hide empty subplots if there are fewer wallets than available subplots
for i in range(num_wallets, len(axes)):
    axes[i].axis('off')

# Step 6: Adjust layout and show the plots
plt.tight_layout()
plt.show()

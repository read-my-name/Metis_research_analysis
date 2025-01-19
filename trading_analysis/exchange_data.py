import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data for DEX and CEX
dex_file_path = 'data/market_behaviour/dex_$metis_transactions.csv'
cex_file_path = 'data/market_behaviour/cex_$metis_transactions.csv'

# Load data into DataFrames
dex_df = pd.read_csv(dex_file_path)
cex_df = pd.read_csv(cex_file_path)

# Function to preprocess the data and calculate daily trading volume
def preprocess_and_calculate_daily_volume(df):
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    # Convert value to numeric
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    # Aggregate trading volume by date
    df['date'] = df['timestamp'].dt.date
    daily_volume = df.groupby('date')['value'].sum().reset_index()
    daily_volume.columns = ['Date', 'Trading Volume']
    return daily_volume

# Process DEX and CEX data
dex_daily_volume = preprocess_and_calculate_daily_volume(dex_df)
cex_daily_volume = preprocess_and_calculate_daily_volume(cex_df)

# Plotting the data
fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

# Plot DEX trading volume
axes[0].plot(dex_daily_volume['Date'], dex_daily_volume['Trading Volume'], 
             marker='o', color='blue', label='Uniswap Trading Volume')
axes[0].grid(alpha=0.3)
axes[0].legend()

# Plot CEX trading volume
axes[1].plot(cex_daily_volume['Date'], cex_daily_volume['Trading Volume'], 
             marker='o', color='green', label='Bitget Trading Volume')
axes[1].grid(alpha=0.3)
axes[1].legend()

# Set a single title for the entire figure
fig.suptitle('Daily Trading Volume of METIS (Bitget vs Uniswap)', fontsize=16)

# Add shared y-label with adjusted position
fig.text(0.02, 0.5, 'Trading Volume (METIS)', va='center', ha='center', rotation='vertical', fontsize=12)

# Set x-label for the last subplot
axes[1].set_xlabel('Date', fontsize=12)

# Adjust layout and show the plot
plt.xticks(rotation=45)
plt.tight_layout()
plt.subplots_adjust(left=0.12, top=0.9)  # Adjust the left margin to allow space for y-label
plt.show()

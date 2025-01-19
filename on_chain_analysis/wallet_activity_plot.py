import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
file_path = 'data/wallet_activity/0xfad31cd4d45Ac7C4B5aC6A0044AA05Ca7C017e62.csv'  # Update this path to your file location
df = pd.read_csv(file_path)

# Convert 'DateTime (UTC)' to datetime format
df['DateTime (UTC)'] = pd.to_datetime(df['DateTime (UTC)'], errors='coerce')

# Ensure the columns 'Value_IN(ETH)' and 'Value_OUT(ETH)' are numeric
df['Value_IN(ETH)'] = pd.to_numeric(df['Value_IN(ETH)'], errors='coerce')
df['Value_OUT(ETH)'] = pd.to_numeric(df['Value_OUT(ETH)'], errors='coerce')

# Initialize a column for the cumulative value
df['Cumulative_Value'] = df['Value_IN(ETH)'] - df['Value_OUT(ETH)']  # IN minus OUT
df['Cumulative_Value'] = df['Cumulative_Value'].cumsum()  # Cumulative sum of the adjusted values

# Plotting the trend line for cumulative value
plt.figure(figsize=(10, 6))

# Plot cumulative value
plt.plot(df['DateTime (UTC)'], df['Cumulative_Value'], label='Cumulative Value (ETH)', color='blue', marker='o', linestyle='-', markersize=4)

# Adding labels and title
plt.xlabel('DateTime (UTC)', fontsize=12)
plt.ylabel('In/Out Value (ETH)', fontsize=12)
plt.title('**C0xfad31cd4d45Ac7C4B5aC6A0044AA05Ca7C017e62** Wallet Activity', fontsize=14)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Adding legend
plt.legend()

# Display the plot
plt.tight_layout()
plt.show()

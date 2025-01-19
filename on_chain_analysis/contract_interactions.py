import pandas as pd
import matplotlib.pyplot as plt

# Load data from the CSV files
df_enki = pd.read_csv('data/smart_contracts/ENKI.csv')
df_token_messaging = pd.read_csv('data/smart_contracts/TokenMessaging.csv')
df_erc1967proxy = pd.read_csv('data/smart_contracts/ERC1967Proxy.csv')
df_growfitterolympicsv2 = pd.read_csv('data/smart_contracts/GrowfitterOlympicsv2.csv')
df_optimizedtransparentupgradeableproxy = pd.read_csv('data/smart_contracts/OptimizedTransparentUpgradeableProxy.csv')

# Convert UnixTimestamp to datetime for all CSV files
df_enki['DateTime'] = pd.to_datetime(df_enki['UnixTimestamp'], unit='s')
df_token_messaging['DateTime'] = pd.to_datetime(df_token_messaging['UnixTimestamp'], unit='s')
df_erc1967proxy['DateTime'] = pd.to_datetime(df_erc1967proxy['UnixTimestamp'], unit='s')
df_growfitterolympicsv2['DateTime'] = pd.to_datetime(df_growfitterolympicsv2['UnixTimestamp'], unit='s')
df_optimizedtransparentupgradeableproxy['DateTime'] = pd.to_datetime(df_optimizedtransparentupgradeableproxy['UnixTimestamp'], unit='s')

# Set the DateTime as the index for easier plotting
df_enki.set_index('DateTime', inplace=True)
df_token_messaging.set_index('DateTime', inplace=True)
df_erc1967proxy.set_index('DateTime', inplace=True)
df_growfitterolympicsv2.set_index('DateTime', inplace=True)
df_optimizedtransparentupgradeableproxy.set_index('DateTime', inplace=True)

# Calculate transaction counts per day for all contracts
df_enki_resampled = df_enki.resample('D').size()
df_token_messaging_resampled = df_token_messaging.resample('D').size()
df_erc1967proxy_resampled = df_erc1967proxy.resample('D').size()
df_growfitterolympicsv2_resampled = df_growfitterolympicsv2.resample('D').size()
df_optimizedtransparentupgradeableproxy_resampled = df_optimizedtransparentupgradeableproxy.resample('D').size()

# Plotting
plt.figure(figsize=(12, 8))

# Plot transaction count over time for each contract with distinct colors
line1, = plt.plot(df_enki_resampled.index, df_enki_resampled, label='ENKI', color='blue', linestyle='-', linewidth=2)
line2, = plt.plot(df_token_messaging_resampled.index, df_token_messaging_resampled, label='TokenMessaging', color='green', linestyle='-', linewidth=2)
line3, = plt.plot(df_erc1967proxy_resampled.index, df_erc1967proxy_resampled, label='ERC1967Proxy', color='red', linestyle='-', linewidth=2)
line4, = plt.plot(df_growfitterolympicsv2_resampled.index, df_growfitterolympicsv2_resampled, label='GrowfitterOlympicsv2', color='orange', linestyle='-', linewidth=2)
line5, = plt.plot(df_optimizedtransparentupgradeableproxy_resampled.index, df_optimizedtransparentupgradeableproxy_resampled, label='OptimizedTransparentUpgradeableProxy', color='purple', linestyle='-', linewidth=2)

# Add title and labels
plt.title('Top Active Smart Contracts Interactions', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Transaction Count', fontsize=12)

# Display the legend
plt.legend()

# Rotate x-axis labels for readability
plt.xticks(rotation=45)

# Add transaction count labels at the peak for each line with offset
def add_peak_label_with_offset(line, label, color):
    peak_index = line.get_xdata()[line.get_ydata().argmax()]
    peak_value = line.get_ydata().max()
    
    # Offset label position
    y_offset = 0.005 * peak_value  # 10% offset above the peak
    x_offset = pd.Timedelta(days=1)  # Shift the label to the right by 1 day

    # Avoid overlap by adjusting the position if needed
    plt.text(peak_index + x_offset, peak_value + y_offset, f'{label}: {int(peak_value)}', color=color, 
             fontsize=10, ha='center', va='bottom', bbox=dict(facecolor='white', alpha=0.7, edgecolor=color))

# Add labels for each line at the peak with offset
add_peak_label_with_offset(line1, 'ENKI', 'blue')
add_peak_label_with_offset(line2, 'TokenMessaging', 'green')
add_peak_label_with_offset(line3, 'ERC1967Proxy', 'red')
add_peak_label_with_offset(line4, 'GrowfitterOlympicsv2', 'orange')
add_peak_label_with_offset(line5, 'OptimizedTransparentUpgradeableProxy', 'purple')

# Display the plot
plt.tight_layout()
plt.show()

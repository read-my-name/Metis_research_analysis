import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load the CSV file
file_path = "data/token_trade/METIS_USD_data.csv"
df = pd.read_csv(file_path)

# Rename columns to standard names for processing
df.rename(columns={
    "Date": "date",
    "Price": "close",
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Vol.": "volume",
    "Change %": "change"
}, inplace=True)

# Convert 'date' column to datetime format and sort by date
df["date"] = pd.to_datetime(df["date"])
df.sort_values("date", inplace=True)

# Clean the volume and change columns
df["volume"] = df["volume"].str.replace("K", "").astype(float) * 1000
df["change"] = df["change"].str.replace("%", "").astype(float)

# Create subplots with 2 rows (1 for candlestick and 1 for volume)
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, 
                    subplot_titles=("Candlestick Chart", "Volume Chart"))

# Define colors for up and down candlesticks
up_color = 'green'
down_color = 'red'

# Add candlestick chart to the first subplot (row 1)
fig.add_trace(go.Candlestick(
    x=df["date"],
    open=df["open"],
    high=df["high"],
    low=df["low"],
    close=df["close"],
    name="Price",
    increasing_line_color=up_color,  # Green for up
    decreasing_line_color=down_color  # Red for down
), row=1, col=1)

# Add volume chart to the second subplot (row 2)
fig.add_trace(go.Bar(
    x=df["date"],
    y=df["volume"],
    name="Volume",
    marker=dict(color="blue"),
    showlegend=False  # Hide legend for volume
), row=2, col=1)

# Update layout to remove legend and arrange subplots
fig.update_layout(
    title="METIS/USD Chart",
    xaxis=dict(title="Date"),
    xaxis2=dict(title="Date"),
    yaxis=dict(title="Price In USD", side="left"),
    yaxis2=dict(title="Volume", side="left", range=[0, df["volume"].max() * 1.2]),
    template="presentation",
    height=800,  # Set height for better visualization
    showlegend=False,  # Remove the legend entirely
    hovermode='x unified'  # Show a unified hover line across both plots
)

# Show the chart
fig.show()

# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.3
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
print("BisimiAllah")

# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# Define the color map for each year

#  2017: "#000000",  # Black 2018: "#2439F2",  # Blue 2019: "#CB2C48",  # Red 2020: "#008000"   # Green

COLOR_MAP = {
    2019: "#CB2C48",  # Red
    2020: "#008000"   # Green
}



# Set font and style configurations
plt.rcParams['font.family'] = 'sans-serif'  # Use a sans-serif font
plt.rcParams['font.sans-serif'] = ['Helvetica']  # Specify Arial as the sans-serif font
plt.rcParams['font.size'] = 12  # Default font size
plt.rcParams['axes.titlesize'] = 14  # Title font size
plt.rcParams['axes.labelsize'] = 12  # Axis label font size
plt.rcParams['xtick.labelsize'] = 10  # X-tick label font size
plt.rcParams['ytick.labelsize'] = 10  # Y-tick label font size
plt.rcParams['legend.fontsize'] = 10  # Legend font size

# Set Seaborn style globally
sns.set_style("whitegrid")

# Load the data with explicit date format and set index
try:
    df = pd.read_csv(
        'Chn_new_date_values.csv',
        parse_dates=['Date'],
        dayfirst=False,  # Ensures consistent parsing
    ).set_index('Date')
except FileNotFoundError:
    print("❌ Error: 'Chn_new_date_values.csv' not found. Please ensure the file is in the correct directory.")
    exit()  # Exit if the file is not found
except pd.errors.ParserError:
    print("❌ Error: CSV file format is incorrect. Ensure 'Date' is in 'YYYY-MM-DD' format.")
    exit()

# Check if 'Value' column exists
if 'Value' not in df.columns:
    print("❌ Error: Column 'Value' not found in the dataset.")
    exit()

# Add a 'year' column to the DataFrame
df['year'] = df.index.year

# Filter the DataFrame to include only 2019 and 2020
df = df[df['year'].isin([2019, 2020])]

# Calculate rolling average with robust handling of missing data
rolling_window = 7
df['Rolling_Avg'] = df['Value'].rolling(window=rolling_window, center=True, min_periods=1).mean()

# Define plot size
plt.figure(figsize=(18, 7))

# Plot shaded area for daily values, colored by year
for year, color in COLOR_MAP.items():
    df_year = df[df['year'] == year]
    plt.fill_between(df_year.index, df_year['Value'], color=color, alpha=0.2, label=f"{year} Daily Mentions")

# Plot daily values as a thin line, colored by year
for year, color in COLOR_MAP.items():
    df_year = df[df['year'] == year]
    sns.lineplot(data=df_year, x=df_year.index, y='Value', color=color, linewidth=3, alpha=0.99, label="")

# Plot rolling average with prominent styling
sns.lineplot(data=df, x=df.index, y='Rolling_Avg', color='000000', linestyle="-", linewidth=2, label=f"{rolling_window}-Day Rolling Avg")

# Generate dynamic title based on dataset range
start_date = df.index.min().strftime('%b %Y')
end_date = df.index.max().strftime('%b %Y')
plt.title(f"China Time-Series ({start_date} - {end_date})", fontsize=18, fontweight='bold', pad=25, color="#333F4B")

# Label axes with improved styling
plt.xlabel("Date", fontsize=15, labelpad=10, color="#333F4B")
plt.ylabel("Frequency of China Mentions", fontsize=15, labelpad=10, color="#333F4B")

# Format x-axis for better readability
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
plt.xticks(rotation=45, ha='right', fontsize=12, color="#333F4B")
plt.yticks(fontsize=12, color="#333F4B")

# Add legend with a clear frame
plt.legend(fontsize=12, loc="upper left", frameon=True, facecolor="white", edgecolor="black")

# Add subtle grid for better readability
plt.grid(color='grey', linestyle='--', linewidth=0.5)

# Ensure layout is optimized
plt.tight_layout(pad=2.5)
# plt.savefig("China_Mentions.pdf", dpi=300, bbox_inches='tight')

# Display the plot
plt.show()

# %% [markdown]
# # The same as beofre but with smooth it 

# %%

# %%

# %%

# %%

# %%

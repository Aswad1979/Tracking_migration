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
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
from scipy.stats import zscore
import matplotlib.dates as mdates

# Constants
YEARS = [2017, 2018, 2019, 2020]
COUNTRIES_HOSTING = ['usa', 'deu', 'sau', 'rus', 'gbr', 'are', 'fra', 'can', 'aus', 'tur']
COUNTRIES_ORIGIN = ['ind', 'mex', 'chn', 'syr', 'bgd', 'pak', 'ukr', 'phl', 'afg', 'idn', 'nga']
COLOR_MAP = {
    2017: "#000000",  # Black
    2018: "#2439F2",  # Blue
    2019: "#CB2C48",  # Red
    2020: "#008000"   # Green
}
ZSCORE_THRESHOLD = 10000

# Set seaborn style and figure size
sns.set(rc={'figure.figsize': (16, 4), 'font.family': 'serif', 'font.serif': ['Times New Roman']})
sns.set_style("ticks")

def load_data(filepath):
    """Load data from CSV file."""
    try:
        df = pd.read_csv(filepath, on_bad_lines='skip', index_col=False, parse_dates=['date'])
        df['year'] = pd.DatetimeIndex(df['date']).year
        df.index = pd.to_datetime(df["date"])
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def calculate_zscore_and_filter(df, column, threshold):
    """Calculate Z-scores and filter data based on a threshold."""
    df[f"Z_score_{column}_original"] = zscore(df[column])
    df_filtered = df[df[column] > threshold].copy()
    df_filtered.loc[:, f"Z_score_{column}"] = zscore(df_filtered[column])
    return df_filtered

def count_country_occurrences(df, countries):
    """Count occurrences of specific countries in the 'country' column."""
    for country in countries:
        df[country] = df['country'].str.count(country)
    return df

def calculate_zscore_for_countries(df, countries):
    """Calculate Z-scores for each country."""
    for country in countries:
        df.loc[:, f'Z_score_{country}'] = zscore(df[country])
    return df

# Updated function to get top N dates based on Z-scores
def get_top_dates(df, zscore_col, years, top_n=5):
    """Get the top N dates for each year based on the Z-score column."""
    top_dates = []
    for year in years:
        df_year = df[df['year'] == year]
        sorted_year = df_year.sort_values(by=[zscore_col], ascending=False)
        
        # Get top N rows based on Z-score
        top_dates_year = sorted_year.head(top_n)['date'].dt.strftime('(%b-%d)').tolist()
        top_dates.append(top_dates_year)
    
    return top_dates

def plot_country_zscores(df, zscore_col, years, color_map, top_dates):
    
    # Set global font and style settings
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['STIXGeneral'],
        'font.size': 12,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12,
        'legend.fontsize': 12
    })

    
    
    """Plot Z-scores for a specific country across multiple years and show top 5 dates in legend inside the plot."""
    plt.figure(figsize=(16, 4), dpi=300)  # Adjusted height for better readability
    ax = plt.gca()
    for i, year in enumerate(years):
        df_year = df[df['year'] == year]
        ts = pd.Series(df_year[zscore_col], index=df_year.index)
        ts.plot(
            linewidth=3.0,
            linestyle='-',
            color=color_map[year],
            marker='.',  # Add markers to the line
            markersize=5,  # Set marker size
            markerfacecolor='white',  # Set marker face color to white
            markeredgecolor=color_map[year],  # Set marker edge color to match the line color
            label=f"{year}: {', '.join(top_dates[i])}",
            ax=ax
        )
    
    # Add gridlines
    ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
    
    # Remove top and right spines
    # ax.spines['top'].set_visible(False)
    # ax.spines['right'].set_visible(False)
    
    # Bold axis labels and title
    plt.title(f"Z-Score for {zscore_col[8:].upper()} (2017-2020)", fontsize=14, fontweight='bold')
    plt.ylabel('Z-Score', fontweight='bold')
    # plt.ylabel('Z-Score', fontsize=10, fontweight='bold')
    # plt.xlabel('', fontsize=8, fontweight='bold')  # Explicitly set x-axis label to an empty string
    plt.xlabel('', fontweight='bold')  # Explicitly set x-axis label to an empty string
    
    # Adjust y-axis limits
    plt.ylim(-1, 26)
    
    # Format x-axis to show more dates
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))  # Show every 4 months
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))  # Format as "Jan 2017"
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
    
    # Explicitly set font size for tick labels
    ax.tick_params(axis='x')#, labelsize=8)  # Set x-axis tick label font size to 8
    ax.tick_params(axis='y')#, labelsize=8)  # Optionally set y-axis tick label font size to 8
    
    # Place the legend inside the plot box
    plt.legend(
        loc='upper right',  # Position the legend in the upper-right corner
        bbox_to_anchor=(1, 1),  # Slightly outside the plot box
        # fontsize=12,  # Reduce legend font size to 8
        title_fontsize=12,  # Optional: Adjust legend title font size if needed
        ncol=1,  # Single column for the legend
        # frameon=True,  # Add a border around the legend
        # shadow=True  # Add a shadow effect for better visibility
    )
    
    # Save plot as a PDF
    plt.tight_layout(rect=[0, 0, 1, 1])  # Reserve space for the legend
    plt.savefig(f"plot2025/{zscore_col[8:]}.pdf", format='pdf', bbox_inches='tight')
    plt.show()

# Main Execution
if __name__ == "__main__":
    # Load data
    df = load_data('2021_new_zscore_fixed.csv')
    if df is None:
        exit(1)
    
    # Process data
    df = calculate_zscore_and_filter(df, 'country_len', ZSCORE_THRESHOLD)
    df = count_country_occurrences(df, COUNTRIES_HOSTING + COUNTRIES_ORIGIN)
    df = calculate_zscore_for_countries(df, COUNTRIES_HOSTING + COUNTRIES_ORIGIN)
    
    # Generate plots for each country
    zscores = [f'Z_score_{country}' for country in COUNTRIES_HOSTING + COUNTRIES_ORIGIN]
    for zscore_col in zscores:
        top_dates = get_top_dates(df, zscore_col, YEARS)
        plot_country_zscores(df, zscore_col, YEARS, COLOR_MAP, top_dates)
        # break

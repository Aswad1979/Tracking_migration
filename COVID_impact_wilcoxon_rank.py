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
print("BisimeAllah")

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable


# Load and preprocess data
df_rank = pd.read_csv('WilcoxonFile.csv').rename(columns={
    "P2019_Jun": "Junrank19", "P2019_Jul": "Julrank19",
    "P2019_Aug": "Augrank", "P2019_Sep": "Seprank",
    "P2019_Oct": "Octrank", "P2019_Nov": "Novrank",
    "P2019_Dec": "Decrank", "P2020_Jan": "Janrank",
    "P2020_Feb": "Febrank", "P2020_Mar": "Marrank",
    "P2020_Apr": "Aprrank", "P2020_May": "Mayrank",
    "P2020_Jun": "Junrank", "P2020_Jul": "Julrank"
})

# Map country codes to include suffixes (e.g., USA -> USA-1)
suffix_map = {
    "USA": "USA-1", "MEX": "MEX-2", "IRQ": "IRQ-3", "GBR": "GBR-4", "DEU": "DEU-5",
    "ITA": "ITA-6", "TUR": "TUR-7", "SOM": "SOM-8", "FRA": "FRA-9", "ESP": "ESP-10",
    "SYR": "SYR-11", "CAN": "CAN-12", "SWE": "SWE-13", "VEN": "VEN-14", "AUS": "AUS-15",
    "CHN": "CHN-16", "IND": "IND-17", "GRC": "GRC-18", "NGA": "NGA-19", "IRN": "IRN-20"
}
df_rank['Country'] = df_rank['Country'].str.strip().str.upper().map(suffix_map)

# Prepare month pairs for rank changes (excluding Jun-19)
months = [
    "Julrank19", "Augrank", "Seprank", "Octrank", "Novrank",
    "Decrank", "Janrank", "Febrank", "Marrank", "Aprrank", "Mayrank", "Junrank"
]
month_labels = [
    "Jul-19", "Aug-19", "Sep-19", "Oct-19", "Nov-19",
    "Dec-19", "Jan-20", "Feb-20", "Mar-20", "Apr-20", "May-20", "Jun-20"
]

# Calculate rank changes between consecutive months (skip Jun-19)
rank_changes = df_rank[months].diff(axis=1)  # Skip Jun-19 by starting from Julrank19
rank_changes['Country'] = df_rank['Country']

# Create a mapping for month names to numeric positions
month_to_numeric = {month: i for i, month in enumerate(months)}


# Set global font and style settings
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['STIXGeneral'],
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 12,
    'ytick.labelsize': 8,
    'legend.fontsize': 10
})

# Plot the Gantt chart with color heatmap
fig, ax = plt.subplots(figsize=(16, 6))  # Adjust height for more countries
ax.set_facecolor('white')

# Normalize rank change magnitudes for color mapping
all_rank_changes = rank_changes.iloc[:, :-1].values.flatten()
all_rank_changes = all_rank_changes[~np.isnan(all_rank_changes)]  # Remove NaNs
norm = Normalize(vmin=min(all_rank_changes), vmax=max(all_rank_changes))
cmap = plt.cm.coolwarm  # Use a diverging colormap (blue for negative, red for positive)

# Iterate through each country and plot rank changes as horizontal bars
for idx, row in rank_changes.iterrows():
    country = row['Country']
    
    for i in range(len(row) - 2):  # Loop through rank changes
        start_month = months[i]  # Start of the bar
        end_month = months[i + 1]  # End of the bar
        rank_change = row.iloc[i + 1]  # Rank change value
        
        # Map months to numeric positions for plotting
        start_pos = month_to_numeric[start_month]
        end_pos = month_to_numeric[end_month]
        
        # Determine color based on rank change magnitude
        color = cmap(norm(rank_change))
        
        # Plot a horizontal bar for the rank change
        ax.barh(
            y=country,  # Country name on y-axis
            width=end_pos - start_pos,  # Width of the bar
            left=start_pos,  # Starting position
            height=0.6,  # Bar thickness
            color=color,
            edgecolor='none',  # Remove borders between bars for a flat look
            alpha=0.8,
            align='center'
        )

# Remove grid lines along the x-axis and y-axis
ax.grid(False)  # This disables all grid lines

# Optionally, if you want to remove the spines (lines around the plot)
for spine in ax.spines.values():
    spine.set_visible(False)

# Customize plot appearance
ax.set_title('Rank Changes Over Time (Gantt Chart)', fontsize=16, fontweight='bold', color='#333F4B')
ax.set_xlabel('Months', fontsize=12, fontweight='bold', color='#333F4B')
ax.set_ylabel('Countries', fontsize=12, fontweight='bold', color='#333F4B')
ax.axvline(x=0, color='black', linestyle='--', linewidth=1)  # Vertical reference line at x=0
ax.set_xlim(0, len(month_labels) - 1)
ax.set_ylim(-0.5, len(rank_changes) - 0.5)

# Set x-axis ticks and labels
ax.set_xticks(np.arange(len(month_labels)))
ax.set_xticklabels(month_labels, rotation=45, ha='right')

# Set y-axis ticks and labels
unique_countries = rank_changes['Country'].unique()
ax.set_yticks(range(len(unique_countries)))
ax.set_yticklabels(unique_countries)

# Add colorbar for magnitude of rank changes
sm = ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])  # Required for ScalarMappable
cbar = plt.colorbar(sm, ax=ax, orientation='vertical', pad=0.02, shrink=0.9, aspect=30)
cbar.set_label('Rank Change Magnitude', fontweight='bold')
cbar.ax.tick_params(labelsize=10)

# Tight layout and show plot
plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Adjust layout to accommodate legend
plt.show()

# Save the figure in high-resolution formats for journal submission
fig.savefig("Rank_Changes_Gantt_Heatmap_no.pdf", dpi=300, bbox_inches='tight')  # High-quality PDF
plt.close(fig)

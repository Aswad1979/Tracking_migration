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

# %%
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm
import matplotlib


# %%
def create_country_counts(df):
    """
    Aggregate the data by country code and create country counts
    """
    # Count occurrences of each country code
    country_counts = df['country code'].value_counts()
    
    # Save the country_counts into a new DataFrame
    country_data = pd.DataFrame(country_counts).reset_index()
    country_data.columns = ['Country Code', 'Count']
    
    # Rename columns to match the worldmap function expectations
    country_data = country_data.rename(columns={'Country Code': 'Alpha_2', 'Count': 'Population (Million)'})
    
    print(f"Successfully processed {len(country_data)} countries")
    print("Countries with data:")
    print(country_data.head(3))
    
    return country_data


# %%
def worldmap(data, x, y, z):
    """
    Create world map visualization from aggregated data
    """
    # Load your geographic data
    countries = gpd.read_file("countries.geojson")
    merged = countries.merge(data, left_on="ISO_A2", right_on="Alpha_2")
    
    # Ensure there are no non-positive values
    merged["Population (Million)"] = merged["Population (Million)"].replace(0, np.nan)
    merged.dropna(subset=["Population (Million)"], inplace=True)
    
    # Get colormap
    cmap = matplotlib.colormaps['viridis']
    
    # Apply logarithmic normalization
    norm = LogNorm(vmin=merged["Population (Million)"].min(), vmax=merged["Population (Million)"].max())
    
    # Calculate normalized values for each country
    normalized_values = norm(merged["Population (Million)"])
    
    # Get the actual color for each country
    colors = cmap(normalized_values)
    
    # Create a DataFrame with country info and colors
    color_df = pd.DataFrame({
        'Country': merged.get('NAME', merged.get('ADMIN', 'Unknown')),
        'Count': merged['Population (Million)'],
        'Normalized_Value': normalized_values,
        'Color_Hex': [matplotlib.colors.rgb2hex(color[:3]) for color in colors]
    })
    
    # Sort by count for better readability
    color_df = color_df.sort_values('Count', ascending=False)
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    merged.plot(column="Population (Million)", ax=ax, cmap=cmap, norm=norm)
    
    # Customize plot appearance
    ax.set_title(x)
    ax.axis("off")
    
    # Create and configure ScalarMappable with log normalization
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    
    # Add colorbar
    cax = fig.add_axes([0.92, 0.2, 0.02, 0.6])
    cbar = plt.colorbar(sm, cax=cax)
    cbar.set_label(y)
    
    # Display the plot
    plt.show()
    
    # Return the color DataFrame
    return color_df


# %%
# Load your df data
df_Place = pd.read_csv('places_filtered.csv')
df_Place = df_Place.rename(columns={'country_code': 'country code'})

# Create country counts from the individual coordinate data
country_data = create_country_counts(df_Place)

# Create the world map visualization
country_colors = worldmap(country_data,'Tweets Places Density Across Countries','Tweets density','World_Place')

# Save the results
country_colors.to_csv('Places_country_colors.csv', index=False)



# %%
# Load your df data
df_Geo = pd.read_csv('geoPlaces.csv')

# Create country counts from the individual coordinate data
country_data = create_country_counts(df_Geo)

# Create the world map visualization
country_colors = worldmap(country_data,'Tweets Geo Density Across Countries','Tweets density','World_Geo')

# Save the results
country_colors.to_csv('Geo_country_colors.csv', index=False)



# %%
# Load data and create visualization
df_Pop = pd.read_csv("195Countries.csv")
country_colors = worldmap(df_Pop, "Population Density Heatmap (Log Scale)", 'Population (Millions)', 'World_Population')

# Save the color information to CSV
country_colors.to_csv('Population_country_colors.csv', index=False)



# %%

# %%

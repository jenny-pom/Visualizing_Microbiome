import pandas as pd
import folium
from folium.plugins import MarkerCluster

####################################################################  Description  ######################################################################################
# This script is used for the fourth task where we are asked to create an interactive map showing the geographical distribution of the metagenomic samples. 
# It reads the metadata, extracts the latitude and longitude information, and creates a folium map with markers for each sample, colored by sequencing type (16S vs Shotgun). 
# The map is saved as an HTML file that can be embedded in a streamlit app.
#########################################################################################################################################################################

# Read you data
df = pd.read_csv("data/metadata/all_metadata.tsv", sep='\t')

# We need to find lat/lon columns. In this dataset, they are 'lat' and 'lon'.
df_coords = df.dropna(subset=['lat', 'lon']).copy()

# Create a folium map centered around the world
m = folium.Map(location=[20, 0], zoom_start=2, tiles='CartoDB positron')

# Added MarkerCluster which group nearby points together, which makes the map cleaner when there are many points
marker_cluster = MarkerCluster().add_to(m)

# Add points to the map
for idx, row in df_coords.iterrows():
    # Determine color based on sequencing type
    color = 'blue' if row['library_strategy'] == 'WGS' else 'green' # Shotgun = blue, 16S = green
    
    # Create a popup with info
    popup_text = f"""
    <b>Accession:</b> {row['sample_accession']}<br>
    <b>Type:</b> {row['library_strategy']}<br>
    <b>Country:</b> {row['country']}
    """
    
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=5,
        popup=folium.Popup(popup_text, max_width=300),
        color=color,
        fill=True,
        fill_opacity=0.7
    ).add_to(marker_cluster)

# Save the map as an HTML file 
m.save("results/vis/interactive_map.html")
print("Map saved to results/vis/interactive_map.html")

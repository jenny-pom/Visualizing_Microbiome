import pandas as pd
import folium
from folium import Popup
from folium.plugins import MarkerCluster
import os
from branca.element import IFrame
####################################################################  Description  ######################################################################################
# This script is used for the fourth task where we are asked to create an interactive map showing the geographical distribution of the metagenomic samples. 
# It reads the metadata, extracts the latitude and longitude information, and creates a folium map with markers for each sample, colored by sequencing type (16S vs Shotgun). 
# The map is saved as an HTML file that can be embedded in a streamlit app.
#########################################################################################################################################################################

# Setup paths
krona_folder = "results/taxonomy/krona_html/" # Path to the folder where your Krona HTML files are stored
metadata_path = "data/metadata/all_metadata.tsv"

# Read you data
df = pd.read_csv("data/metadata/all_metadata.tsv", sep='\t')
df_coords = df.dropna(subset=['lat', 'lon']).copy() # Find latitude and longitude columns.

# Create a folium map centered around the world
m = folium.Map(location=[20, 0], zoom_start=2, tiles='CartoDB positron')
marker_cluster = MarkerCluster().add_to(m) # Add MarkerCluster to group nearby points together

# Make a single loop for adding markers to the map, which will also include the Krona plot popups for each sample (that have it). This way I avoid multiple loops and make the code cleaner.
for idx, row in df_coords.iterrows():
    acc = row['run_accession']
    krona_file = f"{acc}.html" # Assuming the Krona files are named like 'SRR30914511.html', 'SRR30914512.html', 'SRR30914513.html'
    full_path = os.path.join(krona_folder, krona_file)

    dot_color = 'blue' if row['library_strategy'] == 'WGS' else 'green'

    # CHECK: Does a Krona plot exist for this specific accession
    if os.path.exists(full_path):
        with open(full_path, 'r', encoding='utf-8') as f:
            krona_content = f.read() # Read the pre-generated Krona HTML file for the sample

        # We use a standard IFrame here.    
        # If this is still blank, the Krona file itself likely requires an external 'krona.js' file.
        iframe = IFrame(html=krona_content, width=600, height=450)
        popup = folium.Popup(iframe, max_width=650)
        dot_color = 'orange'  # Keep them orange so you know which ones have maps!       
       
    else: 
        popup_text = f"<b>Accession:</b> {acc}<br><b>Strategy:</b> {row['library_strategy']}"
        popup = folium.Popup(popup_text, max_width=300)


    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=6,
        popup=popup,
        color=dot_color,
        fill=True,
        fill_opacity=0.8
    ).add_to(marker_cluster)

# Save the map as an HTML file 
m.save("results/vis/interactive_map.html")
print("Map saved to results/vis/interactive_map.html")

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
# -------------------------------------------------------------------------
########################## Description ####################################
# This script was built for making a interactive streamlit app where all...
# the data visualization created during the project is showed. 
###########################################################################

st.set_page_config(layout="wide") # Some visual adjustments for better display

st.title("Mine Microbiome Explorer") # App title
st.markdown("This tool visualizes Shotgun metadata and taxonomic profiles from global mine samples.") # Brief description of the app

# --- Create Tabs ---
tab_map, tab_krona, tab_stats = st.tabs(["Interactive Map", "Taxonomic Profile (Krona)", "Statistics"])

# ----- Interactive Map Tab -----
with tab_map: 
    st.header("Interactive Sample Map") 
    st.markdown("""
    **Geographical Distribution of Mine Microbiomes**
    * **Blue Dots**: Shotgun Metagenomic samples.
    * **Green Dots**: 16S rRNA Amplicon samples.
    * **Orange Dots**: Click to explore the microbial composition!
    """)

    map_path = "results/vis/interactive_map.html"
    
if os.path.exists(map_path):
    with open(map_path, 'r', encoding='utf-8') as f:
        html_data = f.read()
    
    components.html(html_data, height=700, scrolling=True)
else:
    st.error("Map file not found! Please run task_4.py first.")

# ----- Krona Taxonomy Visualization Tab ---
with tab_krona: # Second tab for the Krona taxonomy visualization
    st.header("Krona Taxonomy Visualization of 3 European Samples") # Header for the Krona section
    st.markdown("""
    ### How to Explore the Microbiome
This interactive **Krona Plot** visualizes the taxonomic composition derived from **MetaPhlAn 4**. 
The nested circles represent the hierarchical nature of life, allowing you to zoom from broad Domains down to specific genetic lineages.

**Key Taxonomic Ranks:**
* **p__ (Phylum):** Large groups like *Proteobacteria* or *Bacteroidetes*.
* **g__ (Genus):** The genus level, such as *Acidithiobacillus*, frequently found in mine environments.
* **s__ (Species):** The specific bacterial species name.
* **t__ (Strain/SGB):** **The Strain Level.** MetaPhlAn 4 utilizes **Species Genome Bins (SGBs)** to identify unique genetic clusters even when a formal species name is not yet assigned.

* **Tip:** Click on any wedge to zoom in. Use the drop-down menu on the top-left to switch between **Slovakia, UK, and Germany**.*
""", unsafe_allow_html=True)
   
    # Here we read the pre-generated Krona HTML file and embed it into the Streamlit app
    with open("results/taxonomy/krona_plots.html", 'r', encoding='utf-8') as f:
        krona_html = f.read()
        components.html(krona_html, height=800, scrolling=True)

        st.divider()

# I wanted to add a technical note section here to explain the processing challenges we faced with the Germany sample and how we resolved it, which is relevant for users interested in the bioinformatics aspect of the project.
st.expander("Technical Note: Processing Challenges (Germany Sample)").markdown("""
**Data Quality & Optimization:**
During the bioinformatic pipeline, the sample from **Germany (SRR5169068)** initially failed to generate a profile using standard MetaPhlAn 4 parameters. 

**Solution:**
Analysis revealed that the sequencing reads in this specific dataset were shorter than the default threshold. To include this sample in the comparative study, the parameter `--read_min_len 30` was applied. This adjustment ensured that shorter, high-quality reads were not discarded, allowing for a successful taxonomic reconstruction without compromising the integrity of the relative abundance calculations.
""")

# ----- Dataset Statistics Tab -----
with tab_stats:
    st.header("Dataset Statistics") # Header for the statistics section
    st.markdown("Overview of sample distribution by country and a comparison of sequencing strategies (16S vs. Shotgun).")
    col1, col2 = st.columns(2) # Create two columns for side-by-side display of statistics
    with col1: 
        st.subheader("Samples per Country")
        st.image("results/vis/task2_country_distribution.png") # Display the country distribution image
    with col2:
        st.subheader("16S vs Shotgun Distribution")
        st.image("results/vis/task3_sequencing_comparison.png") # Display the sequencing strategy comparison image
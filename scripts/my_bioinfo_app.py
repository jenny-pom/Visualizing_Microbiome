import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
# -------------------------------------------------------------------------
########################## Description ####################################
# This script was built for making a interactive streamlit app where all...
# the graphs created during the project is showed. 
###########################################################################

st.set_page_config(layout="wide") # Some visual adjustments for better display

st.title("Mine Microbiome Explorer") # App title
st.markdown("This tool visualizes Shotgun metadata and taxonomic profiles from global mine samples.") # Brief description of the app

# --- Create Tabs ---
tab_map, tab_krona, tab_stats = st.tabs(["Interactive Map", "Taxonomic Profile (Krona)", "Statistics"])

with tab_map: # First tab for the interactive map
    st.header("Interactive Sample Map") # Header for the map section
    st.markdown("This map visualizes the geographical origins of the metagenomic samples, including both shotgun (blue) and 16S (green) datasets, highlighting the diverse range of mine environments analyzed.")
    with open("results/vis/interactive_map.html", 'r', encoding='utf-8') as f:
        map_html = f.read() # Read the pre-generated interactive map HTML file
        components.html(map_html, height=600) # Embed the map into the Streamlit app with specified height

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
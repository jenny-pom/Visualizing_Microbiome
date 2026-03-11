import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

st.title("Mine Microbiome Explorer")
st.markdown("This tool visualizes Shotgun metadata and taxonomic profiles from global mine samples.")

# --- Create Tabs ---
tab_map, tab_krona, tab_stats = st.tabs(["Interactive Map", "Taxonomic Profile (Krona)", "Statistics"])

with tab_map:
    st.header("Interactive Sample Map")
    st.markdown("This map visualizes the geographical origins of the metagenomic samples, including both shotgun (blue) and 16S (green) datasets, highlighting the diverse range of mine environments analyzed.")
    with open("results/vis/interactive_map.html", 'r', encoding='utf-8') as f:
        map_html = f.read()
        components.html(map_html, height=600)

with tab_krona:
    st.header("Krona Taxonomy Visualization of 3 European Samples")
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
   
    # Here we read the pre-generated Krona HTML file and embed it directly into the Streamlit app
    with open("results/taxonomy/krona_plots.html", 'r', encoding='utf-8') as f:
        krona_html = f.read()
        components.html(krona_html, height=800, scrolling=True)

        st.divider()

# 2. Technical Note Section
st.expander("Technical Note: Processing Challenges (Germany Sample)").markdown("""
**Data Quality & Optimization:**
During the bioinformatic pipeline, the sample from **Germany (SRR5169068)** initially failed to generate a profile using standard MetaPhlAn 4 parameters. 

**Solution:**
Analysis revealed that the sequencing reads in this specific dataset were shorter than the default threshold. To include this sample in the comparative study, the parameter `--read_min_len 30` was applied. This adjustment ensured that shorter, high-quality reads were not discarded, allowing for a successful taxonomic reconstruction without compromising the integrity of the relative abundance calculations.
""")

        

with tab_stats:
    st.header("Dataset Statistics")
    st.markdown("Overview of sample distribution by country and a comparison of sequencing strategies (16S vs. Shotgun).")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Samples per Country")
        st.image("results/vis/task2_country_distribution.png")
    with col2:
        st.subheader("16S vs Shotgun Distribution")
        st.image("results/vis/task3_sequencing_comparison.png")
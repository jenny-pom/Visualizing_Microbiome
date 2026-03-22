import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os

# -------------------------------------------------------------------------
st.set_page_config(layout="wide", page_title="Mine Microbiome Explorer")

st.title("Mine Microbiome Explorer")
st.markdown("This tool visualizes Shotgun metadata and taxonomic profiles from global mine samples.")

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
        st.error("Map file not found! Please check the results/vis/ folder.")

# ----- Krona Taxonomy Visualization Tab ---
with tab_krona:
    st.header("Krona Taxonomy Visualization")
    st.markdown("""
    ### How to Explore the Microbiome
    This interactive **Krona Plot** visualizes the taxonomic composition derived from **MetaPhlAn 4**. 
    The nested circles represent the hierarchical nature of life, allowing you to zoom from broad Domains down to specific lineages.
    """)
    
    # 1. FIXED: These options now match the dictionary keys below EXACTLY.
    options = [
        "SRR30914511 (United Kingdom)", 
        "SRR34737771 (Slovakia)", 
        "SRR5169068 (Germany)"
    ]

    sample_choice = st.selectbox(
        "Select a specific European mine sample to visualize:",
        options
    )

    # 2. FIXED: Keys match the 'options' list to prevent KeyError.
    sample_to_file = {
        "SRR30914511 (United Kingdom)": "SRR30914511.html",
        "SRR34737771 (Slovakia)": "SRR34737771.html",
        "SRR5169068 (Germany)": "SRR5169068.html"
    }
    
    # Retrieve the filename from the dictionary based on the user's choice
    selected_filename = sample_to_file[sample_choice]
    
    # Path to the Krona HTML files
    krona_path = f"results/taxonomy/krona_html/{selected_filename}"

    # 3. OPEN THE FILE: Read and display the chosen one
    if os.path.exists(krona_path):
        with open(krona_path, 'r', encoding='utf-8') as f:
            krona_html = f.read()
            components.html(krona_html, height=800, scrolling=True)
    else:
        st.error(f"Krona file not found at: {krona_path}")

    st.divider()

    # Technical Note expander
    with st.expander("Technical Note: Processing Challenges (Germany Sample)"):
        st.markdown("""
        **Data Quality & Optimization:**
        During the bioinformatic pipeline, the sample from **Germany (SRR5169068)** initially failed to generate a profile using standard MetaPhlAn 4 parameters. 

        **Solution:**
        Analysis revealed that the sequencing reads in this specific dataset were shorter than the default threshold. To include this sample, the parameter `--read_min_len 30` was applied.
        """)

# ----- Dataset Statistics Tab -----
with tab_stats:
    st.header("Dataset Statistics")
    st.markdown("Overview of sample distribution by country and sequencing strategy.")
    col1, col2 = st.columns(2)
    with col1: 
        st.subheader("Samples per Country")
        if os.path.exists("results/vis/task2_country_distribution.png"):
            st.image("results/vis/task2_country_distribution.png")
    with col2:
        st.subheader("16S vs Shotgun Distribution")
        if os.path.exists("results/vis/task3_sequencing_comparison.png"):
            st.image("results/vis/task3_sequencing_comparison.png")

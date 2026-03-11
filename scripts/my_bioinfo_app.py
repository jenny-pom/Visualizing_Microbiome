import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide") # Make the app use the full width of the page

st.title("Mine Microbiome Explorer")
st.markdown("This tool visualizes Shotgun metadata from global mine samples.")

# --- Show Interactive Sample Map ---
st.header("Interactive Sample Map")
# Read the HTML file and embed it in Streamlit
with open("results/vis/interactive_map.html", 'r', encoding='utf-8') as f:
    html_data = f.read()
    components.html(html_data, height=500)

# --- Show Dataset Statistics ---
st.header("Dataset Statistics")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Samples per Country")
    st.image("results/vis/task2_country_distribution.png")
    
with col2:
    st.subheader("16S vs Shotgun Distribution")
    st.image("results/vis/task3_sequencing_comparison.png")

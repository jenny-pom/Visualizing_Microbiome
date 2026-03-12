import pandas as pd
# -------------------------------------------------------------------------
# This script reads the shotgun metagenomic data.
# Counts the number of unique locations represented in the dataset, and prints out the results. 
# It also provides a breakdown of the most common countries in the dataset.
# -------------------------------------------------------------------------

# Reading in the shotgun data seperated by tabs
df = pd.read_csv("data/shotgun_data/mine_shotgun_only.tsv", sep='\t')

# Count unique numbers of countries based on the 'country' column, which includes both country and province information
raw_count = df['country'].nunique()

# Use .str.split(':').str[0] to get the first part, which is the actual country name, and ignore the province information after the colon.
df['clean_country'] = df['country'].str.split(':').str[0]

# Count the number of unique countries without province information
actual_countries = df['clean_country'].nunique()

print(f"Number of unique locations (including provinces): {raw_count}")
print(f"Number of actual countries: {actual_countries}")

# Display the 5 most common countries
print("\n--- Top 5 Countries ---")
print(df['clean_country'].value_counts().head(5))

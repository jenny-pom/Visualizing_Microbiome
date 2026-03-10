import pandas as pd

# Load data
df = pd.read_csv("data/shotgun_data/mine_shotgun_only.tsv", sep='\t')

# 1. Count unique countries (including provinces)
raw_count = df['country'].nunique()

# 2. Create a "Clean Country" column that only takes the part before the colon
# We use .str.split(':').str[0] to get the first part
df['clean_country'] = df['country'].str.split(':').str[0]

# 3. Count the actual unique countries
actual_countries = df['clean_country'].nunique()

print(f"Number of unique locations (including provinces): {raw_count}")
print(f"Number of actual countries: {actual_countries}")

# Display the 5 most common countries
print("\n--- Top 5 Countries ---")
print(df['clean_country'].value_counts().head(5))

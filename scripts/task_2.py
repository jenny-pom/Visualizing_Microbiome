import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Upload data
file_path = "data/shotgun_data/mine_shotgun_only.tsv"
df = pd.read_csv(file_path, sep='\t')

# 2. Clean the data: Keep only the country (the text before the colon)
df['clean_country'] = df['country'].str.split(':').str[0]

# 3. Count samples per country and sort (from most to least)
country_counts = df['clean_country'].value_counts()

# 4. Create the plot
plt.figure(figsize=(12, 7))
# Use color palette ('mako' or 'viridis')
sns.barplot(x=country_counts.index, y=country_counts.values, palette='viridis')

# Add titles and labels
plt.title('Number of Shotgun Metagenome Samples per Country', fontsize=16, pad=20)
plt.xlabel('Country', fontsize=12)
plt.ylabel('Number of Samples', fontsize=12)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Add the exact number above each bar
for i, count in enumerate(country_counts.values):
    plt.text(i, count + 2, str(count), ha='center', fontweight='bold', fontsize=10)

# Change the style for better aesthetics
plt.tight_layout()

# 5. Save the plot
# We save both as PNG (for PowerPoint/Word) and PDF (for best quality)
plt.savefig("results/vis/task2_country_distribution.png", dpi=300)
plt.savefig("results/vis/task2_country_distribution.pdf")

print(f"Done! The plot for {len(country_counts)} countries has been saved in 'visualizations/'.")
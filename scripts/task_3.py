import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Read the data
file_path = "data/metadata/all_metadata.tsv"
df = pd.read_csv(file_path, sep='\t')

# 2. Clean the country names by taking only the part before the colon
df['clean_country'] = df['country'].str.split(':').str[0]

# Filter so that we only have Amplicon och Shotgun (WGS)
strategy_map = {'WGS': 'Shotgun Metagenome', 'AMPLICON': '16S rRNA Amplicon'}
df_plot = df[df['library_strategy'].isin(['WGS', 'AMPLICON'])].copy()
df_plot['Sequencing Type'] = df_plot['library_strategy'].map(strategy_map)

# 3. Creat the plot
plt.figure(figsize=(14, 8))

# We want to order the countries by the total number of samples (both 16S and Shotgun combined)
order = df_plot['clean_country'].value_counts().index

# 'hue' creates separate bars for 16S and Shotgun within each country, and 'order' ensures the countries are sorted by total count
sns.countplot(data=df_plot, x='clean_country', hue='Sequencing Type', order=order, palette='viridis')

# Add title and labels
plt.title('Distribution of 16S vs Shotgun Sequencing per Country', fontsize=16, pad=20)
plt.xlabel('Country', fontsize=12)
plt.ylabel('Number of Samples', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.legend(title='Sequencing Strategy')
plt.grid(axis='y', linestyle='--', alpha=0.3)

plt.tight_layout()

# 4. Save the plot
plt.savefig("results/vis/task3_sequencing_comparison.png", dpi=300)
plt.savefig("results/vis/task3_country_distribution.pdf", dpi=300)
print("Task 3 plot saved to results/vis/task3_sequencing_comparison.png")

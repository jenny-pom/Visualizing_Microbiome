import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

####################################################################  Description  ######################################################################################
# This script is used for the second task where we are asked to show the distribution of 16S vs Shotgun sequencing samples across different countries. 
# It reads the metadata, processes it to extract relevant information, and creates a bar plot that is saved as both PNG and PDF for use in the app and for presentations.
#########################################################################################################################################################################

# Read the data
file_path = "data/shotgun_data/mine_shotgun_only.tsv"
df = pd.read_csv(file_path, sep='\t') # Load the TSV file into a DataFrame

# Keep only the country name (remove any additional info after ':')
df['clean_country'] = df['country'].str.split(':').str[0]

# Count the number of samples per country
country_counts = df['clean_country'].value_counts()

# Create the bar plot
plt.figure(figsize=(12, 7))
# Use color palette that match the overall theme of the app
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

# Save both as PNG (for PowerPoint/Word) and PDF (for best quality)
plt.savefig("results/vis/task2_country_distribution.png", dpi=300)
plt.savefig("results/vis/task2_country_distribution.pdf")
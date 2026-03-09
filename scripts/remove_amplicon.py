import pandas as pd



# 1. Read the file into a DataFrame
# Vi använder sep='\t' eftersom det är en TSV-fil
file_path = "data/metadata/ALL_SAMPLES_combined_full_metadata.tsv"
data_frame = pd.read_csv(file_path, sep='\t')

# 2. See distribution of sequencing types (library_strategy)
print("--- Distribution of Sequencing Types ---")
print(data_frame['library_strategy'].value_counts()) # counts of each unique value in the 'library_strategy' column

# 3. TASK 2: Se fördelning per land (för alla prover)
print("\n--- Samples per Country (Task 2) ---"
print(data_frame['country'].value_counts())

# 4. Filtering: Only keep samples that are shotgun (WGS)
#'WGS' (Whole Genome Shotgun)
shotgun_df = data_frame[data_frame['library_strategy'] == 'WGS'].copy() # use .copy() to avoid SettingWithCopyWarning when we modify shotgun_df later

# 5. Save the filtered DataFrame to a new TSV file
output_path = "data/shotgun_data/mine_shotgun_only.tsv"
shotgun_df.to_csv(output_path, sep='\t', index=False)

print(f"\nSuccess! Filtered {len(shotgun_df)} shotgun samples to {output_path}")

# 6. Find samples from Sweden (Task 5)
sweden_samples = shotgun_df[shotgun_df['country'].str.contains("Sweden", na=False)]
print("\n--- Potential Swedish Shotgun Samples ---")
print(sweden_samples[['sample_accession', 'run_accession', 'lat', 'lon']])


# Define the path to your merged abundance table
MERGED="results/taxonomy/merged_abundance_table_2.txt"

# Extract sample names from the header (the line that starts with "clade_name")
SAMPLES=$(grep "^clade_name" $MERGED | cut -f2-)

col=2
for s in $SAMPLES; do
    # Get the sample name from the header to name the file correctly
    s_clean=$(echo $s | tr -d '\r')
    
    echo "Fixing format for: $s_clean (Column $col)"
    
    # 1. Skip lines starting with #
    # 2. Keep only lines with species-level (s__) to get nice circles
    # 3. Move the column to the beginning and clean the format
    grep -vE "clade_name|UNCLASSIFIED" $MERGED | awk -v col=$col -F'\t' '{print $col "\t" $1}' | sed 's/|/\t/g' > results/taxonomy/krona_${s_clean}.txt
    ((col++))
done

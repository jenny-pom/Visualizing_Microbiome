#!bin/bash
# Loop through the listed sampleID files and get metadata for each sample
# Usage: ./get_metadata.sh data/sample_IDs/filename.txt
# -------------------------------------------------------------------------

# Define variables
ID_FILES="$1" # Take the first argument given in the terminal
OUTPUT_DIR="data/metadata" #Define the output directory (hardcoded) for metadata files
BASENAME=$(basename "$ID_FILES" .txt) # Get the base name of the input file without extension
FINAL_TSV="$OUTPUT_DIR/${BASENAME}_metadata.tsv" # Define the output TSV file name based on the input file name

mkdir -p "$OUTPUT_DIR" # Create the output directory if it doesn't exist!

echo "start metadata retrieval for: $ID_FILES"

# Get the first sample ID from the input file to create the header for the output TSV file
first_id=$(head -n 1 "$ID_FILES" | tr -d '\r\n ')
curl -s "https://www.ebi.ac.uk/ena/portal/api/search?result=read_run&query=sample_accession=$first_id&fields=all&format=tsv" | head -n 1 > "$FINAL_TSV"

#Loop through the file 
while read id; do
    id=$(echo "$id" | tr -d '\r\n ')
    [[ -z "$id" ]] && continue  # Skip empty lines

    echo "Catching metadata for $id..."

    curl -s "https://www.ebi.ac.uk/ena/portal/api/search?result=read_run&query=sample_accession=$id&fields=all&format=tsv" | tail -n +2 >> "$FINAL_TSV"
    

done < "$ID_FILES"

echo "Done! Full metadata saved to: $FINAL_TSV"

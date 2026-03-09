# Loop through the file and get metadata for each sample

while read id; do
    echo "Hämtar data för $id..."
    curl -s "https://www.ebi.ac.uk/ena/portal/api/search?result=read_run&query=sample_accession=$id&fields=all&format=tsv" >> metadata/all_samples.tsv
done < samples.txt

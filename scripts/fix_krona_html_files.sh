cd results/taxonomy/cleaned_krona_samples/

# Loop through all the text files that match the pattern "krona_SRR*.txt"
for input_file in krona_SRR*.txt; do
    # Create output file names based on the input file name
    base_name=$(basename "$input_file" .txt)
    fixed_txt="${base_name}_FIXED.txt"
    html_out="${base_name}.html"

    echo "Fix format and create plot for: $base_name"

    # 1. Remove lines starting with # (headers)
    # 2. Remove k__, p__ etc. to clean the names
    # 3. Replace all pipes (|) with tabs (\t) so Krona understands the levels
    # 4. We use 'sed' to ensure the tab after the number is kept
    grep -v "#" "$input_file" | sed 's/[a-z]__//g' | tr '|' '\t' > "$fixed_txt"

    # Create the actual Krona plot
    ktImportText "$fixed_txt" -o "$html_out"
done

echo "Done! Now all your HTML files in the folder should have the correct content."

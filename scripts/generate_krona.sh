for txt_file in results/taxonomy/cleaned_krona_samples/*.txt; do
    
    filename=$(basename "$txt_file" .txt)
    
    # Define the output HTML file path
    html_output="results/taxonomy/krona_html/${filename}.html"
    
    echo "Converting $txt_file to $html_output..."
    
    # Create the Krona plot using ktImportText
    ktImportText "$txt_file" -o "$html_output"
done
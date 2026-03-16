# Visualising the Mine Microbiome  
**Author:** Jenny Laberg Nilsson   

## Project Overview  
This project analyses publicly available mine microbiome datasets from ENA (European Nuclear Archive). The workflow consist of following steps:
1. Extraction of sample metadata and raw FASTQ sequencing data.
2. Quality control
3. Implementation of MetaPhlAn 4 to perform high-resolution taxonomic analysis using clade-specific marker genes.
4. Generating interactive Krona plots to visualize the microbial diversity of each site.
5. Developing an interactive HTML dashboard to map the geographical distribution of samples alongside their corresponding taxonomic profiles.

## Data Sources  
Public datasets from ENA (European Nuclear Archive)
```bash
curl "https://www.ebi.ac.uk/ena/portal/api/search?result=read_run&query=sample_accession=SAMPLE_ID&fields=all&format=tsv"  
```

## Requirements & Envirolment  
This project uses two Conda environments to manage dependencies. Ensure you have Conda installed.  
Activate the environments used for the analysis (see folder env):
```bash  
# Create the environment from scratch  
conda create -n microbiome_env python=3.10 -c bioconda -c conda-forge  

# Activate the environment  
conda activate microbiome_env  

# Install core bioinformatic tools  
conda install -c bioconda xmlstarlet metaphlan kraken2 krona -y  

# Install data processing and plotting libraries  
conda install -c conda-forge pandas matplotlib leaflet -y  

# Export environment to a file for reproducibility   
conda env export > env/environment.yml  
```
**List of essential software:**  
Note: All software was installed using conda  
**Kraken2**	- Taxonomic classification  
**MetaPhlAn** - Metagenomic micriobial profiling   
**Krona** - Interactive taxonomy visualisation  
**Python/R** - Data processing and visualisation  

## Project Workflow & Log  

### 1. Project Set-up & Metadata Extraction   
Set up directory, initiate github and connect to github. Also retrieve the data and collect it in one master file.  
**Date:** 2026-03-09  
**Command run:**  
```bash  
#### Set-up of project directory and connect to github  
mkdir Visualizing_Microbiome  
mkdir scripts data results results/vis results/logs metadata  
touch REAME.md .gitignore  
git init  
git remote add origin https://github.com/jenny-pom/Visualizing_Microbiome.git  
git status  
git add .  
git commit -m  
git push  

# Generate script and collect metadata for mine microbiome samples  
# non drainage metadata  
bash scripts/get_metadata.sh data/sample_IDs/NCBI.mine.metagenome.sampleID.txt  
# drainage metadata  
bash scripts/get_metadata.sh data/sample_IDs/NCBI.mine.drainage.metagenome.sampleID.txt  

# find header index  
cat data/metadata/NCBI.mine.drainage.metagenome.sampleID_metadata.tsv | head -n2 | sed 's/\t/\n/g' | nl -ba  

# Take the first file including header  
cat data//sample_IDs/NCBI.mine.drainage.metagenome.sampleID.txt> data/sample_IDs/all_mine_samples.tsv  

# Take the next file (without header) and add it to make a file containing all sample IDs.  
tail -n +2 data/metadata/NCBI.mine.metagenome.sampleID.txt >> data/sample_IDs/all_mine_samples.tsv  

# Now create a master file containing all the metadata (both from drainage and non dranagie)  
# First add the header  
head -n 1 data/metadata/NCBI.mine.drainage.metagenome.sampleID_full_metadata.tsv > data/metadata/all_metadata.tsv  
 
# Second add the data from the drainage  
tail -n +2 data/metadata/NCBI.mine.drainage.metagenome.sampleID_full_metadata.tsv >> data/metadata/all_metadata.tsv  

# Lastly, add the data from the general mine metagenome  
tail -n +2 data/metadata/NCBI.mine.metagenome.sampleID_full_metadata.tsv >> data/metadata/all_metadata.tsv  
```
---

### 2. Data filtering  
Start filtering the data, this project will only focus on WGS (shotgun) data.  
**Date:** 2026-03-09  
**Command run:**  
```bash  
chmod +x remove_amplicon.py  

python scripts/remove_amplicon.py  
```
---

### 3. TASK 2 - Geographical Distrbution Visualization  
Make a script that visualise the number of samples over geographical distribution.  
**Date:** 2026-03-10  
**Command run:**  
```bash  
# Count the actual number of uniq countries by running count_contries.py, this is good to know before plotting.  
python scripts/count_countries.py   

Number of unique locations (including provinces): 46  
Number of actual countries: 10  
 
--- Top 5 Countries ---  
clean_country  
China             160  
USA               121  
Brazil             25  
Canada             15  
United Kingdom     11  
Name: count, dtype: int64  

#Run script to generate a barplot of sample geographical distribution  
python scripts/task_2.py  
```  
---


### 3. TASK 3 - 16S rRNA amplicon vs shotgun metagenome  
**Date:** 2026-03-10  
**Command run:**  
```bash  
nano task_3.py  
chmod +x task_3  
python scripts/task_3.py   
```
---

### 4. TASK 4 - Interactive Sample Map  
**Date:** 2026-03-10  
**Command run:**  
```bash  
nano task_4.py  
chmod +x task_4  
python scripts/task_4.py  
```
---

### 5. Add Streamlit  
**Date:** 2026-03-10  
**Command run:**  
```bash  
pip install streamlit streamlit-folium  
nano my_bioinfo_app.py  
chmod +x bioinfo_app.py  
streamlit run scripts/my_bioinfo_app.py  
```  
---

### 6. Sample Selection, FASTq quality control and trimming   
**Date:** 2026-03-10  
**Command run:**  
There where no WGS samples from Sweden so instead samples from 3 different countries in Europe were selceted:  
1. **SRR5169068**   
Country - Germany: Drei Kronen und Ehrt (Harz Mountains)  
Read count - 146909573  
Description - Characterization of carboxylesterases from Los Rueldos acid mine drainage formation  
Library strategy - WGS  
Library layout - PAIRED  

2. **SRR30914511**  
Country - United Kingdom: London (Actually I don't think this is the rigth location but there is no other information)  
Read count - 50713785  
Description - Illumina HiSeq 2500 sequencing: DNA of metagenome: acid mine drainage  
Library strategy - WGS  
Library layout - PAIRED  

3. **SRR34737771**  
Country - Slovakia: Roznava  
Read count - 17628455  
Description - DNBSEQ-T7 sequencing: DNA-Seq of metagenome: mine water  
Library strategy - WGS  
Library layout - SINGLE  

**Bioinformatic Pipeline**  
**QC:** FastQC v0.11.9  
**Processing:** `fastp` for adapter removal and quality  filtering  

**Date:** 2026-03-10  
**Command run:**  
```bash  
# After selecting samples, I ran this to save the metadata in an index text file  
paste <(head -n 1 data/metadata/all_metadata.tsv | tr '\t' '\n') <(grep "SRR5169068" data/me  
tadata/all_metadata.tsv | tr '\t' '\n') | cat -n > data/selected_samples_WGS/SRR5169068_index.txt  

paste <(head -n 1 data/metadata/all_metadata.tsv | tr '\t' '\n') <(grep "SRR34737771" data/me  
tadata/all_metadata.tsv | tr '\t' '\n') | cat -n > data/selected_samples_WGS/SRR34737771_index.txt  

paste <(head -n 1 data/metadata/all_metadata.tsv | tr '\t' '\n') <(grep "SRR30914511" data/me  
tadata/all_metadata.tsv | tr '\t' '\n') | cat -n > data/selected_samples_WGS/SRR30914511_index.txt  

conda install -c bioconda metaphlan krona -y  

# Make a directory for the raw fastq data  
mkdir -p data/raw_data  

# Download the fastaq data  
# SRR5169068 (Germany)  
nohup curl -L ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR516/008/SRR5169068/SRR5169068_2.fastq.gz -o data/raw_fastq_data/SRR5169068_2.fastq.gz > download_SRR5169068_2.log 2>&1 &  
nohup curl -L ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR516/008/SRR5169068/SRR5169068_1.fastq.gz -o data/raw_fastq_data/SRR5169068_1.fastq.gz > download_SRR5169068_1.log 2>&1 &  
# SRR30914511 (England)   
nohup sh -c 'curl -L ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR309/011/SRR30914511/SRR30914511_1.fastq.gz -o data/raw_fastq_data/SRR30914511_1.fastq.gz && curl -L ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR309/011/SRR30914511/SRR30914511_2.fastq.gz -o data/raw_fastq_data/SRR30914511_2.fastq.gz' > download_SRR30914511.log 2>&1 &  
# SRR34737771 (Slovakia)  
nohup curl -L ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR347/071/SRR34737771/SRR34737771.fastq.gz -o data/raw_fastq_data/SRR34737771.fastq.gz > data/raw_fastq_data/download_SRR34737771.log 2>&1 &  

# Make a directory for quality control  
mkdir -p data/raw_fastq_data/quality_control  

# Do fastqc on the raw fastq files before continuing with making Krona plots  
fastqc ../*.fastq.gz -o .  
```
## Quality Control Summary  
This section documents the initial quality assessment of the metagenomic samples using **FastQC**.  

#### Sample SRR30914511 (United Kingdom)  
**Type:** Paired-end | **Status:** Action Required (Trimming)  
Overall high base-call accuracy, but technical artifacts were identified in the reverse strand and adapter contamination in the forward strand.    
| Metric | Value |  
| :--- | :--- |  
| **Total Sequences** | 50,713,785 |  
| **Sequence Length** | 251 bp |  
| **GC Content** | 51% |  

#### Overrepresented Sequences  
| Strand | Sequence | Count | % | Possible Source |  
| :--- | :--- | :--- | :--- | :--- |  
| **Forward** | `GATCGGAAGAGCACACGTCTGAACTCC...` | 55,865 | 0.11% | TruSeq Adapter, Index 12 |  
| **Reverse** | `NNNNNNNNNNNNNNNNNNNNNNNNNN...` | 110,166 | 0.22% | Poly-N (No Hit) |  
| **Reverse** | `GATCGGAAGAGCGTCGTGTAGGGAAAG...` | 57,880 | 0.11% | Illumina PCR Primer 1 |  

> **Decision:** Trimming conducted using `fastp` to remove adapters and filter out Poly-N/low-quality segments before MetaPhlAn analysis.  

#### Sample SRR34737771 (Slovakia)  
**Type:** Single-end | **Status:** Passed  

Excellent quality data. No adapters detected and zero sequences flagged as poor quality.  

| Metric | Value |
| :--- | :--- |
| **Total Sequences** | 17,628,455 |
| **Sequence Length** | 150 bp |
| **GC Content** | 54% |

> **Decision:** No trimming required. Proceeding directly to taxonomic profiling with raw data.  
  
#### Sample SRR5169068 (Germany)  
**Type:** Paired-end | **Status:** Passed   

This is the largest dataset in the project. The sequences are shorter (51 bp) but show high consistency.  

| Metric | Value |  
| :--- | :--- |  
| **Total Sequences** | 146,909,573 |  
| **Sequence Length** | 51 bp |  
| **GC Content** | 44% |  

> **Decision:** Quality is high, but a light cleaning pass could be performed to ensure consistency with the other paired-end samples in the pipeline. However, due to time constraints and the fact that the reads are ONLY 50 bp, this step will not be performed.

```bash
# Perform trimming of SRR30914511 using fastp
mkdir -p data/trimmed_data_SRR30914511

# Make a quality control envirolment
conda create -n qc_env -c bioconda fastp -y
conda activate qc_env
fastp --version
fastp 0.23.4

# Start filtering  
fastp -i data/raw_fastq_data/SRR30914511_1.fastq.gz \
      -I data/raw_fastq_data/SRR30914511_2.fastq.gz \
      -o data/trimmed_data_SRR30914511/SRR30914511_1_trimmed.fastq.gz \
      -O data/trimmed_data_SRR30914511/SRR30914511_2_trimmed.fastq.gz \
      --detect_adapter_for_pe \ # Finds adaptor
      --trim_poly_g \ # Removes lost signal addition of G
      --thread 4 \
      --html results/qc/fastp_SRR30914511.html \ # Will generate report
      --json results/qc/fastp_SRR30914511.json
```
## Trimming Results (fastp)  
| Metric | Before Trimming | After Trimming |  
| :--- | :--- | :--- |  
| **Total Reads** | 101,427,570 | 100,658,838 (99.2%) |  
| **Total Bases** | 25.46 Gb | 24.91 Gb |  
| **Q30 Bases (%)** | 91.46% (avg) | 92.00% (avg) |  


**Filtering Details:**  
* **Low quality:** 590,396 reads removed.  
* **Too many Ns:** 44,690 reads removed.  
* **Too short:** 133,646 reads removed.  
* **Bases trimmed due to adapters:** 356,999,865 bp.  

> **Summary:** The trimming successfully removed over 350 MB of adapter sequences while retaining 99.2% of the total reads. The Q30 score improved, providing high-quality input for taxonomic profiling.  
---

### 7 MetaPhlAn Taxonomic Analysis  
**Date:** 2026-03-11  
**Command run:**  
```bash  
###### Start Taxonomic Analysis #######  
# Make a directory for the taxonomy result  
mkdir -p results/taxonomy  
conda activate metaphlan_env # Eller vad din miljö heter

mkdir -p results/profiling

# Sample from England
nohup metaphlan data/trimmed_data_SRR30914511/SRR30914511_1_trimmed.fastq.gz,data/trimmed_data_SRR30914511/SRR30914511_2_trimmed.fastq.gz \
  --input_type fastq \
  --db_dir /home/inf-22-2025/miniconda3/envs/microbiome_env/lib/python3.10/site-packages/metaphlan/metaphlan_databases/ \
  -x mpa_vJan25_CHOCOPhlAnSGB_202503 \
  --mapout results/taxonomy/SRR30914511.bowtie2.bz2 \
  --nproc 8 \
  -o results/taxonomy/SRR30914511_profile.txt > results/logs/metaphlan_UK.log 2>&1 &

# Slovakia
nohup metaphlan data/raw_fastq_data/SRR34737771.fastq.gz \
  --input_type fastq \
  --db_dir /home/inf-22-2025/miniconda3/envs/microbiome_env/lib/python3.10/site-packages/metaphlan/metaphlan_databases/ \
  -x mpa_vJan25_CHOCOPhlAnSGB_202503 \
  --nproc 8 \
  -o results/taxonomy/SRR34737771_profile.txt > results/logs/metaphlan_Slovakia.log 2>&1 &

# Germany
nohup metaphlan --input_type fastq \
--db_dir /home/inf-22-2025/miniconda3/envs/microbiome_env/lib/python3.10/site-packages/metaphlan/metaphlan_databases/ \
-x mpa_vJan25_CHOCOPhlAnSGB_202503 \
--nproc 8 \
-o results/taxonomy/SRR5169068_profile.txt data/raw_fastq_data/SRR5169068_1.fastq.gz,data/raw_fastq_data/SRR5169068_2.fastq.gz > results/logs/metaphlan_Germany.log 2>&1 &

# Check that they are running: 
ps -u inf-22-2025 | grep -E "metaphlan|bowtie2"
```
---

### 8. Integration with Interactive Kronan Map  
**Date:** 2026-03-11  
**Command run:**  
```bash
# After creating the 3 *_profile.txt files we run this to unify them to one single table. 
merge_metaphlan_tables.py results/taxonomy/*_profile.txt > results/taxonomy/merged_abundance_table.txt


# In order to create the Kronan Map the file format has to be corrected
grep -E "s__|clade_name" results/taxonomy/merged_abundance_table.txt | cut -f1,3- | sed 's/clade_name/Sample/' | sed 's/s__//g' > results/taxonomy/merged_abundance_table_krona.txt

# Remove headers and UNCLASSIFIED, use awk to move column 2 to the start, followed by taxonomy.
grep -vE "clade_name|UNCLASSIFIED" results/taxonomy/merged_abundance_table.txt | awk -F'\t' '{print $2 "\t" $1}' | sed 's/|/\t/g' > results/taxonomy/krona_slovakia.txt

# Repeat 
grep -vE "clade_name|UNCLASSIFIED" results/taxonomy/merged_abundance_table.txt | awk -F'\t' '{print $3 "\t" $1}' | sed 's/|/\t/g' > results/taxonomy/krona_germany.txt

# Repeat 
grep -vE "clade_name|UNCLASSIFIED" results/taxonomy/merged_abundance_table.txt | awk -F'\t' '{print $4 "\t" $1}' | sed 's/|/\t/g' > results/taxonomy/krona_uk.txt

# Create one Krona plot for each sample together
ktImportText \
  results/taxonomy/krona_slovakia.txt,Slovakia \
  results/taxonomy/krona_germany.txt,Germany \
  results/taxonomy/krona_uk.txt,UK \
  -o results/taxonomy/krona_plots.html

# In hindsight, I also decided to run Krona for each of the three samples separately so that I could try to integrate them with my interactive sample map.
ktImportText krona_slovakia.txt -o krona_slovakia.html

ktImportText krona_germany.txt -o krona_germany.html

ktImportText krona_uk.txt -o krona_uk.html
```

### 8. Expanding the Interactive Kronan Map 
This step was not necessary but something I tired after getting feedback from Eran.    
**Date:** 2026-03-12  
**Command run:**  
```bash
# Downloading all fastq files from my mine_shotgun_only.tsv, I used the metadata 95 column that has a fastq_ftp link
awk -F'\t' 'NR>1 {print $95}' shotgun_data/mine_shotgun_only.tsv | tr ';' '\n' > all_sho
tgun_fastq_ftp/ftp_list.txt

# Now I will download everything (2 files at a time), this will take A VERY LONG TIME. Big mistake: This was not so smart since I ran out of RAM on the server.
nohup xargs -n 1 -P 2 wget -q -P data/raw_fastq_data_ALL_WGS/ < data/all_shotgun_fastq_ftp/ft
p_list.txt > download_progress.log 2>&1 &

# Space ran out and I decided to remove any files that had not downloaded proberly due to space limitation
find data/raw_fastq_data_ALL_WGS/ -name "*.fastq.gz" -size -1M -delete

g thorugh the folder: krona_html, which takes each one by one
bash scripts/generate_krona.sh 
```
```bash
# I will not do ANY quality control on following samples because of time restriction
# Run metaphlan on all fastqc over nigth
nohup bash -c 'for f in data/raw_fastq_data_ALL_WGS/*.fastq.gz; do
    sample_id=$(basename "$f" .fastq.gz)
    echo "Starting analysis for: $sample_id"

    metaphlan "$f" \
      --input_type fastq \
      --db_dir /home/inf-22-2025/miniconda3/envs/microbiome_env/lib/python3.10/site-packages/metaphlan/metaphlan_databases/ \
      -x mpa_vJan25_CHOCOPhlAnSGB_202503 \
      --nproc 4 \
      --read_min_len 30 \ # Essential since I didn't do any QC
      -o "results/profiles_ALL_WGS/${sample_id}_profile.txt"

    echo "Finished $sample_id"
done' > metaphlan_overnight.log 2>&1 &
```
```bash
# In the meantime I trid to integrate the 3 samples from Germany, Slovakia and UK to the interactive sample map. I did this by modifying the task_4.py script.

# I ended up with a total of 29 finsihed fastq files and I will be running KRONA plots on all of them.

# Merge them using the merge_metaphlan script 
merge_metaphlan_tables.py results/profiles_ALL_WGS/*_profile.txt > results/taxonomy/merged_abundance_table_2.txt

# Clean the table (just like I did priviously)
bash scripts/clean_merged_abundance_table.sh 

# It turned out that the additional 8 samples I had made didn't have any coordinate specified! So they won't show up on the map. :(
```
## References  

https://doi.org/10.1038/s41587-023-01688-w  
http://doi.org10.1038/s41598-017-03315-6  
http://doi.org10.3389/fmicb.2025.1675058  
https://doi.org/10.1111/1758-2229.70261  
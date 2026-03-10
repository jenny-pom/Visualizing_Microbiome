# Visualising the Skin Microbiome
Exploring the publicly available  mine mic## References
OBS!! Add more before hand-in
https://doi.org/10.1038/s41587-023-01688-wrobiome dataset to alayse geographical disrtibution and microbial composition using metagenomic and shotgun sequenced data. 
**Author:** Jenny Laberg Nilsson  

## Project Overview 
This project analyses publicly available skin microbiome datasets from NCBI. The workflow extracts metadata, visualizes geographical sample distribution, and performs microbial profiling on selected Swedish samples.
The Workflow:
1.
2.
3.
4.
...

## Data Sources
Public datasets from NCBI
curl "https://www.ebi.ac.uk/ena/portal/api/search?result=read_run&query=sample_accession=SAMPLE_ID&fields=all&format=tsv"

Example of sample accession: SAMEA121737266

## Requirements & Envirolment
This project uses a Conda environment to manage dependencies. Ensure you have Conda installed.
Activate the environment used for the analysis:
################ TODO!!!!! Update this or change it if necessary before hand in #####################
```bash 
# Create the environment from scratch
conda create -n microbiome_env python=3.10 -c bioconda -c conda-forge

# Activate the environment
conda activate microbiome_env

# Install core bioinformatic tools
conda install -c bioconda xmlstarlet metaphlan kraken2 krona -y

# Install data processing and plotting libraries
conda install -c conda-forge pandas matplotlib leaflet -y

# TODO: Update this before hand in!!!!!!!!!!!! 
# Export environment to a file for reproducibility 
conda env export > env/environment.yml
```
######## TODO!! Update this before hand-in
Tool	Purpose
Kraken2	Taxonomic classification
MetaPhlAn Metagenomic micriobial profiling 
Krona Interactive taxonomy visualisation 
Python/R Data processing and visualisation

Example installation:
ADD


## Project Workflow & Log

### 1. Project Set-up & Metadata Extraction 
Set up directory, initiate github and connect to github. Also retrieve the data and collect it in one master file. 
**Date:** 2026-03-09
**Command run:**
```bash
#### Set-up of project directory and connect to github ####
mkdir Visualizing_Microbiome
mkdir scripts data results results/vis results/logs metadata
touch REAME.md .gitignore
git init
git remote add origin https://github.com/jenny-pom/Visualizing_Microbiome.git
git status
git add .
git commit -m
git push

#### Generate script and collect metadata for mine microbiome samples ####
# non drainage metadata
bash scripts/get_metadata.sh data/sample_IDs/NCBI.mine.metagenome.sampleID.txt
# drainage metadata
bash scripts/get_metadata.sh data/sample_IDs/NCBI.mine.drainage.metagenome.sampleID.txt 

# find header index 
cat data/metadata/NCBI.mine.drainage.metagenome.sampleID_metadata.tsv | head -n2 | s
ed 's/\t/\n/g' | nl -ba

# Now create a master file containing all the metadata (both from drainage and non dranagie)
# First add the header
head -n 1 data/metadata/NCBI.mine.drainage.metagenome.sampleID_full_metadata.tsv > data/metadata/all_metadata.tsv

# Second add the data from the drainage
tail -n +2 data/metadata/NCBI.mine.drainage.metagenome.sampleID_full_metadata.tsv >> data/metadata/all_metadata.tsv

# Lastly, add the data from the general mine metagonome
tail -n +2 data/metadata/NCBI.mine.metagenome.sampleID_full_metadata.tsv >> data/metadata/all_metadata.tsv
```

### 2. Data filtering
Start filtering the data, this project will only work with WGS (shotgun) data.
**Date:** 2026-03-09
**Command run:**
```bash
chmod +x remove_amplicon.py

python scripts/remove_amplicon.py 

```

### 3. TASK 2 - Geographical Distrbution Visualization
Make a script that visualise the number of samples over geographical distrubution.
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
### 3. TASK 3 - 16S rRNA amplicon vs shotgun metagenome
**Date:** 2026-03-10
**Command run:**
```bash
# Take the first file including header
cat data/metadata/NCBI.mine.drainage.metagenome.sampleID_metadata.tsv > data/sample_IDs/all_mina_samples.tsv

# Take the next file (without header) and add it. 
tail -n +2 data/metadata/NCBI.mine.metagenome.sampleID_metadata.tsv >> data/sample_IDs/all_mine_samples.tsv
```

### 4. Interactive Sample Map

### 5. Swedish Sample Selection

### 6. Microbial Profiling

### 7 Krona Visualization

### 8. Integration with Interactive Map

## Project structure

## References
TODO!!! Add more before hand-in
https://doi.org/10.1038/s41587-023-01688-w

# Visualising the Mine Microbiome  
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

# Lastly, add the data from the general mine metagonome  
tail -n +2 data/metadata/NCBI.mine.metagenome.sampleID_full_metadata.tsv >> data/metadata/all_metadata.tsv  
```
---

### 2. Data filtering  
Start filtering the data, this project will only work with WGS (shotgun) data.  
**Date:** 2026-03-09  
**Command run:**  
```bash  
chmod +x remove_amplicon.py  

python scripts/remove_amplicon.py  
```
---

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
There where no WGS samples from Sweden so instead samples from 3 different countries in Europe were selceted:  
1. **SRR5169068**   
Country - Germany: Drei Kronen und Ehrt (Harz Mountains)  
Read count - 146909573  
Description - Characterization of carboxylesterases from Los Rueldos acid mine drainage formation  
Library strategy - WGS  
Library layout - PAIRED  

2. **SRR30914511**  
Country - United Kingdom: London  
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
1.  **QC:** FastQC v0.11.9
2.  **Processing:** `fastp` for adapter removal and quality filtering
**Date:** 2026-03-10  
**Command run:**  
```bash  
# After selecting samples, I ran this to same the metadata in an index text file  
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
#### Quality Control Summary  
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

> **Decision:** Quality is high, but a light cleaning pass could be performed to ensure consistency with the other paired-end samples in the pipeline. However, due to time constraints, this step will not be performed.

```bash
# Perform trimming of SRR30914511 using fastp
mkdir -p data/trimmed_data_SRR30914511

# Make a quality control envirolment
conda create -n qc_env -c bioconda fastp -y
conda activate qc_env
fastp --version
# fastp 0.23.4

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
#### Trimming Results (fastp)  
| Metric | Before Trimming | After Trimming |  
| :--- | :--- | :--- |  
| **Total Reads** | 101,427,570 | 100,658,838 (99.2%) |  
| **Total Bases** | 25.46 Gb | 24.91 Gb |  
| **Q30 Bases (%)** | 91.46% (avg) | 92.00% (avg) |  
| **Adapter Trimmed Reads** | - | 11,718,317 (11.5%) |  
| **Duplication Rate** | - | 15.84% |  

**Filtering Details:**  
* **Low quality:** 590,396 reads removed.  
* **Too many Ns:** 44,690 reads removed.  
* **Too short:** 133,646 reads removed.  
* **Bases trimmed due to adapters:** 356,999,865 bp.  

> **Summary:** The trimming successfully removed over 350 MB of adapter sequences while retaining 99.2% of the total reads. The Q30 score improved, providing high-quality input for taxonomic profiling.  
---

### 7 MetaPhlAn Taxonomic Analysis  
**Date:** 2026-03-10  
**Command run:**  
```bash  
###### Start Taxonomic Analysis #######  
# Make a directory for the taxonomy result  
mkdir -p results/taxonomy  
conda activate metaphlan_env # Eller vad din miljö heter

mkdir -p results/profiling

# Sample from England
metaphlan data/trimmed_data_SRR30914511/SRR30914511_1_trimmed.fastq.gz,data/trimmed_data_SRR30914511/SRR30914511_2_trimmed.fastq.gz \
          --input_type fastq \
          --add_viruses \
          --bowtie2out results/profiling/SRR30914511.bowtie2.bz2 \
          --nproc 8 \
          -o results/profiling/SRR30914511_profile.txt


# Slovakia
metaphlan data/raw_fastq_data/SRR34737771.fastq.gz \
          --input_type fastq \
          --add_viruses \
          --bowtie2out results/profiling/SRR34737771.bowtie2.bz2 \
          --nproc 8 \
          -o results/profiling/SRR34737771_profile.txt


# Germany
metaphlan data/raw_fastq_data/SRR5169068_1.fastq.gz,data/raw_fastq_data/SRR5169068_2.fastq.gz \
          --input_type fastq \
          --add_viruses \
          --bowtie2out results/profiling/SRR5169068.bowtie2.bz2 \
          --nproc 8 \
          -o results/profiling/SRR5169068_profile.txt

```
---

### 8. Integration with Interactive Map  



## Project structure  

## References  
TODO!!! Add more before hand-in  
https://doi.org/10.1038/s41587-023-01688-w  

#!/bin/bash

# Skapa mapp för resultat
mkdir -p results/taxonomy

echo "Startar MetaPhlAn för Tyskland (Paired)..."
metaphlan data/raw_data/SRR5169068_1.fastq.gz,data/raw_data/SRR5169068_2.fastq.gz \
    --input_type fastq --add_viruses --nproc 8 -o results/taxonomy/SRR5169068_profile.txt

echo "Startar MetaPhlAn för UK (Paired)..."
metaphlan data/raw_data/SRR30914511_1.fastq.gz,data/raw_data/SRR30914511_2.fastq.gz \
    --input_type fastq --add_viruses --nproc 8 -o results/taxonomy/SRR30914511_profile.txt

echo "Startar MetaPhlAn för Slovakien (Single)..."
metaphlan data/raw_data/SRR34737771.fastq.gz \
    --input_type fastq --add_viruses --nproc 8 -o results/taxonomy/SRR34737771_profile.txt

echo "Alla körningar är klara!"

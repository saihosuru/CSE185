# CSE185
Group Project 

#cat ~/public/lab7/lab7_accessions.txt | xargs -I {} sh -c 'wget -O - "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={}&rettype=fasta&retmode=text" | awk "{if (NR==1) print \">{}\"; else print}"' > ~/lab7/lab7_virus_genomes.fa



Tool: Make TagDirectory , input : Bam files , 

output: doing lots of preprocessing steps: removing reads that do not align to a unique position in the genome, separating reads by chromosome and sorting them by position, calculating how often reads appear in the same position to estimate the clonality (i.e. PCR duplication), calculating the relative distribution of reads relative to one another to estimate the ChIP-fragment length, calculating sequence properties and GC-content of the reads and performing a simple enrichment calculation to check if the experiment looks like a ChIP-seq experiment


We are going to compare it with makeTagdirectory and comparing the resuts to IGV

1) Since Tagdirectories take in BAM files, could we make our tool with input as SAM file instead of BAM file
2) How to work with BAM files, 

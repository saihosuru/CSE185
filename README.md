# CSE185
Group Project 

#cat ~/public/lab7/lab7_accessions.txt | xargs -I {} sh -c 'wget -O - "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={}&rettype=fasta&retmode=text" | awk "{if (NR==1) print \">{}\"; else print}"' > ~/lab7/lab7_virus_genomes.fa

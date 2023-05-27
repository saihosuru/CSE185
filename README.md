# README
SEAG is a command line tool for producing DNA sequence alignment data on single-ended DNA. It takes as input two files. One file contains a long reference genome sequence while the other file contains many reads, or short fragments of DNA that will be aligned to the genome sequence.

The reads can come from any kind of sequencing experiment (e.g. ATACSeq, ChIP-Seq) as long as both the genome sequence and reads are DNA/cDNA sequences.


### Authors:
Srijan Chakraborty

Hanzhong Yang

Sai Hosuru

*Each author has played an equal role in the development of the software.*

### Usage
$ python3 SEAG <refGenome.fa/fasta> <fragments.fq/fastq> (outputFileName.sam)

###### Inputs
Reference genome (must be a fasta file ending in ".fa" or ".fasta")
Read fragments (must be a fastq file ending in ".fq" or ".fastq")
OPTIONAL: Output file name (must be a .sam file)

###### Output
Default output will be "out.sam", unless output file name is specified.


### Required Packages
pyfaidx

###### Installation Instructions
In command line on UNIX, enter:
"pip install pyfaidx"

# README
SEAG is a command line tool for producing DNA sequence alignment data on single-ended DNA. It takes as input two files. One file contains a long reference genome sequence while the other file contains many reads, or short fragments of DNA that will be aligned to the genome sequence.

The reads can come from any kind of sequencing experiment (e.g. ATACSeq, ChIP-Seq) as long as both the genome sequence and reads are DNA/cDNA sequences.

The SEAG program utilizes a multiway-trie string searching algorithm. It constructs a MWT using the reads provided by the sequencing experiment (.fq/.fastq). A moving frame is then created on the genome that slides up the genome, checking each substring to see if it exists in the multi-way trie. If it exists, the read corresponding the entry in the MWT is mapped to the specific location in the genome that the frame is accessing. It does so until it reaches the end of the genome.

The SEAG program operates under the "perfect match" principle. This means that any difference between the genome substring and the read will be reason to not associate the read to that genome position. This means that some reads that have sequencing errors may not be mapped to any region in the genome. Near-perfect matches are excluded. It is expected that not all reads will be mapped to the genome.


### Authors:
Srijan Chakraborty

Hanzhong Yang

Sai Hosuru

*Each author has played an equal role in the development of the software.*

### Usage
$ python3 SEAG [refGenome.fa/.fasta] [fragments.fq/.fastq] (outputFileName.sam)

###### Inputs
Reference genome (must be a fasta file ending in ".fa" or ".fasta")
Read fragments (must be a fastq file ending in ".fq" or ".fastq")
OPTIONAL: Output file name (must be a .sam file)

###### Output
Default output will be "out.sam", unless output file name is specified.


### Required Packages
pyfaidx - to read FASTA files and get sequences for each chromosome.

###### Installation Instructions
In command line on UNIX, enter:
"pip install pyfaidx"

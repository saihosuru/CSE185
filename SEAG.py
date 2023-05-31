#!/usr/bin/env python
# coding: utf-8

# In[ ]:


################################################################################
### This file takes in either 2 or 3 files: a reference genome FASTA file    ###
### (.fa, .fasta), and either one FASTQ file of reads or two FASTQ files in
### the case of a paired-end reads. 
###
### The SAMGenerator outputs a tab-separated .sam file with details 
### regarding all the alignments and all other details.
###
### Columns and fields:
### 1. Query Name (type String)
### 2. Record Flag (type int)
### 3. Reference Name (type String)
### 4. Position in the genome ()
### 5. Mapping Quality (type int, Max 255)
### 6. CIGAR string (type String)
### 7. reference of next segment (type string)
### 8. position of the next segment (type string)
### 9. Observed length of template (type string)
### 10. The actual sequence (type String)
### 11. ASCII PHRED-encoded base qualities.
###






### SAM/BAM docs
# https://seqan.readthedocs.io/en/seqan-v1.4.2/Tutorial/BasicSamBamIO.html#:~:text=SAM%20files%20are%20TSV%20(tab,followed%20by%20tab%2Dseparated%20tags.


# In[4]:


# Step: Check command line input, return error if not proper input
#-G for genome .fa file 
#Genome_File
#-R - read fastq file 
#Read_File
# -RS - multiple read fastq files 
#Read_File - list 

# Usage:
# python3 SAMGenerator.py <genome.fa/.fasta> <reads1.fq/.fastq> (reads2.fq/fastq)




import sys, argparse
#print(len(sys.argv))
### Return error message if not appropriate arguments
if not (len(sys.argv) == 3 or len(sys.argv) == 4):
    print("USAGE ERROR: appropriate number of input files not present.")
    print("Usage: python3 SAMGenerator.py <genome.fa/.fasta> <reads1.fq/.fastq> (outputfile.sam)")
    sys.exit(1)

if (len(sys.argv) == 4)):
    if not (sys.argv[3][-4:] == '.sam'):
        print("USAGE ERROR: output file name does not end in \'.sam\'. ")
        print("Usage: python3 SAMGenerator.py <genome.fa/.fasta> <reads1.fq/.fastq> (outputfile.sam)")
        sys.exit(1)
    
#Copy filenames into an array of filenames to be opened sequentially
fqFiles = []
for i in range(len(sys.argv)):
    fqFiles.append(sys.argv[i])

        
#genome file has been opened and initialized.
#fastq files are not opened, but filenames are in array

#Author: Srija


# In[ ]:


# Step: Check validity of files\
import os 

#Checks if the Genome file exists in the path 
if not os.path.exists(fqFiles[1]):
    print("File path does not contain this Genome File")
    sys.exit(1)
    
#Checks if the Genome file ends with .fa to see if its a fasta file 

if not (fqFiles[1].lower().endswith(".fasta") or fqFiles[1].lower().endswith(".fa")):
    print("Genome File is not a FASTA file.")
    sys.exit(1)

#For the remaining input 
    # Check if the read file exists in the path 
if not os.path.exists(fqFiles[2]):
    print("Read File path does not contain the file")
    sys.exit(1)

    # Check if the read file ends with .fastq
if not (fqFiles[2].lower().endswith(".fastq") or fqFiles[2].lower().endswith(".fq")):
    print("The Read File is not a FASTQ file.")
    sys.exit(1)

# If it reaches this point then all the files provided are correct 
print("Files are valid and they do exist.")


# In[ ]:

def TrieConstruction(Patterns):
    ''' 
    TrieConstruction(Patterns)
    
    Takes an input of an array of strings called "Patterns" and returns
    a Node object representing a multiway trie. The multiway trie contains
    all the strings present in Patterns in the form of Node objects, with
    each edge representing a single letter in a string.
    
    The multiway trie is traversible by accessing a node's edges until
    
    '''
    
    
    #Initialize an empty collection of nodes
    Trie = {} 
    newNode = 0
    
    #For each string
    for element in Patterns:
        pattern = element[1]
        currentNode = 0             #tracker variable
        patternNode = 0             #tracker variable
        
        #For each letter in the string
        for i in range(len(pattern)):
            currentSymbol = pattern[i]
            
            #if the letter is ANYWHERE in the tree:
            if currentNode in Trie:
                Cont = False
                
                #Traverse the tree to find where to add a new node
                for edge in Trie[currentNode]:
                    
                    #if the edge is already the next letter that we want to add:
                    if edge[1] == currentSymbol:
                        
                        #advance to the next node through that letter
                        patternNode = currentNode
                        currentNode = edge[0]
                        Cont = True
                        break
                        
                    #keep traversing until all edges have been accessed.
                    
                #If the letter wasn't found in the next layer, the letter must be in a
                #deeper layer of the trie.
                if Cont == False:
                    
                    #create a new node and assign it an edge with the new letter.
                    newNode += 1
                    newEdge = (newNode , currentSymbol, False, [])
                    Trie[currentNode].append(newEdge)
                    patternNode = currentNode
                    currentNode = newNode
            else:
            
                #create a new node and assign it an edge with the new letter 
                #at the root(StartN).
                startN = currentNode
                newNode += 1
                newE = (newNode,currentSymbol, False , [])
                Trie[startN] = [newE]
                patternNode = currentNode
                currentNode = newNode
                
        
        for i in range(len(Trie[patternNode])):
            elem = Trie[patternNode][i]
            if elem[1] == pattern[-1]:
                fourthElem = []
                for tup in elem[3]:
                    fourthElem.append(tup)
                fourthElem.append(element)
                newT = (elem[0], elem[1], True, fourthElem )
                Trie[patternNode][i] = newT
    return Trie


# Step: Read Files
output = ''
if (len(sys.argv) == 4):
    output = open(sys.argv[3], "w")
else:
    output = open("output.sam", "w")



with open(fqFiles[2],"r") as file:
    
    #initialize data buffers
    line1 = ''
    line2 = ''
    line3 = ''
    line4 = ''
    
    #while there is still more data in the file
    Trie = {}
    All_info=[]
    while(line1 := file.readline()):
        
        #replacement conditional:
        
        
        #input data into buffers
        line2 = file.readline()
        line3 = file.readline()
        line4 = file.readline()
        
        #format the buffer data into different datatypes.
        header = line1.rstrip()
        sequence = line2.rstrip()
        separator = line3.rstrip()
        quality = line4.rstrip()
        my_tuple = (header, sequence,quality)
        All_info.append(my_tuple)
    Answer=TrieConstruction(All_info)
    #print(Answer)


# In[ ]:


################################################################################


# In[ ]:


# Step: Generate Trie


# In[ ]:


# Step: Generate Alignment
from pyfaidx import Fasta
fa = str(fqFiles[1])
fasta = Fasta(fa)
chromos = fasta.keys()
#print(chromos)
chromosomes = []
'''for key in chromos:
    temp = key
    if 'chr' in key:
        temp = key.replace("chr","")
    if len(temp) >= 3:
        continue
    else:
        chromosomes.append(temp)
'''
chromosomes = chromos
Aho_Trie = Answer
for chro in chromosomes:
    sequence = str(fasta[chro])
    sequence = sequence.upper()
    final_l = len(sequence)
    l = 0
    c = l
    v = 0
    while l < final_l:
        present = False
        if c >= final_l:
            l = l + 1
            c = l
            v = 0
            continue
        for elem in Aho_Trie[v]:
            if elem[1] == sequence[c]:
                v = elem[0]
                c += 1
                present = True
                if elem[2] == True:
                    for tup in elem[3]:
                        print("Found Match for:  ", tup)
                        output.write(str(tup[0]) + "\t" +str(tup[1]) + "\t" + str(tup[2]) + "\t" +  str(chro) + "\t"
                        + str(l)+"\n")
                    l = l + 1
                    c = l
                    v = 0
                break
        if present == False:
            l = l + 1
            c = l
            v = 0
        else:
            continue

output.close()
fasta.close()
# In[ ]:


# Step: Generate Values for the columns in the SAM file


# In[ ]:


# Step: Output columns to SAM file with proper formatting.


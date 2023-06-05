################################################################################
###                                  SEAG.py                                 ### 
###                                                                          ###
### This file takes in either 2 or 3 files: a reference genome FASTA file    ###
### (.fa, .fasta), and either one FASTQ file of reads or two FASTQ files in  ###
### the case of a paired-end reads.                                          ###
###                                                                          ###
### The SAMGenerator outputs a tab-separated .sam file with details          ###
### regarding all the alignments and all other details.                      ###
###                                                                          ###
### Columns and fields:                                                      ###
### 1. Query Name (type String)                                              ###
### 2. Record Flag (type int)                                                ###
### 3. Reference Name (type String)                                          ###
### 4. Position in the genome (type int)                                     ###
### 5. Mapping Quality (type int, Max 255)                                   ###
### 6. CIGAR string (type String)                                            ###
### 7. reference of next segment (type string)                               ###
### 8. position of the next segment (type string)                            ###
### 9. Observed length of template (type string)                             ###
### 10. The actual sequence (type String)                                    ###
### 11. ASCII PHRED-encoded base qualities.                                  ###
################################################################################



'''
import required packages
'''
import sys, argparse, os
from pyfaidx import Fasta



''' 
Check required arguments. If not proper arguments, exit with error message.
'''
if not (len(sys.argv) == 3 or len(sys.argv) == 4):
    print("USAGE ERROR: appropriate number of input files not present.")
    print("Usage: python3 SAMGenerator.py <genome.fa/.fasta> <reads1.fq/.fastq> (outputfile.sam)")
    sys.exit(1)

if (len(sys.argv) == 4):
    if not (sys.argv[3][-4:] == '.sam'):
        print("USAGE ERROR: output file name does not end in \'.sam\'. ")
        print("Usage: python3 SAMGenerator.py <genome.fa/.fasta> <reads1.fq/.fastq> (outputfile.sam)")
        sys.exit(1)






'''
Copy filenames into an array of filenames to be opened sequentially
'''
fqFiles = []
for i in range(len(sys.argv)):
    fqFiles.append(sys.argv[i])






'''
Check if all the files are of proper type.
'''

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






#Open a file that will serve as the output of the software
#Title the file either what the user wants or a default "output.sam"
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
    
    
    
    
    
    
    


#Open the fasta genome file
fa = str(fqFiles[1])
fasta = Fasta(fa)


#Get access to each of the chromosomes in the fasta file
#fasta.keys() returns an array of individual chromosomes.
chromosomes = fasta.keys()

#Create a MWT for string searching using .
Aho_Trie = Answer



'''This block of code's function can be summarized:
The code sequentially checks every substring of set length
in each chromosome. It then checks if the string is present
in the MWT. If it is in the MWT, that means that was a read
that was found in the genome. It marks that position in the
genome for that specific read, then goes to the next position
in the genome.

It then outputs the details to the output file.

'''
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
                        tt = l + 1
                        output.write(str(tup[0]) + "\t" +str(tup[1]) + "\t" + str(tup[2]) + "\t" +  str(chro) + "\t"
                        + str(tt)+"\n")
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



#close the output and fasta files.
output.close()
fasta.close()


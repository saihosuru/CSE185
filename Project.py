def TrieConstruction(Patterns):
    Trie = {}
    newNode = 0
    for pattern in Patterns:
        currentNode = 0
        patternNode = 0
        for i in range(len(pattern)):
            currentSymbol = pattern[i]
            if currentNode in Trie:
                Cont = False
                for edge in Trie[currentNode]:
                    if edge[1] == currentSymbol:
                        patternNode = currentNode
                        currentNode = edge[0]
                        Cont = True
                        break
                if Cont == False:
                    newNode += 1
                    newEdge = (newNode , currentSymbol, False, "")
                    Trie[currentNode].append(newEdge)
                    patternNode = currentNode
                    currentNode = newNode
            else:
                startN = currentNode
                newNode += 1
                newE = (newNode,currentSymbol, False , "")
                Trie[startN] = [newE]
                patternNode = currentNode
                currentNode = newNode
                

        for i in range(len(Trie[patternNode])):
            elem = Trie[patternNode][i]
            if elem[1] == pattern[-1]:
                newT = (elem[0], elem[1], True, pattern)
                Trie[patternNode][i] = newT

    return Trie

patterns = []
pattern_count = {}
f = "test.txt"
fast="test_example_from_Klf4.txt"
'''
with open(f,'r') as file:
    for line in file:
        temp = line.strip()
        patterns.append(temp)
'''
with open(fast,"r") as file:
    lines= file.readlines()
    for i in range(0, len(lines), 4):
            # Extract the four lines for each record
            header = lines[i].rstrip()
            sequence = lines[i+1].rstrip()
            separator = lines[i+2].rstrip()
            quality = lines[i+3].rstrip()

            # Process the data for each record as needed
            #print("Header:", header)
            print("Sequence:", sequence)
            #print("Separator:", separator)
            #print("Quality:", quality)
            patterns.append(sequence)
print(TrieConstruction(patterns))
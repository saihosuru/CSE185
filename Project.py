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

with open(f,'r') as file:
    for line in file:
        temp = line.strip()
        patterns.append(temp)












def final(start_pos,list_of_patterns,diction):
    Aho_Trie = TrieConstruction(list_of_patterns)
    l = start_pos
    c = l
    v = 0
    final_l = len(combined_lines)
    while l < final_l:
        present = False
        if c >= final_l:
            l = l + 1
            c = l
            v = 0
            continue
        for elem in Aho_Trie[v]:
            if elem[1] == combined_lines[c]:
                v = elem[0]
                c += 1
                present = True
                if elem[2] == True:
                    diction[elem[3]] += 1
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
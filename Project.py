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
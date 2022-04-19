#Classes que simulam a estrutura de um grafo no qual os vértices podem ser coloridos

class Vertex:
    def __init__(self, name) -> None:
        self.name =  name
        self.adjacentList = []
        self.label = None #Rotulo do vértice
    
    def addNeighbor(self,vertex) -> None: #Adiciona um vértice a lista de vizinhos
        if not(vertex in self.adjacentList): #Adiciona o vértice somente se ele já não estiver na lista
            self.adjacentList.append(vertex)

    def getNeighborhood(self) -> list: #Retorna a lista com a vizinhança de vértices adjacentes
        return(self.adjacentList)

    def setLabel(self,label) -> None: #Define o rótulo do vértice
        self.label = label
    
    def getLabel(self) -> int: #Retorna o rótulo do vértice
        return(self.label)
    
    
    

class Graph:
    def __init__(self) -> None:
        self.vertexlist = {} #A lista de vértices é implementado através de um dicionário
    
    def addEdge(self, nameVertex1, nameVertex2) -> None: #Adiciona uma aresta entre os vértices
        self.vertexlist[nameVertex1].addNeighbor(self.vertexlist[nameVertex2]) #Adiciona o vértice 1 a lista de vizinhos do 2
        self.vertexlist[nameVertex2].addNeighbor(self.vertexlist[nameVertex1]) #Adiciona o vértice 2 a lista de vizinhos do 1
    

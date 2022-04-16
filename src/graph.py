#Classes que simulam a estrutura de um grafo no qual os vértices podem ser coloridos

class Vertex:
    def __init__(self, name) -> None:
        self.name =  name
        self.adjacentList = []
        self.color = None
    
    def addNeighbor(self,vertex) -> None: #Adiciona um vértice a lista de vizinhos
        self.adjacentList.append(vertex)
    
    def getNeighborhood(self) -> list: #Retorna a lista com a vizinhança de vértices adjacentes
        return(self.adjacentList)

    def paint(self,color) -> None: #"Pinta" o vértice com a "cor" dada
        self.color = color
    
    def getColor(self) -> int: #Retorna a "cor" do vértice
        return(self.color)
    

class Graph:
    def __init__(self) -> None:
        self.vertexlist = {} #A lista de vértices é implementado através de um dicionário
    
    def addVextex(self,name) -> None: #Adiciona ao grafo um vértice com o nome dado
        self.vertexlist[name] = Vertex(name)
    
    def addEdge(self,nameVertex1,nameVertex2) -> None: #Adiciona uma aresta entre os vértices
        self.vertexlist[nameVertex1].addNeighbor(self.vertexlist[nameVertex2]) #Adiciona o vértice 1 a lista de vizinhos do 2
        self.vertexlist[nameVertex2].addNeighbor(self.vertexlist[nameVertex1]) #Adiciona o vértice 2 a lista de vizinhos do 1
    

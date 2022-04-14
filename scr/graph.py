#Classe que implementa a estrutura de um grafo no qual os vértices podem ser coloridos

class Vertex:
    def __init__(self, name):
        self.name =  name
        self.adjacentList = []
        self.color = None
    
    def addNeighbor(self,vertex): #Adiciona um vértice a lista de vizinhos
        self.adjacentList.append(vertex)
    
    def getNeighborhood(self): #Retorna a lista com a vizinhança de vértices adjacentes
        return(self.adjacentList)

    def paint(self,color): #"Pinta" o vértice com a "cor" dada
        self.color = color
    

class Graph:
    def __init__(self):
        self.vertexList = {} #A lista de vértices é implementado através de um dicionário
    
    def addVextex(self,name): #Adiciona ao grafo um vértice com o nome dado
        self.vertexList[name] = Vertex(name)
    
    def addEdge(self,nameVertex1,nameVertex2): #Adiciona uma aresta entre os vértices
        self.vertexList[nameVertex1].addNeighbor(self.vertexList[nameVertex2]) #Adiciona o vértice 1 a lista de vizinhos do 2
        self.vertexList[nameVertex2].addNeighbor(self.vertexList[nameVertex1]) #Adiciona o vértice 2 a lista de vizinhos do 1
    

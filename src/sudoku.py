#Implementação do jogo Sudoku através de grafos

from cProfile import label
from graph import Vertex,Graph
import random

class Cell(Vertex):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.candidates = [] #Lista de possíveis valores para prencher a célula
    
    def addCandidate(self, label) -> None:
        self.candidates.append(label)
    
    def removeCandidate(self, label) -> None:
        self.candidates.remove(label)
    
    def getCandidates(self) -> list:
        return(self.candidates)


class Sudoku(Graph): #Se comporta como um grafo
    def __init__(self) -> None:
        super().__init__()
        self.newGame() #Cria outro jogo

    def setRandomLabel(self, nColumn, nLine) -> None: #Rotula aleatóriamente uma célula especificada
        labels = [1,2,3,4,5,6,7,8,9] #Possíveis rótulos
        cell = self.vertexlist[(nColumn, nLine)]
        for neighbor in cell.getNeighborhood(): #Analisa todos as células vizinhas
            if neighbor.getLabel() in labels: 
                labels.remove(neighbor.getLabel()) #Romove da lista de rótulos o que já está presente na vizinhança
        cell.setLabel(random.choice(labels)) #Escolhe aleatóriamente um dos rótulos restantes para a célula   
        
    def assemble(self) -> None: #Função que monta o tablô 9x9 do sudoku
        for nLine in range(9): #Para cada uma das 81 células do tablô cria-se um vértice
            for nColumn in range(9): 
                self.vertexlist[(nColumn,nLine)] = Cell((nColumn,nLine)) #O nome da célula é uma tupla com suas coordenadas no tablô
        
        for lineBlock in range(3):
            for columnBlock in range(3):
                block = []
                for nLine in range(3): #Para cada uma das 81 células do tablô cria-se um vértice
                    for nColumn in range(3): 
                        block.append((nColumn+ 3*columnBlock, nLine + 3*lineBlock))
                for nCellA in range(9):
                    for nCellB in range(nCellA, 9):
                        self.addEdge(block[nCellA], block[nCellB])

        for cell in self.vertexlist: #Adiciona as arestas de cada celula a suas respectivas adjacentes
            columnIndex = cell[0]
            lineIndex = cell[1]
            for nColumn in range(columnIndex+1, 9):
                self.addEdge(cell,(nColumn,lineIndex))
            for nLine in range(lineIndex+1, 9):
                self.addEdge(cell,(columnIndex,nLine))

    def newGame(self) -> None:
        self.assemble() #Recria o tabô
        #Rotula aleatóriamente a células conjunto central 3x3
        for nLine in range(0,9): 
            for nColumn in range(0,9):
                #print(f" coluna: {nColumn}\n linha: {nLine}\n\n")
                try:
                    self.setRandomLabel(nColumn, nLine)
                except:
                    self.newGame()    
            print(self)
        ''''cell = self.vertexlist[(0,3s)]
        cell.setLabel(1)
        for neighbor in cell.getNeighborhood():
            neighbor.setLabel(1)
        print(self)'''
        #Prenche os vértices a

    def __str__(self) -> str: #Representação gráfica do Sudoku
        outStr = ""
        lineCounter = 0 #Contador do número de linhas
        for nLine in range(9):
            lineCounter+=1
            colunmCounter = 0 #Contador do número de colunas
            for nColumn in range(9):
                colunmCounter+=1
                valCell = self.vertexlist[(nColumn,nLine)].getLabel()
                if (valCell == None): #Se a célula não está colorida, representa sua cor por "X"
                    outStr+= " X"
                else:
                    outStr += f" {valCell}"

                if (colunmCounter == 3): #A cada 3 colunas 
                    outStr+= " " #Adiciona-se um espaço em branco para delimitar os blocos de 3x3
                    colunmCounter = 0
            outStr+='\n'

            if (lineCounter == 3): #A cada 3 linhas 
                outStr+= "\n" #Adiciona-se uma linha em branco para delimitar os blocos de 3x3
                lineCounter = 0

        return(outStr)

a = Sudoku()
a.newGame()
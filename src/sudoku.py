#Implementação do jogo Sudoku através de grafos

from cProfile import label
from os import kill
from graph import Vertex,Graph
import random

class Cell(Vertex):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.candidatesLabels = [1,2,3,4,5,6,7,8,9] #Lista de possíveis valores para prencher a célula
    
    def choiche(self,label): #Escolhe um rótulo para 
        self.setLabel(label)
    
    def analyzeChoice(self, label, neighborCell): #Função usada para verificar se o uso de um rótulo por uma célula vizinha gera algum conflito.
        if self.getLabel() != None: #Se a célula já está rotulada, o uso do rótulo pela célula vizinha não gera conflito
            #print("EITA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            return(True)
        if label in self.candidatesLabels : #Se o label está na lista de candidatos
            #print("EITA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            if len(self.candidatesLabels) == 1: #Se o unico candidado da célula for o rótulo a ser usado pela vizinha, tem-se um conflito
                    return(False)
            elif len(self.candidatesLabels) == 2: 
                remmants =  self.candidatesLabels.copy().remove(label) #Lista com o candidato remanescente caso o rótulo seja usado
                for cell in self.adjacentList:
                    if cell.getCandidates() == remmants: #Se lista com candidato remanecente for igual a lista de candidatos de algum vértice viznho tem-se um conflito
                        return(False)
                    elif cell in neighborCell.getCandidates() and cell.getCandidates() == self.candidatesLabels: #Se ao usar o label a célula terá como remanescente um mesmo label que o vizinho tem-se um conflito
                        return(False)
                c = 0
                for cell in neighborCell.adjacentList:
                    if (cell in self.adjacentList and sorted(cell.getCandidates()) == sorted(self.candidatesLabels)):
                        c+=1
                if c > len(self.candidatesLabels):
                    return(False)
            return(True) #Se passar por todas a verificações, então não há conflito
        else:
            #print("EITA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            return(True) #Se o label não é um dos candidatos do vértice, não existe conflito

    
    def addCandidate(self, label) -> None:
        self.candidatesLabels.append(label)
    
    def removeCandidate(self, label) -> None:
        self.candidatesLabels.remove(label)
    
    def getCandidates(self) -> list:
        return(self.candidatesLabels)


class Sudoku(Graph): #Se comporta como um grafo
    def __init__(self) -> None:
        super().__init__()
        self.newGame() #Cria outro jogo

    def setRandomLabel(self, nColumn, nLine) -> None: #Rotula aleatóriamente uma célula especificada
        cell = self.vertexlist[(nColumn, nLine)]
        label = random.choice(cell.getCandidates())
        cell.removeCandidate(label) #Remove o rótulo escolhido da lista de candidatos da célula
        '''for neighbor in cell.getNeighborhood(): #Analisa todos as células vizinhas
            if not(neighbor.analyzeChoice(label,cell)): #Se a análise de escolha sinalizar algum conflito
                #print("EITA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                label = random.choice(cell.getCandidates()) #Escolhe um novo rótulo
                cell.removeCandidate(label) '''
        cell.setLabel(label)
        for neighbor in cell.getNeighborhood():
            if label in neighbor.getCandidates():
                neighbor.removeCandidate(label) #Remove da lista de candidatos das células vizinhas o rótulo escolhido      
        
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
        '''for nLine in range(0,9): 
            for nColumn in range(0,9):
                #print(f" coluna: {nColumn}\n linha: {nLine}\n\n")
                self.setRandomLabel(nColumn, nLine)
                for cell in self.vertexlist[(nColumn, nLine)].getNeighborhood():
                    cell.choiche(1)
                    #self.setRandomLabel(cell.name[0], cell.name[1])
                print("\n#####################\n")
                print(self)
                self.assemble()'''
        for lineBlock in range(3):
            for columnBlock in range(3):
                for nLine in range(3): #Para cada uma das 81 células do tablô cria-se um vértice
                    for nColumn in range(3):
                        print("\n#####################\n")
                        print(self)
                        print(f"coluna:{nColumn + 3*columnBlock} , linha: {nLine + 3*lineBlock}\n")
                        try:
                            self.setRandomLabel(nColumn + 3*columnBlock, nLine + 3*lineBlock)
                        except:
                            0/0
        '''for nLine in range(0,9): 
            for nColumn in range(0,9):
                self.assemble()
                cell = self.vertexlist[(nColumn,nLine)]
                cell.setLabel(1)
                for neighbor in cell.getNeighborhood():
                    neighbor.setLabel(1)
                print("\n#####################\n")
                print(f"linha:{nLine} , coluna: {nColumn}\n")
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
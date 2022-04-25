#Implementação do jogo Sudoku através de grafos

from cProfile import label
from os import kill
from graph import Vertex,Graph
import random

class Cell(Vertex):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.candidatesLabels = [1,2,3,4,5,6,7,8,9] #Lista de possíveis valores para prencher a célula
    
    def choiche(self,label) -> None: #Escolhe um rótulo para 
        self.setLabel(label)

    def __lt__(self, cell) -> bool: #Usado para ordenar a lista de vértices com base no número de candidatos disponível
        if self.label == None and cell.getLabel() == None: #Se ambos não estão rotulados o menor é o que tem mesmo candidatos
            if len(self.candidatesLabels) < len(cell.getCandidates()):
                return(True)
            else: 
                return(False)
        elif cell.getLabel() == None: #Se um estiver rotulado, o menor é o que não possui rótulo
            return(False)
        else:
            return(True)
    
    '''def analyzeChoice(self, label, neighborCell): #Função usada para verificar se o uso de um rótulo por uma célula vizinha gera algum conflito.
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
            return(True) #Se o label não é um dos candidatos do vértice, não existe conflito'''

    
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

    def setRandomLabel(self,cell): #nColumn, nLine) -> None: #Rotula aleatóriamente uma célula especificada
        #cell = self.vertexlist[(nColumn, nLine)]
        label = random.choice(cell.getCandidates())
        cell.removeCandidate(label) #Remove o rótulo escolhido da lista de candidatos da célula
        for neighborCell1 in cell.getNeighborhood():
            if neighborCell1.getCandidates() == [label] and neighborCell1.getLabel() == None : #Se o rótulo escolhido for o único candidato de algum vizinho em branco
                label = random.choice(cell.getCandidates())  #Escolhe um novo rótulo
                cell.removeCandidate(label) 
            elif label in neighborCell1.getCandidates():
                candidatos = neighborCell1.getCandidates()
                clique1 = [neighborCell1]
                clique2 = [neighborCell1]
                for neighborCell2 in cell.adjacentList:
                    if (neighborCell2.getLabel() == None and neighborCell2 != neighborCell1 ):
                        if (candidatos == neighborCell2.getCandidates() and neighborCell2.isNeighbor(clique1[-1])):
                            clique1.append(neighborCell2)
                        if (candidatos == neighborCell2.getCandidates() and neighborCell2.isNeighbor(clique2[-1])):
                            clique2.append(neighborCell2)
                numRemainingLabels = len(neighborCell1.getCandidates())
                if (numRemainingLabels < len(clique1) or numRemainingLabels < len(clique2)):
                    print(f"Grupo 1: Células restantes: {len(clique1)} Rótulos Restantes: {numRemainingLabels} Vértice: {neighborCell1.name} ")
                    print(f"Grupo 2: Células restantes: {len(clique2)} Rótulos Restantes: {numRemainingLabels} Vértice: {neighborCell1.name} ")
                    if ( len(cell.getCandidates() > 0)): #Se houver mais candidatos
                        label = random.choice(cell.getCandidates())  #Escolhe um novo rótulo
                        cell.removeCandidate(label)
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

    def newGame(self) -> None: #Gera um novo jogo de sudoku
        self.assemble() #Recria o tabô
        #Rotula aleatóriamente a células conjunto central 3x3
        nRemaningCells = 81 #Numero de células restantes a serem rotuladas
        cells = list(self.vertexlist.values()) #Salva as células que estão no dicionário em uma lista
        while (nRemaningCells > 0):
            cells.sort() #Ordena a lista de células
            cell = cells[0]
            try:
                self.setRandomLabel(cell) #Rotula a célula em branco com menos candidatos
            except:
                #nRemaningCells = 81
                cell.setLabel("@")
                print(self)
                print("EITAAAAAAAAAAAAAAAAAAAAAAAAA")
                break
            nRemaningCells -=1 #Decrementa o contador de células restantes
        print(self)
        print("\n#####################\n")
        print(f"linha:{cell.name[1]} , coluna: {cell.name[0]}\n")
            #input()

    

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
print(a.vertexlist[(2,1)].isNeighbor(a.vertexlist[(2,1)]))
a.newGame()
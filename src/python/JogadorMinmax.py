
# Jogador
# Created on 11 de Junho de 2021

from Jogador import Jogador
from Jogada import Jogada
from Tabuleiro import Tabuleiro 
import TabuleiroGomoku 
import time
import threading
PROFUNDIDADE = 1 
# Esta Classe implementa o esqueleto de um jogador guloso.
#
# Ele se conecta no servidor do jogo  no host passado pela linha de argumentos e
# na porta fornecida pela classe Servidor.
# Passa ent&atilde;o a receber as jogadas do oponente e enviar jogadas por meio do servidor
# segundo um protocolo pr&eacute;-definido.
#
# Execucao
# java Jogador <nome> <host>
# Exemplo:
# java Jogador equipe1 localhost
# <b>Protocolo</b>
# A cada rodada o jogador recebe uma jogada e envia uma jogada.
# A jogada recebida possui o seguinte formato:
# <jogador>\n<x>\n<y>\n<xp>\n<yp>\n
# Onde:
#
# <jogador>= indica qual &eacute; a cor do jogador (Tabuleiro.AZUL ou Tabuleiro.VERM) ou
# '#' indicando fim do jogo.
# <x><y> = sao as coordenadas da posicao recem ocupada (0 a 7).
# <xp><yp> = sao as coordenadas da pe&ccedil;a responsavel pela jogada (0 a 7).
#
# A jogada enviada possui o seguinte formato:
# <x>\n<y>\n<xp>\n<yp>\n
# Se o jogador precisar passar a jogada deve atribuir valor -1 as coordenadas.
#
# Caso o jogador tenha algum problema ou desista deve enviar o caracter #
#
# @author Alcione
# @version 1.0
class Node: 
    def __init__(self,value, TabGoMoku, Jogador,Parent = None): 
        self.value = value  
        self.terminalFlag = False  # True or False    
        self.TabGoMoku = TabGoMoku   
        self.Parent = Parent  
        self.SelectChild = False # True se esse nó for a raiz da próxima árvore
        self.Jogador = Jogador
    
    
    
    # calcula a função de utilidade
    def Utility_Function(self,jogada): 
        pass 
    
    # simula o tabuleiro com a jogada  
    # faz o move    
    def PlaySim(self,jogada): 
       pass 
    

    def expand(self,parent):  
        
        # verificar todas possibilidades de jogada 
        # Para cada possibilidade criar um novo nó
        for i in self.TabGoMoku.obtemJogadasPossiveis(parent.Jogador):  
            child = self.Gen_child(Parent,i)
        pass 

    def Gen_child(self,Parent, value, jogada): 
        # tabuleiro
        getTab = PlaySim(self,jogada)   

        value = Utility_Function(self,jogada)
        child = Node(self,value,getTab,Parent)
        return child 



class JogadorMinMax(Jogador):

    def __init__(self, nome):
        Jogador.__init__(self, nome)
        self.MAXNIVEL = 10
        self.TEMPOMAXIMO = 1.0
        self.jogada = Jogada(-1, -1, -1, -1) 




     # Calcula uma nova jogada para o tabuleiro e jogador corrente.
     # Aqui deve ser colocado o algoritmo com as t&eacute;cnicas de inteligencia
     # artificial. No momento as jogadas s&atilde;o calculadas apenas por crit&eacute;rio de
     # validade. Coloque aqui seu algoritmo minmax.
     # @param tab Tabuleiro corrente
     # @param jogadorCor Jogador corrente
     # @return retorna a jogada calculada.


    def calculaJogada(self, tab, jogadorCor):
        tempo1 = time.time()
        usado = 0.0
        for prof in range(1, self.MAXNIVEL):
            tempo2 = time.time()
            t1 = threading.Thread(
                target=self.max, args=(tab, jogadorCor, prof,))
            t1.start()
            t1.join(self.TEMPOMAXIMO - usado)
            usado = tempo2 - tempo1
            print("tempo usado:", usado)
            if usado >= self.TEMPOMAXIMO:
                break

        return self.jogada

    def max(self, tab, jogador, prof):
        
        self.jogada = tab.obtemJogadaHeuristica(jogador)

    def min(self, tab, jogador, prof): 

if __name__ == "__main__":
    import sys
    JogadorMinMax(sys.argv[1]).joga()
    print("Fim")





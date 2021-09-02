# Jogador
# Created on 11 de Junho de 2021

from __future__ import annotations

from typing import List
 
from Jogador import Jogador
from Jogada import Jogada
from Tabuleiro import Tabuleiro
import time
import threading
from TabuleiroGoMoku import TabuleiroGoMoku 
import numpy as np 



class JogadorMinMax(Jogador):

    def __init__(self, nome):
        Jogador.__init__(self, nome)
        self.MAXNIVEL = 10
        self.TEMPOMAXIMO = 1.0
        self.jogada = Jogada(-1, -1, -1, -1)

        # Calcula uma nova jogada para o tabuleiroe jogador corrente.

    # Aqui deve ser colocado o algoritmo com as t&eacute;cnicas de inteligencia
    # artificial. No momento as jogadas s&atilde;o calculadas apenas por crit&eacute;rio de
    # validade. Coloque aqui seu algoritmo minmax.
    # @param tab Tabuleiro corrente
    # @param jogadorCor Jogador corrente
    # @return retorna a jogada calculada.

    def calculaJogada(self, tab, jogadorCor):
        tempo1 = time.time()
        usado = 0.0 
        #tab.imprimeTab(tab.getTab()) 
        self.jogada = Jogada(-1, -1, -1, -1)
        for prof in range(1, self.MAXNIVEL):
            t1 = threading.Thread(
                target=self.setup, args=(tab, jogadorCor,prof,))
            t1.start()
            t1.join(self.TEMPOMAXIMO - usado)
            tempo2 = time.time()
            usado = tempo2 - tempo1
            print("tempo usado:", usado) 
            print("Profundidade:",prof)   
            print("linha: {} coluna:{}".format(self.jogada.getLinha(), self.jogada.getColuna()))

            if usado >= self.TEMPOMAXIMO:
                break

        return self.jogada 
    
    def funcao_utilidade(self,jogador,tab):  
        oponente = (jogador + 1) % 2 

        value_jogador =  tab.heuristicaBasica(jogador,tab.getTab()) 
        #value_oponente = tab.heuristicaBasica(oponente,tab.getTab()) 
        return value_jogador #- value_oponente
    
    
    # realiza o movimento da jogada selecionada no tabuleiro 
    def play(self,tab, jogada, jogador): 
        child_tab = TabuleiroGoMoku()
        
        child_tab.copiaTab(tab.getTab()) 
        child_tab.move(jogador, jogada)  
        
        return child_tab  
    # inicia a arvore para o algoritmo minmax
    def setup(self,tab,jogador,prof):   
        print("---------FUCK")
        depth = 1  
        Best_Score = -np.inf  
        Beta = np.inf 

        for jogada in tab.obtemJogadasPossiveis(jogador): 
                Genchild = self.play(tab,jogada,jogador) 
                value = self.minDec(Genchild,jogador,depth,prof,Best_Score,Beta)  
                if value > Best_Score: 
                    self.jogada = jogada 
                    Best_Score = value  
        print("**Best Score: ",Best_Score) 
    # funcão de decisao
    def maxDec(self, tab, jogador, depth, MaxDepth, alpha,beta): 
    
        if(depth == MaxDepth): 
            return self.funcao_utilidade(jogador,tab)
        max_value = -np.inf  

        for i in tab.obtemJogadasPossiveis(jogador): 
        
            child_tab = self.play(tab, i,jogador) 
            max_value = max(max_value,self.minDec(child_tab,jogador,depth+1,MaxDepth,alpha,beta))  
            if max_value >= beta:
                return max_value 
            alpha = max(alpha, max_value)
        return max_value

    def minDec(self, tab, jogador, depth,MaxDepth,alpha,beta):
        
        if(depth == MaxDepth): 
            return self.funcao_utilidade(jogador,tab) 

        min_value = np.inf
        oponente = (jogador + 1) % 2
        for i in tab.obtemJogadasPossiveis(oponente): 
        
            child_tab = self.play(tab,i,oponente) 
            min_value = min(min_value, self.maxDec(child_tab,jogador,depth+1,MaxDepth,alpha,beta))  
            if min_value <= alpha:
                return min_value 
            
            beta = min(beta, min_value)
        return min_value


if __name__ == "__main__":
    import sys

    JogadorMinMax(sys.argv[1]).joga()
    print("Fim")

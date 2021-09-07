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


def play(tab, jogada, jogador):
    """
    Realiza um movimento em uma copia do tabuleiro passado
    :rtype: TabuleiroGoMoku
    """
    child_tab = TabuleiroGoMoku()
    child_tab.copiaTab(tab.getTab())
    child_tab.move(jogador, jogada)
    return child_tab


class JogadorMinMax(Jogador):
    MAXNIVEL = 10
    TEMPOMAXIMO = 1.0

    def __init__(self, nome):
        Jogador.__init__(self, nome)
        self.jogada = Jogada(-1, -1, -1, -1)

        # Calcula uma nova jogada para o tabuleiroe jogador corrente.

    def calculaJogada(self, tab, jogadorCor):
        tempo1 = time.time()
        usado = 0.0
        self.jogada = Jogada(-1, -1, -1, -1)

        for prof in range(1, self.MAXNIVEL):
            t1 = threading.Thread(
                target=self.setup, args=(tab, jogadorCor, prof))
            t1.start()
            t1.join(self.TEMPOMAXIMO - usado)
            tempo2 = time.time()
            usado = tempo2 - tempo1
            print(f"Profundidade: {prof} Tempo usado: {round(usado, 3)} Jogada: {self.jogada.getLinha()}-{self.jogada.getColuna()}")
            if usado >= self.TEMPOMAXIMO:
                break

        return self.jogada

    # @staticmethod
    def funcaoUtilidade(self, jogador, tab):
        value_jogador = self.heuristicaBasica(jogador, tab.getTab(), tab)
        return value_jogador

    def setup(self, tab: TabuleiroGoMoku, jogador: int, prof: int):
        """
        Inicia a arvore para o algoritmo minmax

        :param tab:
        :param jogador:
        :param prof: Profundidade maxima do busca em profundidade interativa
        """
        depth = 1
        best_score = -np.inf
        beta = np.inf

        for jogada in tab.obtemJogadasPossiveis(jogador):
            genchild = play(tab, jogada, jogador)
            value = self.minDec(genchild, jogador, depth, prof, best_score, beta)
            if value > best_score:
                self.jogada = jogada
                best_score = value

    def maxDec(self, tab: TabuleiroGoMoku, jogador: int, depth: int, max_depth: int, alpha: float, beta: float) -> int:
        if depth == max_depth:
            return self.funcaoUtilidade(jogador, tab)

        max_value = -np.inf
        for i in tab.obtemJogadasPossiveis(jogador):
            child_tab = play(tab, i, jogador)
            max_value = max(max_value, self.minDec(child_tab, jogador, depth + 1, max_depth, alpha, beta))

            if max_value >= beta:
                return max_value
            alpha = max(alpha, max_value)

        return max_value

    def minDec(self, tab: TabuleiroGoMoku, jogador: int, depth: int, max_depth: int, alpha: float, beta: float) -> int:
        if depth == max_depth:
            return self.funcaoUtilidade(jogador, tab)

        min_value = np.inf
        oponente = (jogador + 1) % 2
        for i in tab.obtemJogadasPossiveis(oponente):
            child_tab = play(tab, i, oponente)
            min_value = min(min_value, self.maxDec(child_tab, jogador, depth + 1, max_depth, alpha, beta))

            if min_value <= alpha:
                return min_value
            beta = min(beta, min_value)

        return min_value
    
    # Copiamos a função de TabuleiroGoMoku.py para aumentar o ponto negativo do oponente
    # Retorna um valor heuristico para o tabuleiro dado um jogador
    # param jogador numero do jogador
    # param tab tabuleiro
    # retorna valor do tabuleiro
    def heuristicaBasica(self, jogador, tab, objTab):
        valor = 0
        for linha in range(0, objTab.DIM):
            for coluna in range(0, objTab.DIM):
                if tab[linha][coluna] == jogador:
                    temp = self.contaHeuristica(
                        jogador, linha, coluna, 1, 0, tab, objTab)
                    if temp == 100:
                        return 10000
                    valor += temp
                    temp = self.contaHeuristica(
                        jogador, linha, coluna, 0, 1, tab, objTab)
                    if temp == 100:
                        return 10000
                    valor += temp
                    temp = self.contaHeuristica(
                        jogador, linha, coluna, 1, -1, tab, objTab)
                    if temp == 100:
                        return 10000
                    valor += temp
                    temp = self.contaHeuristica(
                        jogador, linha, coluna, 1, 1, tab, objTab)
                    if temp == 100:
                        return 10000
                    valor += temp
                elif tab[linha][coluna] != objTab.LIVRE:
                    valor -= 4 * self.contaHeuristica(objTab.oponente(
                        jogador), linha, coluna, 1, 0, tab, objTab)
                    valor -= 4 * self.contaHeuristica(objTab.oponente(
                        jogador), linha, coluna, 0, 1, tab, objTab)
                    valor -= 4 * self.contaHeuristica(objTab.oponente(
                        jogador), linha, coluna, 1, -1, tab, objTab)
                    valor -= 4 * self.contaHeuristica(objTab.oponente(
                        jogador), linha, coluna, 1, 1, tab, objTab)
        return valor

    # Copiamos a função de TabuleiroGoMoku.py para ampliarmos as possibilidades
    # Conta o numero de pecas de um jogador a partir da posicao passada e na
    # direcao especificada levando em consideracao a vantagem. Os valores da
    # direcao definida por dirX e dirY devem ser 0, 1, or -1, sendo que um
    # deles deve ser diferente de zero.
    def contaHeuristica(self, jogador, linha, coluna, dirX, dirY, tab, objTab):
        boqueadoPonta1 = boqueadoPonta2 = False
        lin = linha + dirX  # define a direcao .
        col = coluna + dirY
        while (not objTab.saiuTabuleiro(lin, col) and tab[lin][col] == jogador):
            # Quadrado esta no tabuleiro e contem uma peca do jogador.
            lin += dirX  # Va para o proximo.
            col += dirY

        # verifica se fechou a ponta
        if (objTab.saiuTabuleiro(lin, col) or tab[lin][col] != objTab.LIVRE):
            boqueadoPonta1 = True

        # self.win_r1 = lin - dirX  # Quadrado anterior.
        # Quadrado nao esta no tabuleiro ou contem uma peca do jogador.
        # self.win_c1 = col - dirY

        lin = lin - dirX  # Olhe na direcao oposta.
        col = col - dirY

        ct = 0  # Numero de pecas em linha de um jogador.
        while (not objTab.saiuTabuleiro(lin, col) and tab[lin][col] == jogador):
            # Quadrado esta no tabuleiro e contem uma peca do jogador.
            ct += 1
            lin -= dirX   # Va para o proximo.
            col -= dirY

         # verifica se fechou a ponta
        if (objTab.saiuTabuleiro(lin, col) or tab[lin][col] != objTab.LIVRE):
            boqueadoPonta2 = True

        # self.win_r2 = lin + dirX
        # self.win_c2 = col + dirY

        # Neste ponto, (win_r1,win_c1) e (win_r2,win_c2) marcam as extremidades
        # da linha que pertence ao jogador.

        # Verifica se esta bloqueado e nao pode fechar essa linha
        if (ct < 5 and boqueadoPonta1 and boqueadoPonta2):
            ct = 0
        elif ct == 5 or (ct == 4 and not boqueadoPonta1 and not boqueadoPonta2):
            ct = 100
        elif (ct == 4 and boqueadoPonta1 and not boqueadoPonta2) or (ct == 4 and not boqueadoPonta1 and boqueadoPonta2):
            ct = 90 
        elif ct == 3 and not boqueadoPonta1 and not boqueadoPonta2: 
            ct = 75 
        elif (ct == 3 and boqueadoPonta1 and not boqueadoPonta2) or (ct == 3 and not boqueadoPonta1 and boqueadoPonta2):
            ct = 50 
        elif ct == 2 and not boqueadoPonta1 and not boqueadoPonta2: 
            ct = 25 
        elif (ct == 2 and boqueadoPonta1 and not boqueadoPonta2) or (ct == 2 and not boqueadoPonta1 and boqueadoPonta2):
            ct = 15  
        elif ct == 1 and not boqueadoPonta1 and not boqueadoPonta2: 
            ct = 10 
        elif (ct == 1 and boqueadoPonta1 and not boqueadoPonta2) or (ct == 1 and not boqueadoPonta1 and boqueadoPonta2):
            ct = 5
        return ct


if __name__ == "__main__":
    import sys

    JogadorMinMax(sys.argv[1]).joga()
    print("Fim")

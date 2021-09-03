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

    @staticmethod
    def funcaoUtilidade(jogador, tab):
        value_jogador = tab.heuristicaBasica(jogador, tab.getTab())
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


if __name__ == "__main__":
    import sys

    JogadorMinMax(sys.argv[1]).joga()
    print("Fim")

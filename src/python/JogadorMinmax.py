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

PROFUNDIDADE = 1


class Heuristica:

    @staticmethod
    def calcula(tab) -> int:
        pass


class Node:
    def __init__(self, jogador, value, tab, parent, depth):
        self.value: int = value
        self.tabGoMoku: TabuleiroGoMoku = tab
        self.jogador: int = jogador  # Tabuleiro.AZUL = 0 Tabuleiro.VERM = 1
        self.parent: Node = parent
        self.children: List[Node] = None
        self.depth: int = depth

    def expand(self) -> List[Node]:
        self.children = [self.gen_child(i) for i in self.tabGoMoku.obtemJogadasPossiveis(self.jogador)]
        return self.children

    def expand_until(self, max_depth):
        for i in self.tabGoMoku.obtemJogadasPossiveis(self.jogador):
            if self.depth <= max_depth:
                self.gen_child(i).expand_until(max_depth)
            else:
                break

    def gen_child(self, jogada: Jogada):
        child_tab = TabuleiroGoMoku()
        child_tab.copiaTab(self.tabGoMoku.tab)
        child_tab.move(self.jogador, jogada)

        value = Heuristica.calcula(child_tab)

        child = Node(self.jogador, value, child_tab, self, self.depth + 1)
        return child

    @staticmethod
    def print_top_down(node: Node):
        if node.children is not None:
            for i in node.children:
                Node.print_top_down(i)
                print(i)

    def __str__(self):
        return f"Depth: {self.depth}, Heuristic:{self.value}"


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
        pass


if __name__ == "__main__":
    import sys

    JogadorMinMax(sys.argv[1]).joga()
    print("Fim")

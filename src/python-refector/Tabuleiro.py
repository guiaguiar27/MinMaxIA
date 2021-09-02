import abc
from typing import List
from numpy import ndarray
from Jogada import Jogada

'''
 Tabuleiro
 
 Esta é a interface do tabuleiro
 NÃO ALTERE ESSA CLASSE.
 Se precisar alterála faça outra classe.
 
 @author Vitor
 @version 1.1
'''


class Tabuleiro(metaclass=abc.ABCMeta):
    """
    Classe Abstrata para o tabuleiroGomuku
    """
    AZUL = 0
    LIVRE = -1
    VERM = 1
    EMPATE = -2
    cor = ["Azul", "Vermelho"]

    @abc.abstractmethod
    def copiaTab(self, a_tab: ndarray):
        """"
            Copia as posicoes de um array para o array atual do tabuleiro
            :param a_tab: ndarray
                Array contendo os valores para a cópia.
            :return: void
        """
        pass

    @abc.abstractmethod
    def fimJogo(self) -> bool:
        """
        Verifica se o jogo terminou.

        :return: bool
            False = nao terminou;
            True = se terminou
        """
        pass

    @abc.abstractmethod
    def vencedorCor(self) -> int:
        """
        Verifica qual cor é o vencedora.

        :return:
            0 = nao terminou;
            AZUL = venceu o jogador 1;
            VERM = venceu o jogador 2;
        """
        pass

    @abc.abstractmethod
    def vencedorNum(self) -> int:
        """
        Verifica quem é o vencedor.

        :return:
            0 = nao terminou;
            1 = venceu o jogador 1;
            2 = venceu o jogador 2;
            -1 = empate;
        """
        pass

    @abc.abstractmethod
    def move(self, jogador: int, j: Jogada) -> bool:
        """
         Executa um movimento no tabuleiro.

        :param jogador: int
            número do jogador a ser avaliado
        :param j: Jogada
            jogada que será realizada
        :return: bool
            True = o movimento é válido.
            False = o movimento é válido.
        """
        pass

    @abc.abstractmethod
    def numPecas(self, ai_jogador: int) -> int:
        """
         Retorna o número de peças de um jogador.

        :param ai_jogador: int
            número do jogador a ser avaliado
        :return:
            número de peças
        """
        pass

    @abc.abstractmethod
    def obtemJogadaBoa(self, ai_jogador: int) -> Jogada:
        """
         Retorna a melhor jogada para um determinado jogador

        :param ai_jogador: int
            número do jogador a ser avaliado
        :return: Jogada
            melhor jogada
        """
        pass

    @abc.abstractmethod
    def obtemJogadaHeuristica(self, jogador: int) -> Jogada:
        """
         Retorna a melhor jogada dado um jogador utilizando a função heuristicaBasica

        :param jogador: int
            número do jogador a ser avaliado
        :return:
            melhor jogada
        """

        pass

    @abc.abstractmethod
    def obtemJogadasPossiveis(self, ai_jogador: int) -> List[Jogada]:
        """
         Retorna um vetor contendo as jogadas possiveis de um jogador

        :param ai_jogador: int
        :return: List[Jogada]
            jogadas possiveis
        """
        pass

    @abc.abstractmethod
    def getTab(self) -> ndarray:
        """
         Retorna uma cópia do tabuleiro na forma de ndarray.

        :return: ndarray
            Array com os valores
        """
        pass

    @abc.abstractmethod
    def __str__(self):
        """
         Retorna o tabuleiro na forma de String
        """
        pass

    @abc.abstractmethod
    def verifica(self, ai_jogador: int, jogada: Jogada) -> int:
        """
        Verifica se um movimento é válido.

        :param ai_jogador: int
        :param jogada: Jogada
        :return:
            0 = o movimento é inválido;
            >0 = movimento é válido
        """
        pass

    @abc.abstractmethod
    def iniciaLimpo(self):
        """
         Inicia o tabuleiro com a configuração padrão
        """
        pass

    @abc.abstractmethod
    def inicia(self, tab: ndarray):
        """
         Inicia o tabuleiro com a configuração passada na forma de ndarray

        :param tab: ndarray
            Tabela com a configuração inicial
        """
        return

    @abc.abstractmethod
    def oponente(self, jogador: int) -> int:
        """
        Retorna o oponente do jogador recebido

        :param jogador: int
        :return:
            Retorna o oponente do jogador recebido
        """
        pass

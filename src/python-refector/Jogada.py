"""
Esta Classe implementa as coordenadas de uma jogada.
@author:Alcione de Paiva
"""


class Jogada:
    """
    Cria uma objeto jogada com as coordenadas. Se a origem for negativa entao
    a jogada é considerada como a colocação de uma peça nova.
    linhaInicial linha original da peça
    colunaInicial coluna original da peça
    linha linha da jogada
    coluna coluna da jogada
    """

    def __init__(self, linha_inicial: int, coluna_inicial, lin: int, col: int):
        """
        :type col: int
        :type lin: int
        :type coluna_inicial: int
        :type linha_inicial: int
        """
        self.linhaInicial = linha_inicial
        self.linha = lin
        self.colunaInicial = coluna_inicial
        self.coluna = col

    def JogadaNova(self, linha: int, coluna: int):
        """
        Cria uma objeto jogada com as coordenadas

        :type linha: int
        :param linha: linha da jogada

        :type coluna: int
        :param coluna: coluna da jogada
        """
        self.linha = linha
        self.coluna = coluna
        self.linhaInicial = -1
        self.colunaInicial = -1

    def setJogada(self, linha_inicial: int, coluna_inicial: int, linha: int, coluna: int):
        """
        Define as coordenadas do objeto.
      
        :param linha_inicial: linha original da peça 
        :param coluna_inicial: coluna original da peça 
        :param linha: linha da jogada 
        :param coluna: coluna da jogada 
        """
        self.linhaInicial = linha_inicial
        self.linha = linha
        self.colunaInicial = coluna_inicial
        self.coluna = coluna

    def getLinha(self) -> int:
        """
            Retorna a coordenada X de destino.
        """
        return self.linha

    def getColuna(self) -> int:
        """
            Retorna a coordenada Y de destino.
        """
        return self.coluna

    def getLinhaInicial(self) -> int:
        """
            Retorna a coordenada X de origem.
        """
        return self.linhaInicial

    def getColunaInicial(self) -> int:
        """
            Retorna a coordenada Y de origem.
        """
        return self.colunaInicial

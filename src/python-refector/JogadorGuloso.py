from Jogador import Jogador
from Jogada import Jogada
from Tabuleiro import Tabuleiro

"""
Jogador
Created on 11 de Junho de 2021

Esta Classe implementa o esqueleto de um jogador guloso.

Ele se conecta no servidor do jogo  no host passado pela linha de argumentos e
na porta fornecida pela classe Servidor.

Passa entao a receber as jogadas do oponente e enviar jogadas por meio do servidor
segundo um protocolo pr&eacute;-definido.

Execucao
java Jogador <nome> <host>
Exemplo:
java Jogador equipe1 localhost
<b>Protocolo</b>
A cada rodada o jogador recebe uma jogada e envia uma jogada.
A jogada recebida possui o seguinte formato:
<jogador>\n<x>\n<y>\n<xp>\n<yp>\n
Onde:

<jogador>= indica qual &eacute; a cor do jogador (Tabuleiro.AZUL ou Tabuleiro.VERM) ou
'#' indicando fim do jogo.
<x><y> = sao as coordenadas da posicao recem ocupada (0 a 7).
<xp><yp> = sao as coordenadas da pe&ccedil;a responsavel pela jogada (0 a 7).

A jogada enviada possui o seguinte formato:
<x>\n<y>\n<xp>\n<yp>\n
Se o jogador precisar passar a jogada deve atribuir valor -1 as coordenadas.

Caso o jogador tenha algum problema ou desista deve enviar o caracter #

@author Alcione
@version 1.0
"""


class JogadorGuloso(Jogador):
    """
    Calcula uma nova jogada para o tabuleiro e jogador corrente.

    Aqui deve ser colocado o algoritmo com as tecnicas de inteligencia artificial.
    No momento as jogadas sao calculadas apenas por criterio de validade.
    Coloque aqui seu algoritmo minmax.
    """

    def calculaJogada(self, tab, jogador_cor):
        """
        :param tab: Tabuleiro corrente
        :param jogador_cor: Jogador corrente
        :return: retorna a jogada calculada.
        """
        return tab.obtemJogadaHeuristica(jogador_cor)

    def __init__(self, nome):
        Jogador.__init__(self, nome)


if __name__ == "__main__":
    import sys

    JogadorGuloso(sys.argv[1]).joga()
    print("Fim")

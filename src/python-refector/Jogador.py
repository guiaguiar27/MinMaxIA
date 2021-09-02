from abc import ABC, abstractmethod

from numpy import ndarray

from Jogada import Jogada
from Configuracao import Configuracao
from Tabuleiro import Tabuleiro
from TabuleiroGoMoku import TabuleiroGoMoku
import traceback
import random
import socket

"""
    Jogador
    Created on 19 de Marco de 2001, 08:28
    
    Esta Classe implementa o esqueleto de um jogador para jogar um jogo de tabuleiro distribu&iacute;do.
    Trata-se de uma classe abstrata e, portanto, e preciso criar uma subclasse e implementar o metodo
    
    <b>calculaJogada</b> para que possa ser instanciada.
    
    Ele se conecta no servidor do jogo  no host passado pela linha de argumentos e
    na porta fornecida pela pelo singleton <b>Configuracao</b>.
    
    Passa entao a receber as jogadas do oponente e enviar jogadas por meio do servidor
    segundo um protocolo pre-definido. 
    
    <b>Execucao</b>
    <center><i>java Jogador <nome> <host></i></center> 
    
    <b>Exemplo:</b> 
    <center><i>java Jogador equipe1 localhost</i></center> 
    
    <b>Protocolo</b>
    A cada rodada o jogador recebe uma jogada e envia uma jogada. 
    A jogada recebida possui o seguinte formato:
    <center><i><jogador>\n<linha>\n<coluna>\n<linhaInicial>\n<colunaInicial>\n</i></center> 
    
    Onde:
    <ul>
    <li><jogador>= indica qual e a cor do jogador (Tabuleiro.AZUL ou Tabuleiro.VERM) ou
    '#' indicando fim do jogo.
    <li> <linha><coluna> = sao as coordenadas da posicao recem ocupada.
    <li> <linhaInicial><colunaInicial> = sao as coordenadas da peca respons&aacute;vel pela jogada .
    </ul> <p>
    
    A jogada enviada possui o seguinte formato:
    <center><i><linha>\n<coluna>\n<linhaInicial>\n<colunaInicial>\n</i></center> 
    
    Se o jogador precisar passar a jogada deve atribuir valor -1 as coordenadas.
    
    Caso o jogador tenha algum problema ou desista deve enviar o caracter #
    
    
    
    
    author Alcione
    version 1.0
"""


class Jogador(ABC):
    def __init__(self, nome):
        """
        :param args[0]: nome do jogador
        :param args[1]: endereco ip ou nome da maquina onde esta o servidor
        """
        self.conf = Configuracao()
        self.host = self.conf.getHost()
        self.nome = nome
        self.tabuleiro = TabuleiroGoMoku()
        self.tempoEspera = 1000
        self.jogador = 0

        self.tabuleiro.iniciaLimpo()

        if nome == "":
            self.nome = "jogador" + str(random.randint(0, 1000))

    def joga(self):
        """
        Metodo que inicia o jogo.
        """

        cli_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Iniciando...." + self.nome)
        try:
            cli_soc.connect((self.host, self.conf.getPorta()))

            print("enviando...." + self.nome)
            # cinput.readLine()
            cli_soc.sendall(bytes(self.nome + "\n", 'ascii'))
            linha_lida = cli_soc.recv(1024).decode('utf-8').split('\n')
            print("Linha lida:" + " - ".join(linha_lida))

            jogador_lido = int(linha_lida[0])
            linha = int(linha_lida[1])
            coluna = int(linha_lida[2])

            oponente = self.tabuleiro.VERM if jogador_lido == self.tabuleiro.AZUL else self.tabuleiro.VERM
            n_jogador = self.tabuleiro.cor[jogador_lido]
            n_oponente = self.tabuleiro.cor[(jogador_lido + 1) % 2]
            while True:
                if linha != -1:
                    sb = "Oponente: {} jogada({},{})".format(
                        self.tabuleiro.cor[oponente], linha, coluna)
                    print(sb)
                    jtemp = Jogada(-1, -1, linha, coluna)
                    if not self.tabuleiro.move(oponente, jtemp):
                        print("Jogada Invalida!!")

                print("Vou calcular jogada!")
                jog = self.calculaJogada(self.tabuleiro, jogador_lido)

                if jog is None:
                    print("Jogada Nula!")
                else:
                    print("Jogada Boa!")
                if jog is not None:
                    sb = "\nEu: {} jogada({},{})".format(
                        n_jogador, jog.getLinha(), jog.getColuna())
                    print(sb)
                    self.tabuleiro.move(jogador_lido, jog)

                    sb = "{}\n{}\n".format(jog.getLinha(), jog.getColuna())
                    cli_soc.sendall(bytes(sb, 'ascii'))
                    print(f"enviando: {jog.getLinha()} - {jog.getColuna()}\n")
                else:
                    cli_soc.sendall(bytes("-1\n-1\n", 'ascii'))
                linha_lida = cli_soc.recv(1024).decode('utf-8').split('\n')
                if linha_lida[0] == '#':
                    print("recebido #")
                    return
                linha = int(linha_lida[1])
                coluna = int(linha_lida[2])
        except Exception as e:
            print(e)
            traceback.print_exc()

            try:
                cli_soc.sendall(b'#\n')
            except Exception as e:
                print("Ocorreu um erro" + str(e))

        finally:
            print("Fim")
            cli_soc.close()

    def getTempoEspera(self) -> int:
        return self.tempoEspera

    @abstractmethod
    def calculaJogada(self, tab: TabuleiroGoMoku, jogador_cor: int) -> Jogada:
        pass

    def setTempoEspera(self, tempo_espera: int):
        self.tempoEspera = tempo_espera

    def oponente(self) -> int:
        """
        :return: Retorna o oponente.
        """
        if self.jogador == Tabuleiro.AZUL:
            return Tabuleiro.VERM
        return Tabuleiro.AZUL

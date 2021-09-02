from typing import List

from numpy import ndarray
from Configuracao import Configuracao
from Jogada import Jogada
from Tabuleiro import Tabuleiro
import numpy as np

'''
    Gomoku é um jogo japonês antigo, conhecido também como RanJu. 
    O objetivo do jogo é conseguir colocar 5 bolinhas na diagonal, na horizontal ou  na vertical. 
    Vence quem atingir este objetivo primeiro. <p><img SRC="file:gomoku.gif" height=179 width=178> 
      
    Esta Classe implementa o servidor GoMokuServer. 
    Não ALTERE ESSA CLASSE.
    Ela se registra na porta porta 1962. 
    Passa entao a receber as jogadas dos jogadores e enviá-las para o oponente segundo um protocolo pré-definido. 
    
    *Execucao
    GoMokuServer Protocolo:
        A cada rodada o servidor recebe uma jogada e envia para o oponente. 
        A jogada recebida possui o seguinte formato:
            <x> <y>
        Caso o servidor receba o caracter '#' de um jogador significa que ocorreu algum problema e o jogador está.
        
        A jogada enviada possui o seguinte format
            
            <jogador>
            <x> <y>
        Onde: 
            <jogador> = indica qual é a cor do jogador (Tabuleiro.self.AZUL ou Tabuleiro.self.VERM) ou '#' indicando fim do jogo. 
            <x><y> = sao as coordenadas da jogada (0 a 7). 
    @author Alcione 
    @version 2.0
'''


class TabuleiroGoMoku(Tabuleiro):

    def __init__(self):
        self.DIM = Configuracao().getDim()
        self.tab = np.ones((self.DIM, self.DIM), dtype='i2') * self.LIVRE
        self.win_r1 = self.win_c1 = self.win_r2 = self.win_c2 = 0

    # Inicia o tabuleiro com a configuracao padrao
    def iniciaLimpo(self):
        self.tab = np.ones((self.DIM, self.DIM), dtype='i2') * self.LIVRE

    def inicia(self, tab: ndarray):
        self.tab = np.zeros((self.DIM, self.DIM), dtype='i2')
        np.copyto(self.tab, tab)

    def copiaTab(self, a_tab: ndarray):
        np.copyto(self.tab, a_tab)

    def copiaToTab(self, a_tab: ndarray) -> ndarray:
        """"
            Copia o tabuleiro atual para o a_tab recebido
            :param a_tab: ndarray
                Array contendo os valores para a cópia.
            :return: void
        """
        np.copyto(a_tab, self.tab)
        return a_tab

    def getTab(self) -> ndarray:
        lab_tab = np.zeros((self.DIM, self.DIM), dtype='i2')
        np.copyto(lab_tab, self.tab)
        return lab_tab

    def numPecas(self, jogador: int) -> int:
        li_tot = 0
        for i in range(0, self.DIM):
            for j in range(0, self.DIM):
                if self.tab[i][j] == jogador:
                    li_tot = li_tot + 1
        return li_tot

    def move(self, ai_jogador: int, jog: Jogada) -> bool:
        lb_tot = self.verifica(ai_jogador, jog)
        if lb_tot > 0:
            self.tab[jog.getLinha()][jog.getColuna()] = ai_jogador
            return True
        return False

    def fimJogo(self) -> bool:
        for linha in range(0, self.DIM):
            for coluna in range(0, self.DIM):
                if self.tab[linha][coluna] != self.LIVRE:
                    if self.temosVencedor(linha, coluna):
                        return True

        if self.obtemJogadasPossiveis(self.AZUL) is not None or self.obtemJogadasPossiveis(self.VERM) is not None:
            return False
        return True

    def vencedorCor(self) -> int:
        return self.cor[self.vencedorNum()]

    def vencedorNum(self) -> int:
        return self.tab[self.win_r1][self.win_c1]

    def verifica(self, jogador: int, jogada: Jogada) -> int:
        """
        Verifica se um movimento é válido.
        """
        if jogada.getLinha() < 0 or jogada.getColuna() < 0 or jogada.getLinha() > self.DIM - 1 or jogada.getColuna() > self.DIM - 1:
            return 0
        if self.tab[jogada.getLinha()][jogada.getColuna()] != self.LIVRE:
            return 0
        return 1

    def saiuTabuleiro(self, linha: int, coluna: int) -> bool:
        """
        Verifica se uma posicao esta fora do tabuleiro.

        :param linha: int
        :param coluna: int
        :return
            True = saiu
            False = Não saiu
        """
        return linha < 0 or coluna < 0 or linha > self.DIM - 1 or coluna > self.DIM - 1

    def count(self, jogador: int, linha: int, coluna: int, dir_x: int, dir_y: int) -> int:
        """
        Conta o numero de pecas de um jogador a partir da posicao passada e na
        direcao especificada. Os valores da direcao definida por dir_x e dir_y
        devem ser 0, 1, or -1, sendo que um deles deve ser diferente de zero.

        Valores de dir_x e dir_y, possiveis:
        (1, 0) = Analisa a linha
        (0, 1) = Analisa a coluna
        (1, -1) = Analisa a diagonal para baixo
        (1, 1) = Analisa a diagonal para cima

        :param jogador:
        :param linha:
        :param coluna:
        :param dir_x:
        :param dir_y:
        :return:
            Numero de peças em uma direção de um jogador
        """

        ct = 0  # Numero de pecas em linha de um jogador.

        lin = linha + dir_x  # define a direcao .
        col = coluna + dir_y
        while not self.saiuTabuleiro(lin, col) and self.tab[lin][col] == jogador:
            # Quadrado esta no tabuleiro e contem uma peca do jogador.
            lin += dir_x  # Va para o proximo.
            col += dir_y

        # Quadrado anterior.
        # Quadrado nao esta no tabuleiro ou contem uma peca do jogador.
        self.win_r1 = lin - dir_x
        self.win_c1 = col - dir_y

        lin = self.win_r1  # Olhe na direcao oposta.
        col = self.win_c1
        while not self.saiuTabuleiro(lin, col) and self.tab[lin][col] == jogador:
            # Quadrado esta no tabuleiro e contem uma peca do jogador.
            ct += 1
            lin -= dir_x  # Va para o proximo.
            col -= dir_y

        self.win_r2 = lin + dir_x
        self.win_c2 = col + dir_y

        # Neste ponto, (win_r1,win_c1) e (win_r2,win_c2) marcam as extremidades
        # da linha que pertence ao jogador.
        return ct

    def obtemJogadasPossiveis(self, jogador: int) -> List[Jogada]:
        lista = []

        for linha in range(0, self.DIM):
            for coluna in range(0, self.DIM):
                aux = Jogada(-1, -1, linha, coluna)
                if self.verifica(jogador, aux) > 0:
                    lista.append(aux)
        return lista

    def obtemJogadaBoa(self, jogador: int) -> Jogada:
        for k in range(5, -1, -1):
            for linha in range(0, self.DIM):
                for coluna in range(0, self.DIM):
                    best_j = Jogada(-1, -1, linha, coluna)
                    if self.verifica(jogador, best_j) > 0:
                        if self.count(jogador, linha, coluna, 1, 0) >= k:  # Analisa a linha
                            return best_j
                        if self.count(jogador, linha, coluna, 0, 1) >= k:  # Analisa a coluna
                            return best_j
                        if self.count(jogador, linha, coluna, 1, -1) >= k:  # Analisa a diagonal para baixo
                            return best_j
                        if self.count(jogador, linha, coluna, 1, 1) >= k:  # Analisa a diagonal para cima
                            return best_j
        pass

    def obtemJogadaHeuristica(self, jogador: int) -> Jogada:
        max_j = Jogada(-1, -1, -1, -1)
        aux_j = Jogada(-1, -1, -1, -1)
        valor_max = -10000
        tab_aux = np.zeros((self.DIM, self.DIM), dtype='i2')
        for linha in range(0, self.DIM):
            for coluna in range(0, self.DIM):
                aux_j.setJogada(-1, -1, linha, coluna)
                if self.verifica(jogador, aux_j) > 0:
                    np.copyto(tab_aux, self.tab)
                    tab_aux[linha][coluna] = jogador
                    valor = self.heuristicaBasica(jogador, tab_aux)
                    if valor > valor_max:
                        valor_max = valor
                        max_j.setJogada(-1, -1, linha, coluna)
                        if valor == 10000:
                            return max_j
        return max_j

    def heuristicaBasica(self, jogador: int, tab: ndarray) -> int:
        """
        Retorna um valor heuristico para o tabuleiro dado um jogador

        :param jogador: int
            numero do jogador
        :param tab: ndarray
            tabuleiro
        :return:
            valor do tabuleiro
        """
        valor = 0
        for linha in range(0, self.DIM):
            for coluna in range(0, self.DIM):
                if tab[linha][coluna] == jogador:

                    temp = self.contaHeuristica(jogador, linha, coluna, 1, 0, tab)  # Analisa a linha
                    if temp == 100:
                        return 10000
                    valor += temp

                    temp = self.contaHeuristica(jogador, linha, coluna, 0, 1, tab)  # Analisa a coluna
                    if temp == 100:
                        return 10000
                    valor += temp

                    temp = self.contaHeuristica(jogador, linha, coluna, 1, -1, tab)  # Analisa a diagonal para baixo
                    if temp == 100:
                        return 10000
                    valor += temp

                    temp = self.contaHeuristica(jogador, linha, coluna, 1, 1, tab)  # Analisa a diagonal para cima
                    if temp == 100:
                        return 10000
                    valor += temp

                elif tab[linha][coluna] != self.LIVRE:
                    valor -= 2 * self.contaHeuristica(self.oponente(jogador), linha, coluna, 1, 0, tab)  # Analisa a linha
                    valor -= 2 * self.contaHeuristica(self.oponente(jogador), linha, coluna, 0, 1, tab)  # Analisa a coluna
                    valor -= 2 * self.contaHeuristica(self.oponente(jogador), linha, coluna, 1, -1, tab)  # Analisa a diagonal para baixo
                    valor -= 2 * self.contaHeuristica(self.oponente(jogador), linha, coluna, 1, 1, tab)  # Analisa a diagonal para cima
        #  imprimeTab(tab)                                                                                    
        # print("valor do tabuleiro: {} -- para jogador:{}".format(valor, jogador))
        return valor

    def contaHeuristica(self, jogador: int, linha: int, coluna: int, dir_x: int, dir_y: int, tab: ndarray) -> int:
        """
        Conta o numero de pecas de um jogador a partir da posicao passada e na
        direcao especificada levando em consideracao a vantagem. Os valores da
        direcao definida por dirX e dirY devem ser 0, 1, or -1, sendo que um
        deles deve ser diferente de zero.

        Valores de dir_x e dir_y, possiveis:
        (1, 0) = Analisa a linha
        (0, 1) = Analisa a coluna
        (1, -1) = Analisa a diagonal para baixo
        (1, 1) = Analisa a diagonal para cima

        :param jogador: 
        :param linha: 
        :param coluna: 
        :param dir_x: 
        :param dir_y: 
        :param tab: 
        :return:
            Numero de peças em uma direção de um jogador
        """
        boqueado_ponta1 = boqueado_ponta2 = False
        lin = linha + dir_x  # define a direcao .
        col = coluna + dir_y
        while not self.saiuTabuleiro(lin, col) and tab[lin][col] == jogador:
            # Quadrado esta no tabuleiro e contem uma peca do jogador.
            lin += dir_x  # Va para o proximo.
            col += dir_y

        # verifica se fechou a ponta
        if self.saiuTabuleiro(lin, col) or tab[lin][col] != self.LIVRE:
            boqueado_ponta1 = True

        self.win_r1 = lin - dir_x  # Quadrado anterior.
        # Quadrado nao esta no tabuleiro ou contem uma peca do jogador.
        self.win_c1 = col - dir_y

        lin = lin - dir_x  # Olhe na direcao oposta.
        col = col - dir_y

        ct = 0  # Numero de pecas em linha de um jogador.
        while not self.saiuTabuleiro(lin, col) and tab[lin][col] == jogador:
            # Quadrado esta no tabuleiro e contem uma peca do jogador.
            ct += 1
            lin -= dir_x  # Va para o proximo.
            col -= dir_y

        # verifica se fechou a ponta
        if self.saiuTabuleiro(lin, col) or tab[lin][col] != self.LIVRE:
            boqueado_ponta2 = True

        self.win_r2 = lin + dir_x
        self.win_c2 = col + dir_y

        # Neste ponto, (win_r1,win_c1) e (win_r2,win_c2) marcam as extremidades
        # da linha que pertence ao jogador.

        # Verifica se esta bloqueado e nao pode fechar essa linha
        if ct < 5 and boqueado_ponta1 and boqueado_ponta2:
            ct = 0
        elif ct == 5:
            ct = 100
        elif ct == 4:
            ct = 50
        return ct

    def temosVencedor(self, linha: int, coluna: int) -> bool:
        """
        Chamado apos uma jogada para verificar se resultou em um ganhador.

        :param linha:
            linha da jogada
        :param coluna:
            coluna da jogada
        :return:
            True = existe um vencedor
            False = Nao existe um vencedor
        """
        if self.count(self.tab[linha][coluna], linha, coluna, 1, 0) >= 5:
            return True
        if self.count(self.tab[linha][coluna], linha, coluna, 0, 1) >= 5:
            return True
        if self.count(self.tab[linha][coluna], linha, coluna, 1, -1) >= 5:
            return True
        if self.count(self.tab[linha][coluna], linha, coluna, 1, 1) >= 5:
            return True

        # ainda nao existe vencedor
        self.win_r1 = -1
        return False

    def __str__(self) -> str:
        """
        Retorna o tabuleiro na forma de String  
        """
        lo_buff = "   "
        for i in range(0, self.DIM):
            lo_buff += str(i) + ' '

        lo_buff += "\n"
        for linha in range(0, self.DIM):
            lo_buff += " " + str(linha)
            for coluna in range(0, self.DIM):
                if self.tab[linha][coluna] == self.VERM:
                    lo_buff += " V"
                elif self.tab[linha][coluna] == self.AZUL:
                    lo_buff += " A"
                else:
                    lo_buff += " -"
            lo_buff += '\n'
        return lo_buff

    def imprimeTab(self, tab: ndarray):
        """
        Retorna o tabuleiro na forma de String
        :param tab: ndarray
        """
        for linha in range(0, self.DIM):
            for coluna in range(0, self.DIM):
                if tab[linha][coluna] == self.VERM:
                    print(" V", end='')
                elif tab[linha][coluna] == self.AZUL:
                    print(" A", end='')
                elif tab[linha][coluna] == self.LIVRE:
                    print(" L", end='')
                else:
                    print(" -", end='')
            print(" ")

    def oponente(self, jogador: int) -> int:
        if jogador == self.AZUL:
            return self.VERM
        else:
            return self.AZUL

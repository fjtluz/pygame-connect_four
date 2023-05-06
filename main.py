import random
import math

import copy

import pygame


def imprime_matriz(matriz):
    for lin in matriz:
        print(lin)


def monta_tabuleiro(screen):
    top_row_start = pygame.Vector2(50, 70)
    top_row_end = pygame.Vector2(screen.get_width() - 50, 70)

    left_column_start = pygame.Vector2(50, 70)
    left_column_end = pygame.Vector2(50, screen.get_height() - 30)

    for i in range(7):
        pygame.draw.line(screen, "black", top_row_start, top_row_end, 20)
        top_row_start.y += (screen.get_height() / 7) + 2.5
        top_row_end.y += (screen.get_height() / 7) + 2.5

    for i in range(8):
        pygame.draw.line(screen, "black", left_column_start, left_column_end, 20)
        left_column_start.x += (screen.get_width() / 8) + 10
        left_column_end.x += (screen.get_width() / 8) + 10


def adiciona_peca(matriz, coluna, color):
    pos_adicionada = (-1, -1)

    linha = len(matriz) - 1

    while linha >= 0:
        if matriz[linha][coluna] == 0:
            matriz[linha][coluna] = color
            pos_adicionada = (linha, coluna)
            break
        linha -= 1

    return pos_adicionada


def imprime_pecas(screen, matriz, intervalo_col, intervalo_lin):
    for (idx_row, row) in enumerate(matriz):
        for (idx_col, col) in enumerate(row):
            if col != 0:
                color = "red" if col == 1 else "yellow"
                pos_x = (intervalo_col[idx_col][0] + intervalo_col[idx_col][1]) / 2
                pos_y = (intervalo_lin[idx_row][0] + intervalo_lin[idx_row][1]) / 2
                pos_circulo = pygame.Vector2(pos_x, pos_y)
                pygame.draw.circle(screen, color, pos_circulo, 40)


def monta_intervalos(start, size):
    intervalo = []
    for i in range(7):
        if i == 0:
            intervalo.append((start, start + size))
        else:
            new_start = intervalo[i - 1][1] + 20
            intervalo.append((new_start, new_start + size))
    return intervalo


def jogo_acabou(matriz: list[list[int]]):
    resultado = (False, -1)

    # possíveis colunas que o vermelho pode ganhar
    colunas_potencial_vermelho = [[], [], [], [], [], [], []]
    # possíveis colunas que o amarelo pode ganhar
    colunas_potencial_amarelo = [[], [], [], [], [], [], []]

    """ 
        Explicação da relação lista-diagonal
        ___________________________
        | x  x  x    x    x  x  x |  c - crescentes_potencial
        | x  x  x    x    x  x  x |  d - decrescentes_potencial
        | x  x  x    x    x  x  x |
        | 0c x  x    x    x  x 5d |
        | 1c x  x    x    x  x 4d |
        | 2c 3c 4c 5c/0d 1d 2d 3d |
        ---------------------------
    """

    linhas_totalmente_preenchidas = 0

    # possíveis diagonais crescentes (direita pra esquerda) que o vermelho pode ganhar
    crescentes_potencial_vermelho = [[], [], [], [], [], []]
    # possíveis diagonais crescentes (direita pra esquerda) que o amarelo pode ganhar
    crescentes_potencial_amarelo = [[], [], [], [], [], []]

    # possíveis diagonais decrescentes (esquerda pra direita) que o vermelho pode ganhar
    decrescentes_potencial_vermelho = [[], [], [], [], [], []]
    # possíveis diagonais decrescentes (esquerda pra direita) que o amarelo pode ganhar
    decrescentes_potencial_amarelo = [[], [], [], [], [], []]

    # utilizando while, pois list.reverse() inverte o index, o que não é desejado
    idx_lin = len(matriz) - 1
    while idx_lin >= 0:
        if not resultado[0]:
            lin = matriz[idx_lin]
            if lin.count(0) == 0:
                linhas_totalmente_preenchidas += 1

            # possível linha que o vermelho pode ganhar
            linha_potencial_vermelho = []
            # possível linha que o amarelo pode ganhar
            linha_potencial_amarelo = []

            for idx_cel, cel in enumerate(lin):

                # calcula o grid_idx; Ex.: (lin=3, col=2) => 32
                grid_idx = idx_lin * 10 + idx_cel

                # calcula o idx da lista de diagonais crescente possíveis;
                # utiliza-se o 9, pois é a diferença entre os grid_idx da diagonais crescrentes.
                # Ex.: (42) => (42 - 30) % 9 === 12 % 9 === 3
                idx_cres = (grid_idx - 30) % 9
                # calcula o idx da lista de diagonais descrentes possíveis;
                # utiliza-se o 11, pois é a diferença entre os grid_idx da diagonais decrescrentes;
                # utiliza-se o -1, pois essa formula parte do 1 e não do zero.
                # Ex.: (23) => (23 - 30) % 11 === -7 % 11 === 4 => 4 - 1 === 3
                idx_decr = ((grid_idx - 30) % 11) - 1

                # define as referências de acordo com a cor analisada no momento
                if cel == 1:
                    linha_potencial = linha_potencial_vermelho
                    coluna_potencial = colunas_potencial_vermelho[idx_cel]
                    crescente_potencial = crescentes_potencial_vermelho[idx_cres] if 6 > idx_cres >= 0 else None
                    decrescente_potencial = decrescentes_potencial_vermelho[idx_decr] if 6 > idx_decr >= 0 else None
                elif cel == 2:
                    linha_potencial = linha_potencial_amarelo
                    coluna_potencial = colunas_potencial_amarelo[idx_cel]
                    crescente_potencial = crescentes_potencial_amarelo[idx_cres] if 6 > idx_cres >= 0 else None
                    decrescente_potencial = decrescentes_potencial_amarelo[idx_decr] if 6 > idx_decr >= 0 else None
                else:
                    continue

                linha_possui_quatro = possui_quatro_seguidos(linha_potencial, idx_cel, 1)
                coluna_possui_quatro = possui_quatro_seguidos(coluna_potencial, idx_lin, -1)
                cres_possui_quatro = possui_quatro_seguidos(crescente_potencial, grid_idx, -9)
                decrescente_potencial = possui_quatro_seguidos(decrescente_potencial, grid_idx, -11)

                if linha_possui_quatro or coluna_possui_quatro or cres_possui_quatro or decrescente_potencial:
                    resultado = (True, cel)
                    break
        idx_lin -= 1

    if not resultado[0] and linhas_totalmente_preenchidas == len(matriz):
        resultado = (True, 3)

    return resultado


def possui_quatro_seguidos(ref_list: list, index_atual: int, diferenca: int):
    """
        Recebe uma lista referência que contém as peças já analisadas
        que podem consistir uma sequencia de quatro ou mais, o index atual
        a ser analisado e a diferença esperada entre o último item da lista
        e o index atual.

        Se a diferença do index atual com o último item da lista não for
        a diferença esperada, a lista referência é limpada e recomeçada com o 
        index atual
        
        Se a diferença for igual, o index atual é acrescentado ao final da lista.
        
        Retorna se o tamanho da lista é maior ou igual a 4. Se for, indica que 
        o jogo deve acabar, senão o jogo continua.
    """
    if ref_list is None:
        return False

    if len(ref_list):
        ultimo_index = ref_list[len(ref_list) - 1]
        if index_atual - ultimo_index != diferenca:
            ref_list.clear()
    ref_list.append(index_atual)

    return len(ref_list) >= 4


def pecas_na_linha(linha: list[int], peca: int) -> list[int]:
    """
        Itera pela quantidade de peças de uma determinada cor presentes na linha informada
        e retorna uma lista coma posição dessas peças. E atualiza a matriz de valores

        :param matriz_valores: matriz de valores
        :param linha: referencia da linha a ser analisada
        :param peca: peca a ser procurada na linha
        :return: lista de posicoes da peça informada
    """

    pecas = []
    inicio_busca = 0
    for i in range(linha.count(peca)):
        inicio_busca = linha.index(peca, inicio_busca)
        pecas.append(inicio_busca)
        inicio_busca += 1

    return pecas


def coluna_ja_visitada(colunas_visitadas, idx_lin, idx_col) -> bool:
    """
        Verifica se a coluna já foi verifica por em outra linha anteriormente

        :param colunas_visitadas:
        :param idx_lin:
        :param idx_col:
        :return:
    """

    visitado = False

    for coluna in colunas_visitadas:
        if (coluna - idx_col) % 10 == 0 and (coluna != (idx_lin * 10) + idx_col):
            visitado = True

    return visitado


def define_valor_diagonal(matriz_pecas, matriz_valores, idx_lin, pos_peca, pos_anl):

    linha = matriz_pecas[idx_lin]
    valor_peca = matriz_pecas[idx_lin][pos_peca]

    # se é a peça logo ao lado e não está na primeira linha
    if abs(pos_anl - pos_peca) == 1 and idx_lin > 0:

        # se a posição acima desta estiver
        if matriz_pecas[idx_lin - 1][pos_anl] == 0:

            # possui ao menos uma diagonal => valor 1
            valor_diagonal = 1

            # lista de posições que irão receber um valor
            posicoes_a_serem_valoradas = []

            if matriz_pecas[idx_lin][pos_anl] != 0:
                posicoes_a_serem_valoradas.append((idx_lin - 1, pos_anl))

            # 1 = direita; -1 = esquerda
            direcao = pos_peca - pos_anl

            # verifica se uma posição a direita da peça não gera overflow
            if direcao == 1:
                # posição a um espaço à direita da peça não estoura o grid pela direita
                permite_um_ao_lado = pos_peca + direcao <= len(linha) - 1
                # posição a dois espaços à direita da peça não estoura o grid pela direita
                permite_dois_ao_lado = pos_peca + (2 * direcao) <= len(linha) - 1
                # posição três espaços a direita da posição analisa não estoura o grid pela esquerda
                permite_tres_ao_lado = pos_peca + (3 * direcao) <= len(linha) - 1

                # para os seguintes se trata da direção inversa
                # posição a um espaço a esquerda da posição analisa não estoura o grid pela esquerda
                permite_um_outro_lado = pos_anl + (-1 * direcao) >= 0
                # posição dois espaços a esquerda da peça não estoura o grid pela esquerda
                permite_dois_outro_lado = pos_anl + (-2 * direcao) >= 0

            # verifica se uma posição a esquerda da peça não gera underflow
            else:
                # posição a um espaço à esquerda da peça não estoura o grid pela esquerda
                permite_um_ao_lado = pos_peca + direcao >= 0
                # posição a dois espaços à esquerda da peça não estoura o grid pela esquerda
                permite_dois_ao_lado = pos_peca + (2 * direcao) >= 0
                # posição três espaços a esquerda da peça não estoura o grid pela esquerda
                permite_tres_ao_lado = pos_peca + (3 * direcao) >= 0

                # para os seguintes se trata da direção inversa
                # posição a um espaço a direita da posição analisa não estoura o grid pela direita
                permite_um_outro_lado = pos_anl + (-1 * direcao) <= len(linha) - 1
                # posição dois espaços a direita da posição analisa não estoura o grid pela direita
                permite_dois_outro_lado = pos_anl + (-2 * direcao) <= len(linha) - 1

            # se não se encontra na última linha e permite uma posição ao lado
            if idx_lin < len(matriz_pecas) - 1 and permite_um_ao_lado:
                # se o espaço na linha abaixo e uma posição ao lado da peça possui o mesmo valor que a peça
                if matriz_pecas[idx_lin + 1][pos_peca + direcao] == valor_peca:
                    valor_diagonal = 2
                    # se não se encontra na penúltima linha e permite duas posições ao lado
                    if idx_lin < len(matriz_pecas) - 2 and permite_dois_ao_lado:
                        # se o espaço duas linhas abaixo e dois posições ao lado da peça possui o mesmo valor que a peça
                        if matriz_pecas[idx_lin + 2][pos_peca + (2 * direcao)] == valor_peca:
                            # se não se encontra na antepenúltima linha e permite três posições ao lado
                            if idx_lin < len(matriz_pecas) - 3 and permite_tres_ao_lado:
                                # se o espaço três linhas abaixo e três posições ao lado da peça está vazio
                                if matriz_pecas[idx_lin + 3][pos_peca + (3 * direcao)] == 0:
                                    posicoes_a_serem_valoradas.append((idx_lin + 3, pos_peca + (3 * direcao)))
                            valor_diagonal = 15
                    # se não se encontra na segunda linha e permite uma posição ao outro lado da peça
                    if idx_lin > 1 and permite_um_outro_lado:
                        # se o espaço na linha acima e uma posição ao outro lado da posição analisada possui o mesmo valor que a peça
                        if matriz_pecas[idx_lin - 2][pos_anl + (-1 * direcao)] == valor_peca:
                            valor_diagonal = 20
            # se não se encontra na terceira linha e permite duas posições ao outro lado da peça
            if idx_lin > 2 and permite_dois_outro_lado:
                # se o espaço na linha acima e uma posição ao outro lado da posição analisada possui o mesmo valor que a peça
                if matriz_pecas[idx_lin - 2][pos_anl + (-1 * direcao)] == valor_peca:
                    # se o espaço duas linhas acima e duas posições ao outro lado da posição analisada possui o mesmo valor que a peça
                    if matriz_pecas[idx_lin - 3][pos_anl + (-2 * direcao)] == valor_peca:
                        valor_diagonal = 15

            for lin, col in posicoes_a_serem_valoradas:
                matriz_valores[lin][col] += valor_diagonal


def define_valor_linha(
        matriz_pecas: list[list[int]],
        matriz_valores: list[list[float]],
        colunas_visitadas: list[int],
        indexes: tuple[int, int, int],
        valor: float
):
    """
        Analisa as posições próximas da peca e determina uma valor para elas. O valor
        decresce conforme a distancia da posição pela peça aumenta. Caso haja uma peça
        de outra cor próxima, o valor decrementa mais, pois isto diminui as chances
        de forma quatro seguidos.

        :param matriz_pecas: matriz da posições das peças
        :param matriz_valores: matriz de valores
        :param colunas_visitadas: lista de colunas já visitadas
        :param indexes: tupla de indexes (index da linha, index da posicao analisada, index da peca)
        :param valor: valor atribuido a essa posicao
    """

    idx_lin = indexes[0]
    idx_pos = indexes[1]
    idx_peca = indexes[2]

    linha = matriz_pecas[idx_lin]

    cel = linha[idx_pos]
    if cel == 0 and not coluna_ja_visitada(colunas_visitadas, idx_lin, idx_pos):
        colunas_visitadas.append((idx_lin * 10) + idx_pos)
        matriz_valores[idx_lin][idx_pos] += valor
        valor -= 1
    elif cel != 0:
        matriz_valores[idx_lin][idx_pos] = -1
        if cel != linha[idx_peca]:
            valor *= 0
    else:
        valor -= 1

    if valor < 0:
        valor *= 0

    return valor


def calcula_jogada_de_maior_valor(matriz_valores_vermelho, matriz_valores_amarelo, colunas_bloqueadas) -> tuple[int, int, bool]:
    """
        Retorna uma tupla contendo, o valor da maior jogada, a coluna que deve jogada e se a jogada favorece o vermelho
    """

    maior_valor = (0, 0, False)
    jogadas_com_maior_valor = []

    for idx_lin in range(len(matriz_valores_vermelho)):
        linha_vermelho = matriz_valores_vermelho[idx_lin]
        linha_amarelo = matriz_valores_amarelo[idx_lin]
        for idx_col in range(len(linha_amarelo)):
            valor_vermelho = linha_vermelho[idx_col]
            valor_amarelo = linha_amarelo[idx_col]
            maximo_linha = valor_vermelho + valor_amarelo
            if colunas_bloqueadas.count(idx_col) == 0:
                if maximo_linha > maior_valor[0]:
                    maior_valor = (maximo_linha, idx_col, valor_vermelho > valor_amarelo)
                    jogadas_com_maior_valor = [maior_valor]
                elif maximo_linha == maior_valor[0]:
                    jogadas_com_maior_valor.append((maximo_linha, idx_col, valor_vermelho > valor_amarelo))

    for possivel_jogada in jogadas_com_maior_valor:
        maior_valor = possivel_jogada
        if possivel_jogada[2]:
            break

    return maior_valor


def simula_jogada(matriz_pecas: list[list[int]], jogada_a_frente=0):
    """
        Define um valor para cada jogada possível e escolhe a jogada de maior valor
    """
    matriz_valores_vermelho = [[0.0 for i in range(7)] for j in range(6)]
    matriz_valores_amarelo = [[0.0 for i in range(7)] for j in range(6)]
    colunas_visitadas = []

    idx_lin = len(matriz_pecas) - 1
    while idx_lin >= 0:
        lin = matriz_pecas[idx_lin]

        idx_pecas = []
        idx_pecas.extend(pecas_na_linha(lin, 1))
        idx_pecas.extend(pecas_na_linha(lin, 2))

        for idx_peca in idx_pecas:
            matriz_valores_vermelho[idx_lin][idx_peca] = -1
            matriz_valores_amarelo[idx_lin][idx_peca] = -1

            cor = matriz_pecas[idx_lin][idx_peca]
            matriz_valores = matriz_valores_vermelho if cor == 1 else matriz_valores_amarelo

            valor = 3.5
            # pecas a esquerda
            posicoes_a_esquerda = range(0, idx_peca)
            idx_esq = posicoes_a_esquerda.stop - 1
            while idx_esq >= posicoes_a_esquerda.start:
                if [0, matriz_pecas[idx_lin][idx_peca]].count(matriz_pecas[idx_lin][3]):
                    valor = define_valor_linha(matriz_pecas, matriz_valores, colunas_visitadas, (idx_lin, idx_esq, idx_peca), valor)
                if abs(idx_peca - idx_esq) == 1:
                    define_valor_diagonal(matriz_pecas, matriz_valores, idx_lin, idx_peca, idx_esq)

                idx_esq -= posicoes_a_esquerda.step

            valor = 3.5
            # pecas a direita
            for idx_dir in range(idx_peca + 1, len(lin)):
                if [0, matriz_pecas[idx_lin][idx_peca]].count(matriz_pecas[idx_lin][3]):
                    valor = define_valor_linha(matriz_pecas, matriz_valores, colunas_visitadas, (idx_lin, idx_dir, idx_peca), valor)
                if abs(idx_peca - idx_dir) == 1:
                    define_valor_diagonal(matriz_pecas, matriz_valores, idx_lin, idx_peca, idx_dir)

            if idx_lin > 0:
                valor = 2
                if idx_lin < len(matriz_pecas) - 1 and matriz_pecas[idx_lin + 1][idx_peca] == matriz_pecas[idx_lin][idx_peca]:
                    if idx_lin < len(matriz_pecas) - 2 and matriz_pecas[idx_lin + 2][idx_peca] == matriz_pecas[idx_lin + 1][idx_peca]:
                        valor = 20
                    else:
                        valor = 3

                if matriz_pecas[idx_lin - 1][idx_peca] == 0:
                    # zera se a linha acima for o topo do grid e não for fechar 4
                    valor = 0 if valor != 15 and idx_lin == 1 else valor
                    matriz_valores[idx_lin - 1][idx_peca] += valor

        idx_lin -= 1

    # calcula a jogada de maior valor sem coluans proibidas
    maior_valor = calcula_jogada_de_maior_valor(matriz_valores_vermelho, matriz_valores_amarelo, [])

    if jogada_a_frente == 0:

        # cria um clone da matriz de peças e simula uma jogada nela
        clone_matriz = copy.deepcopy(matriz_pecas)
        pos_jogada = adiciona_peca(clone_matriz, maior_valor[1], 2)

        # se a jogada for valida
        if pos_jogada != (-1, -1):

            colunas_proibidas = []

            # procura qual seria a melhor jogada do próximo turno, com base na matriz clonada
            proximo_maior_valor = simula_jogada(clone_matriz, jogada_a_frente + 1)

            # verifica se a peça jogada gera um fim de jogo
            ganhou = jogo_acabou(clone_matriz)

            # verifica se a valor da próxima jogada é maior que o da jogada atual
            # e se o próxima jogada ocorre na mesma coluna que a jogada atual
            # e se está próxima jogada favorece o vermelho
            # e se, com a jogada atual, o jogo não termina
            # enquanto isto for verdade, ele tenta calcualr uma jogada melhor
            while proximo_maior_valor[0] > maior_valor[0] and proximo_maior_valor[1] == maior_valor[1] and proximo_maior_valor[2] and not ganhou[0]:
                clone_matriz = copy.deepcopy(matriz_pecas)

                # adiciona a coluna atual na lista de colunas proibidas
                # para não ser escolhida na próxima iteração
                colunas_proibidas.append(maior_valor[1])

                # armazena a jogada antiga e recalcula a jogada maior valor com base nas colunas proibidas
                jogada_antiga = maior_valor
                maior_valor = calcula_jogada_de_maior_valor(matriz_valores_vermelho, matriz_valores_amarelo, colunas_proibidas)

                # se não foi encontrado uma jogada válida, escolhe-se a jogada antiga
                if maior_valor == (0, 0, False):
                    maior_valor = jogada_antiga
                    break

                # simula a adição desta jogada recalculada com intuito de checar sua validade
                pos_jogada = adiciona_peca(clone_matriz, maior_valor[1], 2)
                if pos_jogada != (-1, -1):
                    # se for válida
                    #   informa no console qual era a jogada antiga, o que essa jogada acarretaria e qual foi a jogada recalculada, respectivamente
                    #   ressimula a próxima jogada com base na jogada recalculada
                    #   recalcula se a jogada acarreta numa vitória para o amarelo
                    print(f'Jogada recalculada => Antes: {jogada_antiga}; Próxima jogada: {proximo_maior_valor}; Atual: {maior_valor}')
                    proximo_maior_valor = simula_jogada(clone_matriz, jogada_a_frente + 1)
                    ganhou = jogo_acabou(clone_matriz)
                else:
                    colunas_proibidas.append(maior_valor[1])
        else:
            maior_valor = calcula_jogada_de_maior_valor(matriz_valores_vermelho, matriz_valores_amarelo, [maior_valor[1]])

    if jogada_a_frente == 0:
        print(f"Jogada escolhida: {maior_valor[1]}")
        matriz_valores = []
        for i in range(6):
            linha = []
            for j in range(7):
                soma = matriz_valores_vermelho[i][j] + matriz_valores_amarelo[i][j]
                soma = soma if soma > -1 else -1
                linha.append(soma)
            matriz_valores.append(linha)
        imprime_matriz(matriz_valores)

    return maior_valor


def decide_coluna(matriz: list[list]):
    coluna_selecionada = -1

    # min mode
    idx_lin = len(matriz) - 1
    while idx_lin >= 0:
        lin = matriz[idx_lin]
        for idx_col, cel in enumerate(lin):
            if cel == 1:
                um_esquerda = lin[idx_col - 1] if idx_col > 0 else -1
                dois_esquerda = lin[idx_col - 2] if idx_col > 1 else -1
                tres_esquerda = lin[idx_col - 3] if idx_col > 2 else -1
                um_esq_um_abaixo = matriz[idx_lin + 1][idx_col - 1] if idx_lin < len(matriz) - 1 and idx_col > 0 else -1

                um_direita = lin[idx_col + 1] if idx_col < len(lin) - 1 else -1
                dois_direita = lin[idx_col + 2] if idx_col < len(lin) - 2 else -1
                tres_direita = lin[idx_col + 3] if idx_col < len(lin) - 3 else -1
                um_dir_um_abaixo = matriz[idx_lin + 1][idx_col + 1] if idx_lin < len(matriz) - 1 and idx_col < len(
                    lin) - 1 else -1
                tres_dir_um_abaixo = matriz[idx_lin + 1][idx_col + 3] if idx_lin < len(matriz) - 1 and idx_col < len(
                    lin) - 3 else -1

                acima = matriz[idx_lin - 1][idx_col] if idx_lin > 0 else -1
                um_abaixo = matriz[idx_lin + 1][idx_col] if idx_lin < len(matriz) - 1 else -1
                dois_abaixo = matriz[idx_lin + 2][idx_col] if idx_lin < len(matriz) - 2 else -1

                um_diag_esq = matriz[idx_lin - 1][idx_col - 1] if idx_lin > 0 and idx_col > 0 else -1
                um_diag_esq_um_esq = matriz[idx_lin - 1][idx_col - 2] if idx_lin > 0 and idx_col > 1 else -1
                dois_diag_esq = matriz[idx_lin - 2][idx_col - 2] if idx_lin > 1 and idx_col > 1 else -1
                dois_diag_esq_um_esq = matriz[idx_lin - 2][idx_col - 3] if idx_lin > 1 and idx_col > 2 else -1
                tres_diag_esq = matriz[idx_lin - 3][idx_col - 3] if idx_lin > 2 and idx_col > 2 else -1

                um_diag_dir = matriz[idx_lin - 1][idx_col + 1] if idx_lin > 0 and idx_col < len(lin) - 1 else -1
                um_diag_dir_um_dir = matriz[idx_lin - 1][idx_col + 2] if idx_lin > 0 and idx_col < len(lin) - 2 else -1
                dois_diag_dir = matriz[idx_lin - 2][idx_col + 2] if idx_lin > 1 and idx_col < len(lin) - 2 else -1
                dois_diag_dir_um_dir = matriz[idx_lin - 2][idx_col + 3] if idx_lin > 1 and idx_col < len(
                    lin) - 3 else -1
                tres_diag_dir = matriz[idx_lin - 3][idx_col + 3] if idx_lin > 2 and idx_col < len(lin) - 3 else -1

                if not [-1, 2].count(acima) and um_abaixo == 1 and dois_abaixo == 1:
                    coluna_selecionada = idx_col

                if um_direita == 1 and dois_direita == 1:
                    if not [-1, 2].count(tres_direita) and tres_dir_um_abaixo != 0:
                        coluna_selecionada = idx_col + 3
                    elif not [-1, 2].count(um_esquerda) and um_esq_um_abaixo != 0:
                        coluna_selecionada = idx_col - 1
                elif dois_direita == 1 and tres_direita == 1:
                    if not [-1, 2].count(um_direita) and um_dir_um_abaixo != 0:
                        coluna_selecionada = idx_col + 1
                elif dois_esquerda == 1 and tres_esquerda == 1:
                    if not [-1, 2].count(um_esquerda) and um_esq_um_abaixo != 0:
                        coluna_selecionada = idx_col - 1

                if um_diag_dir == 1:
                    if dois_diag_dir == 1 and dois_diag_dir_um_dir != 0:
                        coluna_selecionada = idx_col + 3
                    elif tres_diag_dir == 1 and um_diag_dir_um_dir != 0:
                        coluna_selecionada = idx_col + 2
                elif dois_diag_dir == 1 and tres_diag_dir == 1:
                    if um_direita != 0:
                        coluna_selecionada = idx_col + 1

                if um_diag_esq == 1:
                    if dois_diag_esq == 1 and dois_diag_esq_um_esq != 0:
                        coluna_selecionada = idx_col - 3
                    elif tres_diag_esq == 1 and um_diag_esq_um_esq != 0:
                        coluna_selecionada = idx_col - 2
                elif dois_diag_esq == 1 and tres_diag_esq == 1:
                    if um_esquerda != 0:
                        coluna_selecionada = idx_col - 1
        idx_lin -= 1

    if coluna_selecionada == -1:
        coluna_selecionada = math.floor(random.random() * 7)

    return coluna_selecionada


def start_game():
    # monta a matriz
    matriz_pecas = [[0 for i in range(7)] for j in range(6)]

    pygame.init()
    screen = pygame.display.set_mode((1300, 800))
    clock = pygame.time.Clock()
    running = True

    # (largura tela - 100 (distancia esquerda + distancia direita) / qtd_divisorias) + fator_correcao
    col_size = ((screen.get_width() - 100) / 8) + 2.5
    col_start = 60

    # (altura tela - 100 (distancia cima + distancia baixo) / qtd_divisorias) + fator_correcao
    row_size = ((screen.get_height() - 100) / 7) - 2.5
    row_start = 80

    # monta intervalo de posição das colunas
    intervalo_colunas = monta_intervalos(col_start, col_size)

    # monta intervalo de posição das linhas
    intervalo_linhas = monta_intervalos(row_start, row_size)

    # inicializar font utilizada no jogo
    pygame.font.init()
    font = pygame.font.SysFont("Comic Sans MS", 30)

    # informa texto de quem é o jogador atual
    texto_base = font.render("JOGADOR ATUAL:", False, "white")
    jogador_atual_texto = font.render("VERMELHO", False, "red")

    # 1 - Vermelho, 2 - Amarelo
    jogador_atual = 1

    # boolean para caso o click do mouse já foi tratado
    validate_press = False

    # define o ganhador
    ganhador = -1

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("white")
        pygame.draw.line(screen, "black", (0, 15), (screen.get_width(), 15), 30)
        monta_tabuleiro(screen)
        imprime_pecas(screen, matriz_pecas, intervalo_colunas, intervalo_linhas)

        # verifica o resultado do jogo
        resultado = jogo_acabou(matriz_pecas)
        if resultado[0]:
            ganhador = resultado[1]

            if ganhador == 3:
                texto_base = font.render("FIM DE JOGO: EMPATE", False, "blue")
            else:
                texto_base = font.render("VENCEDOR:", False, "green")
                if ganhador == 1:
                    jogador_atual_texto = font.render("VERMELHO", False, "red")
                else:
                    jogador_atual_texto = font.render("AMARELO", False, "yellow")
                screen.blit(jogador_atual_texto, pygame.Vector2(texto_base.get_width() + 15, 10))
            screen.blit(texto_base, pygame.Vector2(10, 10))
        else:
            screen.blit(texto_base, pygame.Vector2(10, 10))
            screen.blit(jogador_atual_texto, pygame.Vector2(texto_base.get_width() + 15, 10))
            # Jogador
            if jogador_atual == 1:
                state_mouse = pygame.mouse.get_pressed(num_buttons=3)

                if state_mouse[0] and not validate_press:
                    validate_press = True
                    current_pos = pygame.mouse.get_pos()
                    coluna_selecionada = -1
                    for (idx, intevalo) in enumerate(intervalo_colunas):
                        if intevalo[0] <= current_pos[0] <= intevalo[1]:
                            coluna_selecionada = idx
                            break
                    if coluna_selecionada != -1:
                        pos_adicionada = adiciona_peca(matriz_pecas, coluna_selecionada, jogador_atual)
                        if pos_adicionada != (-1, -1):
                            jogador_atual = 2
                            jogador_atual_texto = font.render("AMARELO", False, "yellow")
                elif not state_mouse[0]:
                    validate_press = False
            # IA
            elif jogador_atual == 2:
                coluna_selecionada = simula_jogada(matriz_pecas)[1]  # decide_coluna(matriz)
                pos_adicionada = adiciona_peca(matriz_pecas, coluna_selecionada, jogador_atual)
                if pos_adicionada != (-1, -1):
                    jogador_atual = 1
                    jogador_atual_texto = font.render("VERMELHO", False, "red")

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(10)

    print(f"Ganhador: {ganhador}")

    pygame.quit()


if __name__ == '__main__':
    start_game()

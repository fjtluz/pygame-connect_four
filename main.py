import random
import math

import pygame


def monta_matriz():
    return [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ]

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
                pos_x = (intervalo_col[idx_col][0] + intervalo_col[idx_col][1])/2
                pos_y = (intervalo_lin[idx_row][0] + intervalo_lin[idx_row][1])/2
                pos_circulo = pygame.Vector2(pos_x, pos_y)
                pygame.draw.circle(screen, color, pos_circulo, 40)


def monta_intervalos(start, size):
    intervalo = []
    for i in range(7):
        if i == 0:
            intervalo.append((start, start + size))
        else:
            new_start = intervalo[i-1][1] + 20
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

    return resultado


def possui_quatro_seguidos(ref_list: list, index_atual: int, diferenca: int):
    f"""
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


def simula_jogada(matriz: list[list[int]]):
    matriz_de_valores = monta_matriz()
    colunas_validas_visitadas = []

    idx_lin = len(matriz) - 1
    while idx_lin >= 0:
        lin = matriz[idx_lin]

        lista_pecas = []

        ultimo_verificado = 0
        for i in range(lin.count(1)):
            ultimo_verificado = lin.index(1, ultimo_verificado)
            matriz_de_valores[idx_lin][ultimo_verificado] = -1
            lista_pecas.append(ultimo_verificado)
            ultimo_verificado += 1

        ultimo_verificado = 0
        for i in range(lin.count(2)):
            ultimo_verificado = lin.index(2, ultimo_verificado)
            matriz_de_valores[idx_lin][ultimo_verificado] = -1
            ultimo_verificado += 1

        for idx_col in lista_pecas:

            # espaços a esquerda
            espacos_a_esquerda = range(idx_col)

            valor = 3
            idx_espaco = espacos_a_esquerda.stop - 1
            while idx_espaco >= espacos_a_esquerda.start:
                if [0, 1].count(matriz[idx_lin][idx_espaco]):
                    if matriz[idx_lin][idx_espaco] == 0:
                        colunas_validas_visitadas.append(idx_espaco)
                        matriz_de_valores[idx_lin][idx_espaco] += valor
                    valor -= 1
                else:
                    valor -= 2
                if valor < 0:
                    valor = 0
                idx_espaco -= espacos_a_esquerda.step

            # espaços a direita
            espacos_a_direita = range(idx_col + 1, len(lin))
            valor = 3
            for idx_espaco in espacos_a_direita:
                if [0, 1].count(matriz[idx_lin][idx_espaco]):
                    if matriz[idx_lin][idx_espaco] == 0:
                        colunas_validas_visitadas.append(idx_espaco)
                        matriz_de_valores[idx_lin][idx_espaco] += valor
                    valor -= 1
                else:
                    valor -= 2
                if valor < 0:
                    valor = 0

            if idx_lin > 0:
                if matriz[idx_lin - 1][idx_col] == 0:
                    matriz_de_valores[idx_lin - 1][idx_col] += 3
        idx_lin -= 1

    print(matriz_de_valores)


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
                um_dir_um_abaixo = matriz[idx_lin + 1][idx_col + 1] if idx_lin < len(matriz) - 1 and idx_col < len(lin) - 1 else -1
                tres_dir_um_abaixo = matriz[idx_lin + 1][idx_col + 3] if idx_lin < len(matriz) - 1 and idx_col < len(lin) - 3 else -1

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
                dois_diag_dir_um_dir = matriz[idx_lin - 2][idx_col + 3] if idx_lin > 1 and idx_col < len(lin) - 3 else -1
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
    matriz = monta_matriz()

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

        # verifica o resultado do jogo
        resultado = jogo_acabou(matriz)
        if resultado[0]:
            ganhador = resultado[1]
            break

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("white")

        pygame.draw.line(screen, "black", (0, 15), (screen.get_width(), 15), 30)
        screen.blit(texto_base, pygame.Vector2(10, 10))
        screen.blit(jogador_atual_texto, pygame.Vector2(texto_base.get_width() + 15, 10))

        monta_tabuleiro(screen)
        imprime_pecas(screen, matriz, intervalo_colunas, intervalo_linhas)

        # Jogador
        if jogador_atual == 1:
            state_mouse = pygame.mouse.get_pressed(num_buttons=3)

            if state_mouse[0] and not validate_press:
                validate_press = True
                current_pos = pygame.mouse.get_pos()
                if current_pos[1] < 50:
                    coluna_selecionada = -1
                    for (idx, intevalo) in enumerate(intervalo_colunas):
                        if intevalo[0] <= current_pos[0] <= intevalo[1]:
                            coluna_selecionada = idx
                            break
                    if coluna_selecionada != -1:
                        pos_adicionada = adiciona_peca(matriz, coluna_selecionada, jogador_atual)
                        if pos_adicionada != (-1, -1):
                            jogador_atual = 2
                            jogador_atual_texto = font.render("AMARELO", False, "yellow")
            elif not state_mouse[0]:
                validate_press = False
        # IA
        elif jogador_atual == 2:
            coluna_selecionada = decide_coluna(matriz)
            pos_adicionada = adiciona_peca(matriz, coluna_selecionada, jogador_atual)
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

# Example file showing a basic pygame "game loop"
import pygame


def monta_tabuleiro(screen):

    top_row_start = pygame.Vector2(50, 70)
    top_row_end = pygame.Vector2(screen.get_width() - 50, 70)

    left_column_start = pygame.Vector2(50, 70)
    left_column_end = pygame.Vector2(50, screen.get_height() - 30)

    for i in range(7):
        pygame.draw.line(screen, "black", top_row_start, top_row_end, 20)
        top_row_start.y += (screen.get_height() / 7) + 2.5
        top_row_end.y += (screen.get_height() / 7) + 2.5

    for i in range (8):
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


def jogo_acabou(matriz):

    resultado = (False, -1)

    matriz_pos_vermelho = []
    matriz_pos_amarelo = []

    # Verifica quatro na mesma linha
    for lin in matriz:
        pos_vermelhos = []
        pos_amarelos = []
        if lin.count(1) >= 4 or lin.count(2) >= 4:
            for (col_idx, col) in enumerate(lin):
                if col == 1:
                    pos_vermelhos.append(col_idx)
                elif col == 2:
                    pos_amarelos.append(col_idx)
        matriz_pos_vermelho.append(pos_vermelhos)
        matriz_pos_amarelo.append(pos_amarelos)

    # valida colunas
    for i in range(len(matriz)):
        vermelho_atual = matriz_pos_vermelho[i]
        amarelo_atual = matriz_pos_amarelo[i]

        if len(vermelho_atual) >= 4 and possui_quatro_seguidos(vermelho_atual):
            resultado = (True, 1)
            break
        elif len(amarelo_atual) >= 4 and possui_quatro_seguidos(amarelo_atual):
            resultado = (True, 2)
            break

    # valida linhas
    for j in range(len(matriz[0])):
        pos_vermelhos = []
        pos_amarelos = []
        for (lin_idx, lin) in enumerate(matriz):
            if lin[j] == 1:
                pos_vermelhos.append(lin_idx)
            elif lin[j] == 2:
                pos_amarelos.append(lin_idx)
        if len(pos_vermelhos) >= 4 and possui_quatro_seguidos(pos_vermelhos):
            resultado = (True, 1)
            break
        elif len(pos_amarelos) >= 4 and possui_quatro_seguidos(pos_amarelos):
            resultado = (True, 2)
            break

    # valida diagonais
    pos_vermelhos = []
    pos_amarelos = []

    for (lin_idx, lin) in enumerate(matriz):
        for (col_idx, col) in enumerate(lin):
            if col == 1:
                pos_vermelhos.append((lin_idx, col_idx))
            elif col == 2:
                pos_amarelos.append((lin_idx, col_idx))

    if len(pos_vermelhos) >= 4 and possui_diagonal(pos_vermelhos):
        resultado = (True, 1)
    elif len(pos_amarelos) >= 4 and possui_diagonal(pos_amarelos):
        resultado = (True, 1)

    return resultado


def possui_diagonal(posicoes):

    diagonal_potencial_crescente = []
    diagonal_potencial_descrecente = []

    if len(posicoes) >= 4:
        idx = len(posicoes) - 1
        while idx >= 0:
            print(diagonal_potencial_crescente)
            if len(diagonal_potencial_crescente) == 4:
                break
            if len(diagonal_potencial_crescente) > 0:
                ultimo_item = diagonal_potencial_crescente[len(diagonal_potencial_crescente) - 1]
                dif_lin = posicoes[idx][0] - posicoes[idx][0]
                dif_col = posicoes[idx][1] - ultimo_item[1]
                if dif_col != -1 or dif_lin != -1:
                    diagonal_potencial_crescente = []
            diagonal_potencial_crescente.append(posicoes[idx])

    return len(diagonal_potencial_crescente) == 4



def possui_quatro_seguidos(array):
    sequencia_promissora = []

    for i in array:
        if len(sequencia_promissora) == 4:
            break
        if len(sequencia_promissora) > 0:
            ultimo_item = sequencia_promissora[len(sequencia_promissora) - 1]
            if i - ultimo_item != 1:
                sequencia_promissora = []
        sequencia_promissora.append(i)

    return len(sequencia_promissora) == 4

def start():

    matriz = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]

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

    intervalo_colunas = monta_intervalos(col_start, col_size)

    intervalo_linhas = monta_intervalos(row_start, row_size)

    pygame.font.init()
    font = pygame.font.SysFont("Comic Sans MS", 30)
    texto_base = font.render("JOGADOR ATUAL:", False, "white")
    jogador_atual_texto = font.render("VERMELHO", False, "red")
    jogador_atual = 1 # 1 - Vermelho, 2 - Amarelo

    # boolean para caso o click do mouse já foi tratado
    validate_press = False

    ganhador = -1

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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
                        if jogador_atual == 1:
                            jogador_atual = 2
                            jogador_atual_texto = font.render("AMARELO", False, "yellow")
                        else:
                            jogador_atual = 1
                            jogador_atual_texto = font.render("VERMELHO", False, "red")
        elif not state_mouse[0]:
            validate_press = False

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    print(f"Ganhador: {ganhador}")

    pygame.quit()


if __name__ == '__main__':
    start()


import pygame
import random
import time as pause

# Inicializa o Pygame
pygame.init()

# Define as dimensões da tela
x = 1080
y = 520
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption('Galaxia Desconhecida')

# Carrega o plano de fundo e redimensiona para caber na tela
bg = pygame.image.load('backgroud/blue.jpg').convert_alpha()
bg = pygame.transform.scale(bg, (x, y))

# Carrega a imagem do asteroide e redimensiona
rock = pygame.image.load('img/asteroid.png').convert_alpha()
rock = pygame.transform.scale(rock, (50, 50))

# Carrega a imagem da nave do jogador, redimensiona e rotaciona para posicionar
playerImg = pygame.image.load('img/nave.png').convert_alpha()
playerImg = pygame.transform.scale(playerImg, (50, 50))
playerImg = pygame.transform.rotate(playerImg, -90)

# Carrega a imagem do míssil e redimensiona
laser = pygame.image.load('img/missel.png').convert_alpha()
laser = pygame.transform.scale(laser, (25, 25))

# Define as posições iniciais dos objetos
pos_rock_x = 480
pos_rock_y = 360
pos_player_x = 200
pos_player_y = 300
vel_x_missil = 0
pos_x_missil = 200
pos_y_missil = 300
pontos = 10  # Pontuação inicial
triggered = False  # Controle do disparo do míssil
rodando = True  # Controle do loop do jogo

# Define a fonte para exibir o texto
font = pygame.font.SysFont('font/font_game.ttf', 50)

# Cria os retângulos de colisão para os objetos
player_rect = playerImg.get_rect()
rock_rect = rock.get_rect()
laser_rect = laser.get_rect()

# Função para o respawn do asteroide em uma posição aleatória
def respawn():
    x = 1050
    y = random.randint(3, 640)
    return [x, y]

# Função para o respawn do míssil
def respawn_missil():
    triggered = False
    respawn_missil_x = pos_player_x
    respawn_missil_y = pos_player_y
    vel_x_missil = 3
    return [respawn_missil_x, respawn_missil_y, triggered, vel_x_missil]

# Função para verificar colisões e atualizar a pontuação
def colisao():
    global pontos
    if player_rect.colliderect(rock_rect) or rock_rect.x == 60:
        pontos -= 1
        return True
    elif laser_rect.colliderect(rock_rect):
        pontos += 1
        return True
    else:
        return False

# Loop principal do jogo
while rodando:
    for event in pygame.event.get():
        # Sai do jogo se a janela for fechada
        if event.type == pygame.QUIT:
            rodando = False

    # Define o fundo da tela
    screen.blit(bg, (0, 0))

    # Cria o efeito de rolagem do fundo
    rel_x = x % bg.get_rect().width
    screen.blit(bg, (rel_x - bg.get_rect().width, 0))
    if rel_x < 1200:
        screen.blit(bg, (rel_x, 0))

    # Controle de comandos do jogador
    comando = pygame.key.get_pressed()
    if comando[pygame.K_UP] and pos_player_y > 1:
        pos_player_y -= 1
        if not triggered:
            pos_y_missil -= 1  # Move o míssil junto com a nave

    if comando[pygame.K_DOWN] and pos_player_y < 665:
        pos_player_y += 1
        if not triggered:
            pos_y_missil += 1

    # Ativa o disparo do míssil
    if comando[pygame.K_SPACE]:
        triggered = True
        vel_x_missil = 1

    # Verifica se o jogo terminou
    if pontos == -1:
        over = font.render(f'Game OVER:', True, (100, 150, 200))
        screen.blit(over, (100, 100)), pause.sleep(3)
        rodando = False

    # Respawn do asteroide se ele sair da tela
    if pos_rock_x == 50:
        pos_rock_x, pos_rock_y = respawn()

    # Respawn do míssil se ele sair da tela
    if pos_x_missil == 1100:
        pos_x_missil, pos_y_missil, triggered, vel_x_missil = respawn_missil()

    # Respawn do asteroide após uma colisão
    if pos_rock_x == 50 or colisao():
        pos_rock_x, pos_rock_y = respawn()

    # Atualiza as posições dos retângulos de colisão
    player_rect.y = pos_player_y
    player_rect.x = pos_player_x
    laser_rect.x = pos_x_missil
    laser_rect.y = pos_y_missil
    rock_rect.x = pos_rock_x
    rock_rect.y = pos_rock_y

    # Movimento dos objetos
    x -= 0.5  # Movimento do fundo
    pos_rock_x -= 1  # Movimento do asteroide
    pos_x_missil += vel_x_missil  # Movimento do míssil

    # Exibe a pontuação
    score = font.render(f'Pontos: {int(pontos)}', True, (255, 255, 255))
    screen.blit(score, (50, 50))

    # Desenha os objetos na tela
    screen.blit(rock, (pos_rock_x, pos_rock_y))
    screen.blit(laser, (pos_x_missil, pos_y_missil))
    screen.blit(playerImg, (pos_player_x, pos_player_y))

    pygame.display.update()

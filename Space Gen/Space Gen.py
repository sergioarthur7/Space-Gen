import pygame
import sys
import random

# Inicialização do Pygame
pygame.init()

# Configurações da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Space Gen")

# Cores
branco = (255, 255, 255)
vermelho = (255, 0, 0)
azul = (0, 0, 255)
preto = (0, 0, 0)
amarelo = (255, 255, 0)

# Jogador
player_width = 50
player_height = 50
player_x = largura // 2 - player_width // 2
player_y = altura - player_height - 10
player_velocidade = 2
vidas = 3

# Tiros
tiros = []
tiro_velocidade = 5
tempo_entre_tiros = 10  # Espaçamento entre tiros (em frames)
contador_tiros = 0

# Inimigos
inimigos = []
inimigo_width = 50
inimigo_height = 50
inimigo_velocidade = 2

# Pontos brancos
pontos = []
ponto_radius = 3

# Pontuação
pontuacao = 0

# Função para criar inimigos
def criar_inimigo():
    x = random.randint(0, largura - inimigo_width)
    y = random.randint(0, altura // 2)
    inimigos.append(pygame.Rect(x, y, inimigo_width, inimigo_height))

# Função para criar pontos brancos
def criar_ponto():
    x = random.randint(0, largura)
    y = random.randint(0, altura)
    pontos.append((x, y))

# Loop principal do jogo
while vidas > 0:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Controles do jogador
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        player_x -= player_velocidade
    if teclas[pygame.K_RIGHT]:
        player_x += player_velocidade

    # Limita o jogador às bordas da tela
    if player_x < 0:
        player_x = 0
    elif player_x > largura - player_width:
        player_x = largura - player_width

    # Movimenta os tiros e controla o espaçamento entre eles
    for tiro in tiros:
        tiro.y -= tiro_velocidade

    contador_tiros += 1
    if contador_tiros >= tempo_entre_tiros:
        if teclas[pygame.K_SPACE]:
            tiro = pygame.Rect(player_x + player_width // 2 - 2, player_y, 4, 10)
            tiros.append(tiro)
            contador_tiros = 0

    # Movimenta os inimigos e cria novos
    for inimigo in inimigos:
        inimigo.y += inimigo_velocidade
        if inimigo.y > altura:
            inimigos.remove(inimigo)
            criar_inimigo()

    # Colisões entre tiros e inimigos
    for tiro in tiros:
        for inimigo in inimigos:
            if tiro.colliderect(inimigo):
                tiros.remove(tiro)
                inimigos.remove(inimigo)
                criar_inimigo()
                pontuacao += 100  # Aumenta a pontuação quando acerta um inimigo

    # Colisões entre jogador e inimigos
    for inimigo in inimigos:
        if pygame.Rect(player_x, player_y, player_width, player_height).colliderect(inimigo):
            vidas -= 1
            inimigos.remove(inimigo)
            criar_inimigo()

    # Disparo de tiros
    if teclas[pygame.K_SPACE]:
        tiro = pygame.Rect(player_x + player_width // 2 - 2, player_y, 4, 10)
        tiros.append(tiro)

    # Desenha a tela
    tela.fill(preto)

    # Desenha o jogador
    pygame.draw.rect(tela, amarelo, (player_x, player_y, player_width, player_height))

    # Desenha os tiros
    for tiro in tiros:
        pygame.draw.rect(tela, azul, tiro)

    # Desenha os inimigos
    for inimigo in inimigos:
        pygame.draw.rect(tela, vermelho, inimigo)

    # Desenha os pontos brancos
    for ponto in pontos:
        pygame.draw.circle(tela, branco, ponto, ponto_radius)

    # Exibe a pontuação na tela
    fonte = pygame.font.Font(None, 36)
    texto_pontuacao = fonte.render(f"Pontuação: {pontuacao}", True, branco)
    tela.blit(texto_pontuacao, (10, 10))

    # Exibe a quantidade de vidas na tela
    texto_vidas = fonte.render(f"Vidas: {vidas}", True, branco)
    tela.blit(texto_vidas, (largura - 150, 10))

    # Atualiza a tela
    pygame.display.update()

    # Cria novos inimigos se não houver muitos
    if len(inimigos) < 5:
        criar_inimigo()

    if len(pontos) < 50:
        criar_ponto()

# Game over
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    tela.fill(preto)
    fonte = pygame.font.Font(None, 72)
    texto_game_over = fonte.render("Game Over", True, branco)
    tela.blit(texto_game_over, (largura // 2 - 150, altura // 2 - 36))

    texto_pontuacao_final = fonte.render(f"Pontuação Final: {pontuacao}", True, branco)
    tela.blit(texto_pontuacao_final, (largura // 2 - 220, altura // 2 + 36))

    pygame.display.update()

    
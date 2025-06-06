import pygame
pygame.init()

# Configuração da tela
largura = 2400
altura = 1800
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo Simples")

# Configuração do círculo
x = 50
y = 50
raio = 20
velocidade = 5

# Loop principal do jogo
rodar = True
while rodar:
    # Lidar com Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodar = False
    
    # Verificar teclas pressionadas
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        x -= velocidade
    if teclas[pygame.K_RIGHT]:
        x += velocidade
    if teclas[pygame.K_UP]:
        y -= velocidade
    if teclas[pygame.K_DOWN]:
        y += velocidade
    
    # Evitar que o objeto saia da tela (efeito wrap-around)
    x = x % largura
    y = y % altura
    
    # Desenhar Objetos
    tela.fill((0, 0, 0))  # Limpar a tela (preto)
    pygame.draw.circle(tela, (255, 0, 0), (int(x), int(y)), raio)
    
    # Atualizar a Tela
    pygame.display.flip()
    
    # Controlar a velocidade do jogo
    pygame.time.Clock().tick(60)  # Limita a 60 quadros por segundo

# Encerrar o Pygame
pygame.quit()

import pygame

pygame.init()
largura = 2400
altura = 1200
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo Simples")

x = 50
y = 50
raio = 20
velocidade = 5

rodar = True
while rodar:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodar = False

    # Lógica de movimento
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        x -= velocidade
    if teclas[pygame.K_RIGHT]:
        x += velocidade

    x = x % largura
    y = y % altura

    # Desenhar tudo
    tela.fill((0, 0, 0))  # fundo preto
    pygame.draw.circle(tela, (255, 0, 0), (int(x), int(y)), raio)
    pygame.display.flip()

pygame.quit()

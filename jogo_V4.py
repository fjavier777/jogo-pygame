import pygame
import os
import random #04/06 Faltava importar random

pygame.init()

# Configuração da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo com Spritesheet")

# Adicione no início do código:
moedas = []
for _ in range(10):
    moedas.append(pygame.Rect(
        random.randint(0, largura - 15),  # x position (subtract coin width)
        random.randint(0, altura - 15),   # y position (subtract coin height)
        15, 15                           # width and height
    ))

# Carrega a spritesheet
spritesheet = pygame.image.load("assets/spritesheet.png").convert_alpha()
if not spritesheet:
    raise FileNotFoundError("Could not load spritesheet!")

frame_rect = pygame.Rect(
    i * self.largura_quadro,
    64,  # Second row (adjust as needed)
    self.largura_quadro,
    self.altura_quadro
)

# Configuração do personagem
class Personagem(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.spritesheet = spritesheet
        self.quadros_por_animacao = 4  # Número de quadros por animação
        self.largura_quadro = 64  # Largura de cada quadro na spritesheet
        self.altura_quadro = 64   # Altura de cada quadro
        
        # Define os quadros de animação (ex: andar para direita)
        self.quadros_andar_direita = []
        for i in range(self.quadros_por_animacao):
            quadro = self.spritesheet.subsurface(
                (i * self.largura_quadro, 0),
                (self.largura_quadro, self.altura_quadro)
            )
            self.quadros_andar_direita.append(quadro)
        
        # Configuração inicial
        self.image = self.quadros_andar_direita[0]
        self.rect = self.image.get_rect(center=(largura//2, altura//2))
        self.frame_atual = 0
        self.velocidade_animacao = 0.15  # Controla a velocidade da animação

    def update(self, direcao):
        # Animação de andar
        self.frame_atual += self.velocidade_animacao
        if self.frame_atual >= len(self.quadros_andar_direita):
            self.frame_atual = 0
        
        if direcao == "direita":
            self.image = self.quadros_andar_direita[int(self.frame_atual)]
            self.rect.x += 5
        elif direcao == "esquerda":
            self.image = pygame.transform.flip(self.quadros_andar_direita[int(self.frame_atual)], True, False)
            self.rect.x -= 5

# Cria o personagem
personagem = Personagem()
todas_as_sprites = pygame.sprite.Group(personagem)

# Loop do jogo
clock = pygame.time.Clock()
rodando = True

while rodando:
    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
    
    # Controles
    teclas = pygame.key.get_pressed()
    direcao = None
    if teclas[pygame.K_RIGHT]:
        direcao = "direita"
    elif teclas[pygame.K_LEFT]:
        direcao = "esquerda"
    
    # Atualizações
    todas_as_sprites.update(direcao)
    
    # Renderização
    tela.fill((0, 0, 0))
    todas_as_sprites.draw(tela)
    pygame.display.flip()
    clock.tick(60)
    
    # Dentro do loop, após desenhar o círculo:
for moeda in moedas[:]:
    pygame.draw.rect(tela, (255, 255, 0), moeda)
    if pygame.Rect(x - raio, y - raio, raio * 2, raio * 2).colliderect(moeda):
        moedas.remove(moeda)
        pontuacao += 10

pygame.quit()
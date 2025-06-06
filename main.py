import pygame
import os
import random

pygame.init()

# Configuração da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo com Spritesheet")

# Criação das moedas
moedas = []
for _ in range(10):
    moedas.append(pygame.Rect(
        random.randint(0, largura - 15),
        random.randint(0, altura - 15),
        15, 15
    ))

# Carrega a spritesheet
try:
    spritesheet = pygame.image.load("assets/spritesheet.png").convert_alpha()
    if not spritesheet:
        raise FileNotFoundError("Spritesheet carregada vazia!")
except Exception as e:
    raise FileNotFoundError(f"Erro ao carregar spritesheet: {str(e)}")

# Configuração do personagem
class Personagem(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.spritesheet = spritesheet
        self.largura_quadro = 16
        self.altura_quadro = 16
        
        if (self.spritesheet.get_width() != 64 or 
            self.spritesheet.get_height() != 192):
            raise ValueError(f"Sua spritesheet tem {spritesheet.get_width()}x{spritesheet.get_height()} pixels, mas precisa ter 64x192")
        
        # Adicionando animações para todas as direções
        self.animacoes = {
            "parado": [self.carregar_frame(0, 0)],
            "direita": [
                self.carregar_frame(1, 0),
                self.carregar_frame(1, 1),
                self.carregar_frame(1, 2),
                self.carregar_frame(1, 3)
            ],
            "esquerda": [
                self.carregar_frame(1, 0, flip=True),
                self.carregar_frame(1, 1, flip=True),
                self.carregar_frame(1, 2, flip=True),
                self.carregar_frame(1, 3, flip=True)
            ],
            # Adicionando animações para cima e baixo
            "cima": [
                self.carregar_frame(2, 0),
                self.carregar_frame(2, 1),
                self.carregar_frame(2, 2),
                self.carregar_frame(2, 3)
            ],
            "baixo": [
                self.carregar_frame(0, 0),  # Usando frame parado como base
                self.carregar_frame(0, 1),
                self.carregar_frame(0, 2),
                self.carregar_frame(0, 3)
            ]
        }
        
        self.estado = "parado"
        self.image = self.animacoes[self.estado][0]
        self.rect = self.image.get_rect(center=(largura//2, altura//2))
        self.velocidade_x = 0
        self.velocidade_y = 0  # Adicionando velocidade vertical
        self.frame_index = 0
        self.animation_speed = 0.15
        # Direção atual para manter a última direção quando parar
        self.direcao = "baixo"
    
    def carregar_frame(self, linha, coluna, flip=False):
        try:
            frame = self.spritesheet.subsurface(
                pygame.Rect(
                    coluna * self.largura_quadro,
                    linha * self.altura_quadro,
                    self.largura_quadro,
                    self.altura_quadro
                )
            )
            return pygame.transform.flip(frame, flip, False)
        except:
            print(f"Erro ao carregar frame na linha {linha}, coluna {coluna}")
            return pygame.Surface((self.largura_quadro, self.altura_quadro))

    def update(self):
        # Atualiza animação apenas se estiver se movendo
        if self.velocidade_x != 0 or self.velocidade_y != 0:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.animacoes[self.estado]):
                self.frame_index = 0
            
            self.image = self.animacoes[self.estado][int(self.frame_index)]
        else:
            # Quando parado, usa o primeiro frame da última direção
            self.image = self.animacoes[self.direcao][0]
        
        # Movimento horizontal e vertical
        self.rect.x += self.velocidade_x
        self.rect.y += self.velocidade_y
        
        # Mantém dentro da tela
        self.rect.x = max(0, min(largura - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(altura - self.rect.height, self.rect.y))

# Inicialização do jogo
personagem = Personagem()
todas_as_sprites = pygame.sprite.Group(personagem)
clock = pygame.time.Clock()
rodando = True
pontuacao = 0
fonte = pygame.font.SysFont(None, 36)

while rodando:
    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
    
    # Controles - agora com todas as direções
    teclas = pygame.key.get_pressed()
    personagem.velocidade_x = 0
    personagem.velocidade_y = 0
    novo_estado = personagem.estado

    if teclas[pygame.K_RIGHT]:
        personagem.velocidade_x = 5
        novo_estado = "direita"
        personagem.direcao = "direita"
    elif teclas[pygame.K_LEFT]:
        personagem.velocidade_x = -5
        novo_estado = "esquerda"
        personagem.direcao = "esquerda"
    elif teclas[pygame.K_UP]:
        personagem.velocidade_y = -5
        novo_estado = "cima"
        personagem.direcao = "cima"
    elif teclas[pygame.K_DOWN]:
        personagem.velocidade_y = 5
        novo_estado = "baixo"
        personagem.direcao = "baixo"
    else:
        # Quando nenhuma tecla está pressionada
        novo_estado = "parado"

    # Atualiza estado e reseta animação se mudar
    if novo_estado != personagem.estado:
        personagem.estado = novo_estado
        personagem.frame_index = 0

    # Atualizações
    todas_as_sprites.update()
    
    # Verificação de colisão com moedas
    for moeda in moedas[:]:
        if personagem.rect.colliderect(moeda):
            moedas.remove(moeda)
            pontuacao += 10
            # Adiciona nova moeda
            moedas.append(pygame.Rect(
                random.randint(0, largura - 15),
                random.randint(0, altura - 15),
                15, 15
            ))
    
    # Renderização
    tela.fill((0, 0, 0))
    todas_as_sprites.draw(tela)
    for moeda in moedas:
        pygame.draw.rect(tela, (255, 255, 0), moeda)
    
    # Mostra pontuação
    texto_pontuacao = fonte.render(f"Pontos: {pontuacao}", True, (255, 255, 255))
    tela.blit(texto_pontuacao, (10, 10))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
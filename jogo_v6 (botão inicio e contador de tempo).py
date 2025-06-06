import pygame
import os
import random

pygame.init()

# Configuração da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo com Spritesheet")

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AMARELO = (255, 255, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)

# Estados do jogo
MENU = 0
JOGANDO = 1
GAME_OVER = 2
estado_jogo = MENU

# Fonte
fonte = pygame.font.SysFont(None, 36)
fonte_grande = pygame.font.SysFont(None, 72)

# Botão de início
botao_inicio = pygame.Rect(largura//2 - 100, altura//2 - 25, 200, 50)
texto_botao = fonte.render("Iniciar Jogo", True, PRETO)

# Tempo inicial (2 minutos e 29 segundos)
tempo_inicial = 2 * 60 + 29  # 2:29 em segundos
tempo_restante = tempo_inicial
ultimo_tempo = pygame.time.get_ticks()

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
            "cima": [
                self.carregar_frame(2, 0),
                self.carregar_frame(2, 1),
                self.carregar_frame(2, 2),
                self.carregar_frame(2, 3)
            ],
            "baixo": [
                self.carregar_frame(0, 0),
                self.carregar_frame(0, 1),
                self.carregar_frame(0, 2),
                self.carregar_frame(0, 3)
            ]
        }
        
        self.estado = "parado"
        self.image = self.animacoes[self.estado][0]
        self.rect = self.image.get_rect(center=(largura//2, altura//2))
        self.velocidade_x = 0
        self.velocidade_y = 0
        self.frame_index = 0
        self.animation_speed = 0.15
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
        if self.velocidade_x != 0 or self.velocidade_y != 0:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.animacoes[self.estado]):
                self.frame_index = 0
            
            self.image = self.animacoes[self.estado][int(self.frame_index)]
        else:
            self.image = self.animacoes[self.direcao][0]
        
        self.rect.x += self.velocidade_x
        self.rect.y += self.velocidade_y
        
        self.rect.x = max(0, min(largura - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(altura - self.rect.height, self.rect.y))

# Inicialização do jogo
personagem = Personagem()
todas_as_sprites = pygame.sprite.Group(personagem)
clock = pygame.time.Clock()
pontuacao = 0

def formatar_tempo(segundos):
    minutos = segundos // 60
    segundos = segundos % 60
    return f"{minutos:02d}:{segundos:02d}"

def reiniciar_jogo():
    global pontuacao, tempo_restante, moedas, estado_jogo
    pontuacao = 0
    tempo_restante = tempo_inicial
    moedas = []
    for _ in range(10):
        moedas.append(pygame.Rect(
            random.randint(0, largura - 15),
            random.randint(0, altura - 15),
            15, 15
        ))
    personagem.rect.center = (largura//2, altura//2)
    estado_jogo = JOGANDO

rodando = True
while rodando:
    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if estado_jogo == MENU and botao_inicio.collidepoint(evento.pos):
                reiniciar_jogo()
            elif estado_jogo == GAME_OVER:
                reiniciar_jogo()
    
    # Atualizações
    if estado_jogo == JOGANDO:
        # Atualiza tempo
        agora = pygame.time.get_ticks()
        if agora - ultimo_tempo >= 1000:  # 1 segundo
            tempo_restante -= 1
            ultimo_tempo = agora
        
        if tempo_restante <= 0:
            estado_jogo = GAME_OVER
        
        # Controles
        teclas = pygame.key.get_pressed()
        personagem.velocidade_x = 0
        personagem.velocidade_y = 0
        novo_estado = personagem.estado

        if teclas[pygame.K_RIGHT]:
            personagem.velocidade_x = 3
            novo_estado = "direita"
            personagem.direcao = "direita"
        elif teclas[pygame.K_LEFT]:
            personagem.velocidade_x = -3
            novo_estado = "esquerda"
            personagem.direcao = "esquerda"
        elif teclas[pygame.K_UP]:
            personagem.velocidade_y = -3
            novo_estado = "cima"
            personagem.direcao = "cima"
        elif teclas[pygame.K_DOWN]:
            personagem.velocidade_y = 3
            novo_estado = "baixo"
            personagem.direcao = "baixo"
        else:
            novo_estado = "parado"

        if novo_estado != personagem.estado:
            personagem.estado = novo_estado
            personagem.frame_index = 0

        todas_as_sprites.update()
        
        # Verificação de colisão com moedas
        for moeda in moedas[:]:
            if personagem.rect.colliderect(moeda):
                moedas.remove(moeda)
                pontuacao += 10
                moedas.append(pygame.Rect(
                    random.randint(0, largura - 15),
                    random.randint(0, altura - 15),
                    15, 15
                ))
    
    # Renderização
    tela.fill(PRETO)
    
    if estado_jogo == MENU:
        # Tela de menu
        titulo = fonte_grande.render("Jogo de Coletar Moedas", True, BRANCO)
        tela.blit(titulo, (largura//2 - titulo.get_width()//2, altura//3))
        
        pygame.draw.rect(tela, VERDE, botao_inicio)
        tela.blit(texto_botao, (botao_inicio.centerx - texto_botao.get_width()//2, 
                               botao_inicio.centery - texto_botao.get_height()//2))
    
    elif estado_jogo == JOGANDO:
        # Jogo em andamento
        todas_as_sprites.draw(tela)
        for moeda in moedas:
            pygame.draw.rect(tela, AMARELO, moeda)
        
        # Mostra pontuação e tempo
        texto_pontuacao = fonte.render(f"Pontos: {pontuacao}", True, BRANCO)
        tela.blit(texto_pontuacao, (10, 10))
        
        tempo_formatado = formatar_tempo(tempo_restante)
        texto_tempo = fonte.render(f"Tempo: {tempo_formatado}", True, BRANCO)
        tela.blit(texto_tempo, (largura - texto_tempo.get_width() - 10, 10))
    
    elif estado_jogo == GAME_OVER:
        # Tela de game over
        mensagem = fonte_grande.render("Fim de Jogo!", True, VERMELHO)
        tela.blit(mensagem, (largura//2 - mensagem.get_width()//2, altura//3))
        
        texto_pontuacao_final = fonte.render(f"Pontuação Final: {pontuacao}", True, BRANCO)
        tela.blit(texto_pontuacao_final, (largura//2 - texto_pontuacao_final.get_width()//2, altura//2))
        
        texto_reiniciar = fonte.render("Clique para jogar novamente", True, BRANCO)
        tela.blit(texto_reiniciar, (largura//2 - texto_reiniciar.get_width()//2, altura*2//3))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
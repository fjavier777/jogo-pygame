import pygame
import sys

pygame.init()

rodar = True #Controla a atividade do jogo. Ou seja, o jogo vai rodar somente enquanto "jogoAtivo" estiver ok. Assim evita que o jogo fique ativo interminavelmente.

WIDTH = 800 #Largura do painel
HEIGHT = 600 #Altura do painel

FPS = 60

clock = pygame.time.Clock()

window = pygame.display.set_mode((WIDTH, HEIGHT))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((60, 30))
        self.image.fill((200, 255, 200))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 30

        self.balls = []

    def update(self):
        self.speedx = 0

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -5

        if keystate[pygame.K_d]:
            self.speedx = 5

        self.rect.x += self.speedx

        if self.rect.right + self.speedx > WIDTH:
            self.rect.right = WIDTH

        if self.rect.left + self.speedx < 0:
            self.rect.left = 0

        #ball = Ball(self.rect.centerx, self.rect.top)
        #for i in all_sprites:
        #    print(i)
        #all_sprites.add(ball)

    def shoot(self):
        ball = Ball(self.rect.centerx, self.rect.top)
        all_sprites.add(ball)

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill((100, 150, 200))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -3

        self.player = None

    def update(self):
        # Move a bola para cima, na velocidade configurada
        self.rect.y += self.speedy

        # Move a bola para a posicao central (no eixo X) do player
        self.rect.centerx = player.rect.centerx

        # Verifica se a bola ja saiu da tela
        if self.rect.centery <= 0:
            all_sprites.remove(self)


all_sprites = pygame.sprite.Group()
balls = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

while rodar:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodar = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    window.fill((0, 0, 30))

    all_sprites.update()
    sys.stdout.write('\rTotal de sprites em jogo: {:5d}'.format(len(all_sprites)))

    all_sprites.draw(window)

    pygame.display.flip()

pygame.quit()
quit()
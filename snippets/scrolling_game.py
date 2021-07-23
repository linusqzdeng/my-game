import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

# set up the frame rate
FPS = 60
FrameperSec = pygame.time.Clock()

# define colours
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)

# display screen's size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
SCREEN.fill(WHITE)
pygame.display.set_caption('Game')

# Enemy speed
SPEED = 10

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('enemy.png')
        self.surf = pygame.Surface((50,80))     # Enemy size
        self.rect = self.surf.get_rect(center=(random.randint(100, 450), 0))
    
    def move(self):
        self.rect.move_ip(0,SPEED)
        if self.rect.bottom >= 600:
            self.rect.top = 0
            self.rect.center = (random.randint(90, 460), 0)

    # def draw(self, surface):
    #     surface.blit(self.image, self.rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('player.png')
        self.surf = pygame.Surface((50,100))    # Player size
        self.rect = self.surf.get_rect(center=(400,550))
    
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5,0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5,0)
    
    # def draw(self, surface):
    #     surface.blit(self.image, self.rect)

# Setting up sprites
P1 = Player()
E1 = Enemy()

# Creating sprites groups
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(E1)
all_sprites.add(P1)

# Adding a new user event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

while True:
    # Cycles through all events occuring
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 2

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    SCREEN.fill(WHITE)

    # Moves and draw all sprites
    for entity in all_sprites:
        SCREEN.blit(entity.image, entity.rect)
        entity.move()

    # Collision detaction
    if pygame.sprite.spritecollideany(P1, enemies):
        SCREEN.fill(RED)
        pygame.display.update()
        for eneity in all_sprites:
            eneity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FrameperSec.tick(FPS)

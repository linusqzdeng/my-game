import pygame
from pygame.locals import *
import sys
import random

# Alwalys at the top
pygame.init()

# 2 dimemsions vector
vec = pygame.math.Vector2

WIDTH = 400
HEIGHT = 450
ACC = 0.5
FRIC = -0.12
FPS = 60

FramPerSec = pygame.time.Clock()

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (45, 163, 215)

# Sprites setting
player_size = (30, 30)
platform_size = (WIDTH, 20)
platform_spot = (WIDTH / 2, HEIGHT - 10)

# Setting up the display surface
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Doodle Jump[Fake]')


# Two classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface(player_size)
        self.surf.fill(SKY_BLUE)
        self.rect = self.surf.get_rect()

        self.pos = vec((10, 385))   # Replace the center param
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.jumping = False    # Define player's jumping posiiton

    # Enabling player to move
    def move(self):
        self.acc = vec(0, 0.5)   # Gravity ---- vertical accelerate

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        # Acceleration and fraction
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + self.acc * 0.5

        # Player can warp the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -15

    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    # Collision detaction
    def updates(self):
        hits = pygame.sprite.spritecollide(P1, platforms, False)
        if P1.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    self.jumping = False


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50, 100), 12))
        self.surf.fill(GREEN)
        self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH - 10),
                                               random.randint(0, HEIGHT - 20)))

    def move(self):
        pass


def plat_gen():
    while len(platforms) < 7:
        width = random.randrange(50, 100)
        p = Platform()
        C = True

        while C:
            p = Platform()
            p.rect.center = (random.randrange(0, WIDTH - width),
                             random.randrange(-50, 0))
            C = check(p, platforms)
        platforms.add(p)
        all_sprites.add(p)


def check(platform, groups):
    if pygame.sprite.spritecollideany(platform, groups):
        return True
    else:
        for entity in groups:
            if entity == platform:
                continue
            if abs(platform.rect.top - entity.rect.bottom) < 50 and abs(platform.rect.bottom - entity.rect.top) < 50:
                return True
            C = False


P1 = Player()
PL1 = Platform()

PL1.surf = pygame.Surface((WIDTH, 20))
PL1.surf.fill(GREEN)
PL1.rect = PL1.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))

# Sprites groups
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(PL1)

platforms = pygame.sprite.Group()
platforms.add(PL1)

# Generaitng initial levle
for x in range(random.randint(5, 6)):
    C = True
    pl = Platform()
    while C:
        pl = Platform()
        C = check(pl, platforms)
    platforms.add(pl)
    all_sprites.add(pl)

# Game loop
while True:
    P1.updates()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # When spacebar is clicked, call the jump(), when keyup, call the cancel_jump()
        if event.type == KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump()
        if event.type == KEYUP:
            if event.key == pygame.K_SPACE:
                P1.cancel_jump()

    # Getting screen moves up when player jumps
    if P1.rect.top <= HEIGHT / 3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top > HEIGHT:
                plat.kill()

    plat_gen()
    SCREEN.fill(BLACK)

    for entity in all_sprites:
        SCREEN.blit(entity.surf, entity.rect)
        entity.move()

    pygame.display.update()
    FramPerSec.tick(FPS)

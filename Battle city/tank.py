import pygame
import os
import sys
from pygame import *

WIDTH = 630
HEIGHT = 630
vec = pygame.math.Vector2


class Tank(pygame.sprite.Sprite):
    SPEED = 2
    DIRECTION = {'UP': vec(0, -1),
                 'DOWN': vec(0, 1),
                 'LEFT': vec(-1, 0),
                 'RIGHT': vec(1, 0)}

    TANK_1_IMGS = pygame.image.load_basic('images/myTank/tank_T1_0.bmp')
    TANK_2_IMGS = pygame.image.load_basic('images/myTank/tank_T2_0.bmp')
    TANK_1_DIR = {'UP': TANK_1_IMGS.subsurface((0, 0), (48, 48)),
                  'DOWN': TANK_1_IMGS.subsurface((0, 48), (48, 48)),
                  'LEFT': TANK_1_IMGS.subsurface((0, 96), (48, 48)),
                  'RIGHT': TANK_1_IMGS.subsurface((0, 144), (48, 48))}
    TANK_2_DIR = {'UP': TANK_2_IMGS.subsurface((0, 0), (48, 48)),
                  'DOWN': TANK_2_IMGS.subsurface((0, 48), (48, 48)),
                  'LEFT': TANK_2_IMGS.subsurface((0, 96), (48, 48)),
                  'RIGHT': TANK_2_IMGS.subsurface((0, 144), (48, 48))}

    def __init__(self, player=1):
        super().__init__()
        # Single- or multi-player mode
        self.player = player
        if self.player == 1:
            self.image = self.TANK_1_IMGS
            self.image_dir = self.TANK_1_DIR
        if self.player == 2:
            self.image = self.TANK_2_IMGS
            self.image_dir = self.TANK_2_DIR

        self.surf = self.image_dir['UP']  # default image "UP"
        self.rect = self.surf.get_rect()
        self.shoot = False

        self.pos = vec(144, 630 - 48)  # spawning position
        self.direction = self.DIRECTION['UP']  # default direction "UP"
        self.vel = vec(0, 0)

        # self.hp = 100
        # self.alive = True
        # self.protected = False

    def move(self):
        """Capture tank's movement."""
        key = pygame.key.get_pressed()
        if key[K_UP]:
            self.direction = self.DIRECTION['UP']
            self.vel = self.SPEED * self.direction
            self.pos += self.vel
        if key[K_DOWN]:
            self.direction = self.DIRECTION['DOWN']
            self.vel = self.SPEED * self.direction
            self.pos += self.vel
        if key[K_LEFT]:
            self.direction = self.DIRECTION['LEFT']
            self.vel = self.SPEED * self.direction
            self.pos += self.vel
        if key[K_RIGHT]:
            self.direction = self.DIRECTION['RIGHT']
            self.vel = self.SPEED * self.direction
            self.pos += self.vel

        self.rect.topleft = self.pos

    def boundary(self):
        """Prevent the tank moving out of the screen."""
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.x > WIDTH - 48:
            self.pos.x = WIDTH - 48
        if self.pos.y < 0:
            self.pos.y = 0
        if self.pos.y > HEIGHT - 48:
            self.pos.y = HEIGHT - 48

        self.rect.topleft = self.pos

    def turn(self, dir):
        """Change the tank image when in terms of its direction."""
        if dir.y < 0:  # move up
            self.surf = self.image_dir['UP']
        if dir.y > 0:  # move down
            self.surf = self.image_dir['DOWN']
        if dir.x < 0:  # move left
            self.surf = self.image_dir['LEFT']
        if dir.x > 0:  # move right
            self.surf = self.image_dir['RIGHT']

        return self.surf

    def collide(self):
        pass

    def update(self):
        global screen

        screen.blit(self.surf, self.rect)
        self.move()
        self.turn(self.direction)
        self.boundary()


class Bullet(pygame.sprite.Sprite):
    BULLET_IMGS = {'UP': pygame.image.load_basic('images/bullet/bullet_up.bmp'),
                   'DOWN': pygame.image.load_basic('images/bullet/bullet_down.bmp'),
                   'LEFT': pygame.image.load_basic('images/bullet/bullet_left.bmp'),
                   'RIGHT': pygame.image.load_basic('images/bullet/bullet_right.bmp')}

    def __init__(self, tank_dir, tank_rect):
        super().__init__()
        self.tank_dir = tank_dir
        self.tank_rect = tank_rect

        self.surf = self.turn(self.tank_dir)
        self.rect = self.surf.get_rect()
        self.shoot = False
        self.speed = 4
        self.vel = self.speed * self.tank_dir
        self.pos = self.start_dir(self.tank_dir, self.tank_rect)

        self.collided = False
        # self.dmg = 100

    def start_dir(self, dir, rect):
        """Change the shooting direction of the bullet while tank is moving."""
        if dir.y < 0:  # upward
            self.pos = vec(rect.midtop)
        if dir.y > 0:  # downward
            self.pos = vec(rect.midbottom)
        if dir.x < 0:  # left forward
            self.pos = vec(rect.midleft)
        if dir.x > 0:  # right forward
            self.pos = vec(rect.midright)

        return self.pos

    def move(self):
        """Capture the bullet movement on screen."""
        self.pos += self.vel
        self.rect.center = self.pos

    def turn(self, dir):
        """Switch image in terms of bullet direction."""
        if dir.y < 0:  # move up
            self.surf = self.BULLET_IMGS['UP']
        if dir.y > 0:  # move down
            self.surf = self.BULLET_IMGS['DOWN']
        if dir.x < 0:  # move left
            self.surf = self.BULLET_IMGS['LEFT']
        if dir.x > 0:  # move right
            self.surf = self.BULLET_IMGS['RIGHT']

        return self.surf

    def update(self):
        self.move()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Battle City')
    clock = pygame.time.Clock()

    # Customised event
    RELOAD = pygame.USEREVENT
    pygame.time.set_timer(RELOAD, 1000)  # max shooting frequency

    # Initialisation
    bullet_sprites = pygame.sprite.Group()
    tank = Tank(player=2)

    over = 0
    while not over:
        clock.tick(60)
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            # Exit and quit the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key in [K_q, K_ESCAPE]):
                over = 1
                pygame.quit()
                sys.exit()

            # Shooting bullet
            if event.type == KEYDOWN and event.key == K_SPACE:
                tank.shoot = True
                bullet = Bullet(tank.direction, tank.rect)
                bullet_sprites.add(bullet)
            if event.type == RELOAD:
                # bullet.collided = False
                pass

        # Game play
        tank.update()

        for bullet in bullet_sprites:  # Draw bullets
            bullet.update()
            screen.blit(bullet.surf, bullet.rect)

            # Remove bullets outside the screen
            if bullet.pos.x < -15 or bullet.pos.x > WIDTH + 15 or \
                    bullet.pos.y < -15 or bullet.pos.y > HEIGHT + 15:
                bullet_sprites.remove(bullet)

        # Update the screen
        pygame.display.update()

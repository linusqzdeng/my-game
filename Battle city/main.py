import pygame
import sys
import os

from tank import Tank, Bullet
from scene import Base, Map
from pygame.locals import *


WIDTH = 624
HEIGHT = 624
BG_IMG = pygame.image.load_basic('images/others/background.bmp')


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Battle City')
    clock = pygame.time.Clock()

    # Customised event
    RELOAD = pygame.USEREVENT
    pygame.time.set_timer(RELOAD, 1000)  # max shooting frequency

    # Initialisation
    # Sprites groups
    bullet_sprites = pygame.sprite.Group()
    tank_sprites = pygame.sprite.Group()

    # Objects
    # Tank
    my_tank = Tank(player=2)
    tank_sprites.add(my_tank)

    # Map
    game_map = Map(stage=1)
    # Base
    base = Base((WIDTH / 2 - 24, HEIGHT - 48))

    # Bricks

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
                my_tank.shoot = True
                bullet = Bullet(my_tank.direction, my_tank.rect)
                bullet_sprites.add(bullet)
            if event.type == RELOAD:
                # bullet.collided = False
                pass

        # Game play

        # Blit objects on screen
        # Base
        screen.blit(base.surf, base.rect)

        # Map
        for block in game_map.all_sprites:
            screen.blit(block.surf, block.rect)

        # Tank
        for tank in tank_sprites:
            tank.update()
            screen.blit(tank.surf, tank.rect)

        # Bullets
        for bullet in bullet_sprites:
            bullet.update()
            screen.blit(bullet.surf, bullet.rect)

            # Remove bullets outside the screen
            if bullet.pos.x < -15 or bullet.pos.x > WIDTH + 15 or \
                    bullet.pos.y < -15 or bullet.pos.y > HEIGHT + 15:
                bullet_sprites.remove(bullet)

        # Update the screen
        pygame.display.update()


if __name__ == "__main__":
    main()

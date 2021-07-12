import pygame
from pygame.locals import *
import sys
import random

# compulsory code line
pygame.init()

# set up the global variables
WIDTH = 800
HEIGHT = 600
player_size = 45
enemy_size = player_size
player_pos = [WIDTH / 2, HEIGHT - 2 * player_size]
enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]

MOVING_STEP = 40
ENEMY_SPEED = 10    # difficulty of the game!
DISPLAY_COLOUR = (0, 0, 0)    # black
PLAYER_COLOUR = (255, 255, 255)   # white
ENEMY_COLOUR = (255, 105, 180)    # pink

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))

# loop for quit the game
game_over = False
FPS = 60
FramePerSec = pygame.time.Clock()


def detact_collision(player_pos, enemy_pos):
    e_x = enemy_pos[0]
    e_y = enemy_pos[1]
    p_x = player_pos[0]
    p_y = player_pos[1]

    if (e_x + enemy_size) >= p_x >= e_x or (p_x + player_size) >= e_x >= p_x:
        if (e_y + enemy_size) >= p_y >= e_y or (p_y + player_size) >= e_y >= p_y:
            return True
    return False


while not game_over:
    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            x = player_pos[0]
            y = player_pos[1]
            if event.key == K_LEFT:
                x -= MOVING_STEP
            elif event.key == K_RIGHT:
                x += MOVING_STEP
            # elif event.key == K_UP:
            #     y -= MOVING_STEP
            # elif event.key == K_DOWN:
            #     y += MOVING_STEP

            player_pos = [x, y]

    DISPLAYSURF.fill(DISPLAY_COLOUR)

    if enemy_pos[1] >= 0 and enemy_pos[1] <= HEIGHT:
        enemy_pos[1] += ENEMY_SPEED
    else:
        enemy_pos[0] = random.randint(0, WIDTH - enemy_size)
        enemy_pos[1] = 0

    # detact collision
    if detact_collision(player_pos, enemy_pos):
        game_over = True
        break

    FramePerSec.tick(FPS)
    pygame.draw.rect(DISPLAYSURF, ENEMY_COLOUR, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))
    pygame.draw.rect(DISPLAYSURF, PLAYER_COLOUR, (player_pos[0] - player_size, player_pos[1], player_size, player_size))
    pygame.display.update()

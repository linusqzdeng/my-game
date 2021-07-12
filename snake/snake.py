import pygame
import random
import sys
from pygame.locals import *


WIDTH = 450
HEIGHT = 450  # define the size of the display window

BLACK = (0, 0, 0)  # define some colours in RGB
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (45, 163, 215)


pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake!")

surface = pygame.Surface(screen.get_size())
surface = surface.convert()

snake_pos = [WIDTH / 2, HEIGHT / 2]

game_over = False

while not game_over:
    clock.tick(10)
    screen.blit(surface, (0, 0))

    for event in pygame.event.get():
        print(event)

        if event.type == pygame.QUIT:  # quit the game when clicking on the close button
            game_over = True
            pygame.quit()
            sys.exit()

    # create the moving funciton of the snake
    key_pressed = pygame.key.get_pressed()

    if key_pressed[K_LEFT]:
        snake_pos[0] -= 10
    elif key_pressed[K_RIGHT]:
        snake_pos[0] += 10

    rect = pygame.draw.rect(surface, RED, (snake_pos[0], snake_pos[1], 10, 10))
    pygame.display.update()

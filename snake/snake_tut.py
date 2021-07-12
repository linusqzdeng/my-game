import pygame
import sys
import random
from pygame.locals import *

WIDTH = 450  # define the size of the window
HEIGHT = 450

GRIDSIZE = 20  # define the size of the grid
GRID_WIDTH = WIDTH / GRIDSIZE
GRID_HEIGHT = HEIGHT / GRIDSIZE

BLACK = (0, 0, 0)  # define some colours in RGB
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (45, 163, 215)

UP = (0, -1)
DOWN = (0, 1)
RIGHT = (1, 0)
LEFT = (-1, 0)


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH / 2), (HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, RIGHT, LEFT])
        self.colour = GREEN

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self,):
        current = self.get_head_position()
        x, y = self.direction


class Food(pygame.sprite.Sprite):
    pass


def main():

    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake!")

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    game_over = False

    while not game_over:
        clock.tick(10)
        screen.blit(surface, (0, 0))  # handle events
        pygame.display.update()

        for event in pygame.event.get():
            print(event)

            if event.type == pygame.QUIT:
                game_over = True


if __name__ == "__main__":
    main()

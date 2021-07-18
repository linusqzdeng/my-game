import pygame
import random
import sys
from pygame.locals import *


WIDTH, HEIGHT = 450, 450

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (45, 163, 215)

snake_size = 10
snake_pos = [WIDTH / 2, HEIGHT / 2]  # spawning position
snake_body = [
    snake_pos,
    [snake_pos[0] - snake_size, snake_pos[1]],
    [snake_pos[0] - 2 * snake_size, snake_pos[1]]
]


def game_over():
    """Call this function when the play lose."""
    pass


class Snake:
    """Enable the snake to move around on screen."""

    def __init__(self, body: list, size: int, color: tuple, screen):
        self.body = body
        self.size = size
        self.screen = screen
        self.color = color
        self.x, self.y = self.body[0]  # head position
        self.direction = random.choice(['Right', 'Left', 'Up', 'Down'])
        self.speed = 5  # difficulty of the game
        self.grow = 0

    def _draw(self):
        """Draw the snake on screen."""
        self.body.insert(0, [self.x, self.y])
        for pos in self.body:
            pygame.draw.rect(self.screen, self.color, (pos[0], pos[1], self.size, self.size))

        # pop the snake tail every frame
        if self.grow:
            self.grow = 0
        else:
            self.body.pop()

    def _move(self):
        """Move the snake in terms of the direction."""
        if self.direction == 'Right':
            self.x += self.speed
        if self.direction == 'Left':
            self.x -= self.speed
        if self.direction == 'Up':
            self.y -= self.speed
        if self.direction == 'Down':
            self.y += self.speed

    def _collision(self):
        """Collision detection."""
        # whether it collides with the edge of the window
        if self.x + self.size >= WIDTH or self.x <= 0 or self.y + self.size >= HEIGHT or self.y <= 0:
            print('Crash into the wall!')
            # game_over()
            sys.exit()

        # whether it collides with itself
        for body in self.body[1:]:
            if self.x == body[0] and self.y == body[1]:
                print('Eat yourself!')
                game_over()
                sys.exit()

    def update(self):
        """Update the snake object."""
        self._collision()
        self._move()
        self._draw()


class Food:
    """Food makes the snake become longer when it is eaten."""

    def __init__(self, size: int, color: tuple, screen):
        self.size = size
        self.color = color
        self.screen = screen
        self.eaten = 0
        self.x = random.randrange(WIDTH - self.size)
        self.y = random.randrange(HEIGHT - self.size)

    def _spawn(self):
        """Spawn the food in randomly on screen."""
        if not self.eaten:
            pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.size, self.size))
        else:
            self.x = random.randrange(WIDTH - self.size)
            self.y = random.randrange(HEIGHT - self.size)

    def _eaten(self, pos: tuple):
        """Change the state to 1 if the food is eaten."""
        self.eaten = 0
        if abs(self.x - pos[0]) <= self.size and abs(self.y - pos[1]) < self.size:
            self.eaten = 1

    def update(self, pos):
        self._spawn()
        self._eaten(pos)


def main():
    # initialising the game
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake!")
    # surface = pygame.Surface(screen.get_size())
    # surface = surface.convert()

    # prepare for game objects
    snake = Snake(snake_body, snake_size, SKY_BLUE, screen)
    food = Food(8, RED, screen)

    # main loop
    over = 0
    while not over:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key in [K_q, K_ESCAPE]):
                over = 1

            # snake's movement
            if (event.type == KEYDOWN and event.key in [K_DOWN, K_s]) and snake.direction != 'Up':
                snake.direction = 'Down'
            elif (event.type == KEYDOWN and event.key in [K_UP, K_w]) and snake.direction != 'Down':
                snake.direction = 'Up'
            elif (event.type == KEYDOWN and event.key in [K_LEFT, K_a]) and snake.direction != 'Right':
                snake.direction = 'Left'
            elif (event.type == KEYDOWN and event.key in [K_RIGHT, K_d]) and snake.direction != 'Left':
                snake.direction = 'Right'

        # expand the snake if the food is eaten
        if food.eaten:
            snake.grow = 1

        # draw the whole screen
        screen.fill(BLACK)
        snake.update()
        food.update((snake.x, snake.y))
        pygame.display.update()


if __name__ == "__main__":
    main()

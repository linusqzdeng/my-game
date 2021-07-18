import pygame
import sys
import random
from pygame.locals import *
from pygame.math import Vector2


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (45, 163, 215)

cell_size = 10
cell_number = 45
WIDTH, HEIGHT = cell_number * cell_size, cell_number * cell_size
snake_body = [Vector2(20, 20), Vector2(21, 20), Vector2(22, 20)]

up = Vector2(0, -1)
down = Vector2(0, 1)
left = Vector2(-1, 0)
right = Vector2(1, 0)


class Snake:
    """Enable the snake to move around on screen."""

    def __init__(self, screen):
        self.screen = screen
        self.body = snake_body
        self.direction = left
        self.grow = 0

    def _draw(self):
        """Draw the snake on screen."""
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            snake_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(self.screen, SKY_BLUE, snake_rect)

    def _move(self):
        """Move the snake in terms of the direction."""
        if not self.grow:
            body_copy = self.body[:-1]  # body excluding the tail
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
        else:
            self.body.insert(0, self.body[0] + self.direction)
            self.grow = 0

    def _collision(self):
        """Collision detection."""
        # whether it collides with the edge of the window
        head_pos = self.body[0]
        if head_pos.x * cell_size > WIDTH or head_pos.x < 0 or head_pos.y * cell_size > HEIGHT or head_pos.y < 0:
            print('Crash into the wall!')
            sys.exit()

        # whether it collides with itself
        for block in self.body[1:]:
            if head_pos.x == block.x and head_pos.y == block.y:
                print('Eat yourself!')
                sys.exit()

    def update(self):
        """Update the snake object."""
        self._collision()
        self._draw()
        self._move()


class Food:
    """Food makes the snake become longer when it is eaten."""

    def __init__(self, screen):
        self.screen = screen
        self.eaten = 0
        self.x, self.y = self._randomise()

    def _randomise(self):
        """Spawn the food in randomly on screen."""
        self.x = random.randrange(cell_number - 1)
        self.y = random.randrange(cell_number - 1)

        return self.x, self.y

    def _spawn(self):
        if not self.eaten:
            pos_x = int(self.x * cell_size)
            pos_y = int(self.y * cell_size)
            food_rect = pygame.Rect(pos_x, pos_y, cell_size, cell_size)
            pygame.draw.rect(self.screen, RED, food_rect)
        else:
            self.x, self.y = self._randomise()

    def update(self):
        self._spawn()


class Main:
    """Main control of the game."""

    def __init__(self, screen):
        self.screen = screen
        self.snake = Snake(self.screen)
        self.food = Food(self.screen)
        self.score = 0

    def scores(self):
        if self.snake_grow():
            self.score += 10
            print(self.score)

    def snake_grow(self):
        if self.food.eaten:
            self.snake.grow = 1
            return 1  # for scores()

    def food_eaten(self):
        self.food.eaten = 0
        if self.snake.body[0].x == self.food.x and self.snake.body[0].y == self.food.y:
            self.food.eaten = 1

    def update(self):
        self.snake_grow()
        self.food_eaten()
        self.scores()
        self.snake.update()
        self.food.update()


def main():
    # initialising the game
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    main_game = Main(screen)

    # main loop
    over = 0
    while not over:
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key in [K_q, K_ESCAPE]):
                over = 1

            # snake's movement
            if event.type == KEYDOWN:
                if event.key in [K_DOWN, K_s] and main_game.snake.direction != up:
                    main_game.snake.direction = down
                if event.key in [K_UP, K_w] and main_game.snake.direction != down:
                    main_game.snake.direction = up
                if event.key in [K_LEFT, K_a] and main_game.snake.direction != right:
                    main_game.snake.direction = left
                if event.key in [K_RIGHT, K_d] and main_game.snake.direction != left:
                    main_game.snake.direction = right

        # draw the whole screen
        screen.fill(BLACK)
        main_game.update()
        pygame.display.update()


if __name__ == "__main__":
    main()

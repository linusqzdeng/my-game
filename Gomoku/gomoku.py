# Game: Gomoku (Five-in-a-row)
# Author: Qizhong Deng

import sys
import numpy as np
import pygame
from pygame.locals import *

WIDTH = 855
HEIGHT = 855
CELL = 45


class Colour:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BOARD = (255, 153, 51)


class Board:
    def __init__(self):
        self.size = 15
        self.start = CELL * 2
        self.end = CELL * 2 + CELL * (self.size - 1)
        self.panel = np.zeros((self.size, self.size))

    def draw(self, screen):
        """A 15 * 15 rectangle, with 15 lines and 14 cells."""
        # Grid
        for i in range(self.size):
            pygame.draw.line(
                screen, Colour.BLACK, (self.start, self.start + CELL * i), (self.end, self.start + CELL * i), 2
            )
            pygame.draw.line(
                screen, Colour.BLACK, (self.start + CELL * i, self.start), (self.start + CELL * i, self.end), 2
            )

        # Dots
        dots_pos = [
            (self.start + CELL * 3, self.start + CELL * 3),
            (self.start + CELL * 11, self.start + CELL * 3),
            (self.start + CELL * 3, self.start + CELL * 11),
            (self.start + CELL * 11, self.start + CELL * 11),
            (self.start + CELL * 7, self.start + CELL * 7),
        ]
        for dot in dots_pos:
            pygame.draw.circle(screen, Colour.BLACK, dot, 8)


class Stone:
    def __init__(self):
        self.r = CELL // 2  # radius
        self.black = []
        self.white = []
        self.player = 1

    def window_pos(self):
        """Returns the stone coordinator within the window."""
        # Board coordinator for stones
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Make sure x ordinate is on the grid
        if mouse_x % CELL > (CELL / 2):
            self.x = (mouse_x - mouse_x % CELL) + CELL
        else:
            self.x = mouse_x - (mouse_x % CELL)

        # Make sure y ordinate is on the grid
        if mouse_y % CELL > (CELL / 2):
            self.y = (mouse_y - mouse_y % CELL) + CELL
        else:
            self.y = mouse_y - (mouse_y % CELL)

        return self.x, self.y

    def grid_pos(self, start):
        """Changes window coordinator into grid coordinator."""
        self.grid_x = (self.x - start) // CELL  # x coordinator measured in grid
        self.grid_y = (self.y - start) // CELL  # y coordinator measured in grid

        return self.grid_x, self.grid_y

    def place(self, board, start, end, x, y):
        """Append the placing stone into its correpsonded list."""
        if (end >= x >= start) and (end >= y >= start):
            if self.player == 1 and (x, y) not in (set(self.black) | set(self.white)):
                self.black.append((x, y))
                board[self.grid_y][self.grid_x] = 1  # 1 stands for black stone
                self.switch()

            elif self.player == 2 and (x, y) not in (set(self.black) | set(self.white)):
                self.white.append((x, y))
                board[self.grid_y][self.grid_x] = 2  # 2 stands for white stone
                self.switch()

    def draw(self, screen, black, white):
        """Draw all of the stones within the list."""
        for stone in set(black):
            pygame.draw.circle(screen, Colour.BLACK, stone, CELL // 2)

        for stone in set(white):
            pygame.draw.circle(screen, Colour.WHITE, stone, CELL // 2)

    def switch(self):
        """Switch player after each move."""
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    def last_palced(self, player, screen):
        """
        Using a red dot in the center of stone to indicate
        the previous stone placed.
        """
        if (len(self.black) + len(self.white)) >= 1:
            if player == 1:
                pygame.draw.circle(screen, Colour.RED, self.white[-1], 5)

            if player == 2:
                pygame.draw.circle(screen, Colour.RED, self.black[-1], 5)


class Player:
    def __init__(self):
        pass

    def winner(self, board, x, y, n=5):
        """
        Detect and return the winner. Winner comes out when there are five
        stones in the same colour in a row, column or diagonal. After each
        move, detect whether the centre stone and the 4 other stones surrounding
        have the same colour.
        """
        end = len(board)
        stone = board[y][x]

        def check(values):
            counter = 0
            for value in values:
                if value == stone:
                    counter += 1
                else:
                    counter = 0

                if counter == n:
                    return True

            return False

        # Five stones in horizontal
        if check(board[y][i] for i in range(max(0, x - n + 1), min(end, x + n))):
            return True

        # Five stones in vertical
        if check(board[i][x] for i in range(max(0, y - n + 1), min(end, y + n))):
            return True

        # Five stones in top-left to bottom-right diagonal
        if check(board[y + i][x + i] for i in range(max(-x, -y, 1 - n), min(end - x, end - y, n))):
            return True

        # Five stones in bottom-left to top-right diagonal
        if check(board[y - i][x + i] for i in range(max(-x, y - end + 1, 1 - n), min(end - x, y + 1, n))):
            return True

        return False

    def message(self, board, x, y):
        """Display message when winner comes out."""
        if board[y][x] == 1:
            print("Congrat! Black stone wins the game!")

        if board[y][x] == 2:
            print("Congrat! White stone wins the game!")


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Gomoku")
    clock = pygame.time.Clock()

    # Initialise game objects
    board = Board()
    stone = Stone()
    player = Player()

    over = 0
    is_win = False
    while not over:
        clock.tick(10)
        screen.fill(Colour.BOARD)

        # Event detection
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key in [K_q, K_ESCAPE]):
                over = 1
                pygame.quit()
                sys.exit()

            if pygame.mouse.get_pressed()[0]:
                stone.window_pos()
                stone.grid_pos(board.start)
                stone.place(board.panel, board.start, board.end, stone.x, stone.y)
                is_win = player.winner(board.panel, stone.grid_x, stone.grid_y)

            if is_win:
                player.message(board.panel, stone.grid_x, stone.grid_y)
                is_win = False

            if is_win and (event.type == KEYDOWN and event.key == K_r):
                # Restart the game
                print("Start over another round!")
                board.panel = np.zeros((15, 15))
                stone.black.clear()
                stone.white.clear()
                stone.player = 1

        # Drawing objects
        board.draw(screen)
        stone.draw(screen, stone.black, stone.white)
        stone.last_palced(stone.player, screen)

        pygame.display.update()


if __name__ == "__main__":
    main()

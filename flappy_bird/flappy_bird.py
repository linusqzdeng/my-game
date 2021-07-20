import pygame
import sys
import os
import random
from pygame.locals import *
from pygame.math import Vector2


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH, HEIGHT = 288, 512


class Bird:
    """Flappy bird."""

    def __init__(self):
        self.midflap_surf, self.rect = Game.load_image("bluebird-midflap.bmp", BLACK)
        self.downflap_surf, _ = Game.load_image("bluebird-downflap.bmp", BLACK)
        self.upflap_surf, _ = Game.load_image("bluebird-upflap.bmp", BLACK)
        self.rect.center = (100, 256)
        self.gravity = 0.15
        self.vel = 0
        self.fall = 1
        self.index = 0

    def flap(self):
        if not self.fall:
            self.rect.centery += -30
            self.fall = 1
            self.vel = 0

    def move(self):
        if self.fall:
            self.vel += self.gravity
            self.rect.centery += self.vel

    def rotate(self, old_surf):
        self.new_surf = pygame.transform.rotozoom(old_surf, (4 - self.vel) * 7, 1)
        return self.new_surf

    def animation(self):
        bird_frames = [self.midflap_surf, self.downflap_surf, self.upflap_surf]
        self.surf = bird_frames[self.index]


class Pipe:
    """Obstacles that prevent the bird flying through."""

    def __init__(self):
        self.surf, _ = Game.load_image("pipe-green.bmp", WHITE)
        self.gap = 100
        self.height = [150, 200, 250, 300, 350]
        self.pipes = []

    def move(self, pipes):
        for pipe in pipes:
            pipe.centerx += -1

    def remove(self, pipes):
        for pipe in pipes:
            if pipe.centerx < -30:
                pipes.remove(pipe)

    def create(self):
        random_height = random.choice(self.height)
        self.bottom_rect = self.surf.get_rect(topleft=(300, random_height))
        self.top_rect = self.surf.get_rect(bottomleft=(300, random_height - self.gap))

        return self.bottom_rect, self.top_rect


class Game:
    """Manage to load images and display them."""

    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.background, _ = Game.load_image("background-day.bmp")  # don't need background rect
        self.floor, _ = Game.load_image("base.bmp")  # don't need floor rect
        self.floor_pos = Vector2(0, 450)

        self.bird = Bird()
        self.pipe = Pipe()

    def init_game(self):
        pygame.init()
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.SPAWNPIPES = pygame.USEREVENT
        self.BIRDFLAP = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SPAWNPIPES, 2800)  # draw pipes every 2.8s
        pygame.time.set_timer(self.BIRDFLAP, 200)  # change bird surf every 0.2s

    @staticmethod
    def load_image(filename, colorkey=None):
        """Load the image and return (surface, rect)."""
        fullname = os.path.join("data", filename)
        image = pygame.image.load(fullname).convert()

        # any pixel that is different from black would be transparent
        if colorkey is not None:
            image.set_colorkey(colorkey)

        return image, image.get_rect()

    def move_floor(self):
        """Move the floor constantly, reset the position when it reaches its end."""
        self.floor_pos.x += -1
        if self.floor_pos.x <= -336:
            self.floor_pos.x = 0

    def draw_pipes(self, pipes):
        """Flip the top pipes upside down and draw all pipes."""
        for pipe in pipes:
            if pipe.bottom < 400:
                flip_pipe = pygame.transform.flip(self.pipe.surf, False, True)  # flip the pipe upside down
                self.screen.blit(flip_pipe, pipe)
            else:
                self.screen.blit(self.pipe.surf, pipe)

    def pipes_collide(self, pipes):
        """Detect if the bird and the pipes collide with each other."""
        for pipe in pipes:
            if self.bird.rect.colliderect(pipe):
                return 1
        return 0

    def screen_collide(self):
        """Detect if the bird flies outside the screen."""
        if self.bird.rect.top < -100 or self.bird.rect.bottom > 450:
            return 1

    def deal_events(self):
        """Events detection."""
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key in [K_q, K_ESCAPE]):
                OVER = 1
                pygame.quit()
                sys.exit()
            # bird flapping
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.bird.fall = 0
            # bird animation
            if event.type == self.BIRDFLAP:
                self.bird.index += 1
                if self.bird.index > 2:
                    self.bird.index = 0  # rotate the bird frames
            # spawn pipes
            if event.type == self.SPAWNPIPES:
                self.pipe.pipes.extend(self.pipe.create())
                print(self.pipe.pipes)

    def start(self):
        # initialise the game
        self.init_game()

        # main loop
        OVER = 0
        while not OVER:
            self.clock.tick(60)

            # events detection
            self.deal_events()

            # display background
            self.screen.blit(self.background, (0, 0))

            # move and draw the pipes
            self.pipe.create()
            self.pipe.move(self.pipe.pipes)
            self.pipe.remove(self.pipe.pipes)
            self.draw_pipes(self.pipe.pipes)

            # floor movement
            self.move_floor()
            self.screen.blit(self.floor, self.floor_pos)
            self.screen.blit(self.floor, self.floor_pos + Vector2(336, 0))

            # bird behaviours
            self.bird.move()
            self.bird.flap()
            self.bird.animation()
            self.bird.rotate_bird = self.bird.rotate(self.bird.surf)
            self.screen.blit(self.bird.rotate_bird, self.bird.rect)

            # collision detection
            if self.pipes_collide(self.pipe.pipes) or self.screen_collide():
                OVER = 1
                pygame.quit()
                sys.exit()

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.start()

import pygame
import os


L_GRID = 48
S_GRID = 24


class Base(pygame.sprite.Sprite):
    BASE_IMGS = [pygame.image.load_basic('images/home/home1.bmp'),
                 pygame.image.load_basic('images/home/home2.bmp'),
                 pygame.image.load_basic('images/home/home_destroyed.bmp')]

    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.surf = self.BASE_IMGS[0]
        self.rect = self.surf.get_rect()
        self.rect.topleft = self.pos

        # States
        self.safe = True
        self.hp = 500

    def destroyed(self):
        if self.hp <= 0:
            self.safe = False

    def dead_img(self):
        if not self.safe:
            self.surf = self.BASE_IMGS[2]

    def update(self):
        self.destroyed()
        self.dead_img()


class Brick(pygame.sprite.Sprite):
    SMALL_BRICK = pygame.image.load_basic('images/scene/brick.bmp')  # 24*24
    BIG_BRICK = pygame.image.load_basic('images/scene/big_brick.bmp')  # 48*48

    def __init__(self, size: str):
        super().__init__()
        # Alter the size of the brick
        if size == 'small'.lower():
            self.surf = self.SMALL_BRICK
        elif size == 'big'.lower():
            self.surf = self.BIG_BRICK
        else:
            raise ValueError

        self.rect = self.surf.get_rect()

        # States
        self.breakable = True
        self.is_broken = False


class Ice(pygame.sprite.Sprite):
    pass


class Iron(pygame.sprite.Sprite):
    SMALL_IRON = pygame.image.load_basic('images/scene/iron.bmp')  # 24*24
    BIG_IRON = pygame.image.load_basic('images/scene/big_iron.bmp')  # 48*48

    def __init__(self, size: str):
        super().__init__()
        if size == 'small'.lower():
            self.surf = self.SMALL_IRON
        elif size == 'big'.lower():
            self.surf = self.BIG_IRON
        else:
            raise ValueError

        self.rect = self.surf.get_rect()

        # States
        self.breakable = False
        self.is_broken = False


class River(pygame.sprite.Sprite):
    pass


class Tree(pygame.sprite.Sprite):
    pass


class Tile:
    LEVELFILES = sorted(os.listdir(os.path.join(os.getcwd(), 'levels')))
    LEVELFILES_PATH = [os.path.join(os.getcwd(), 'levels', file) for file in LEVELFILES]

    def __init__(self, stage):
        # Sprites groups
        # self.brick_sprites = pygame.sprite.Group()
        # self.ice_sprites = pygame.sprite.Group()
        # self.iron_sprites = pygame.sprite.Group()
        # self.river_sprites = pygame.sprite.Group()
        # self.tree_sprites = pygame.sprite.Group()

        self.all_sprites = pygame.sprite.Group()
        self.level_file = self.LEVELFILES_PATH[stage - 1]
        self.load_stage_comps()

    def load_stage_comps(self):
        with open(self.level_file, 'r') as file:
            for j, line in enumerate(file.readlines()):  # j is the row number
                line = line.strip('\n')
                print(line)

                # Ignore the comments symblised as "#"
                if line.startswith('#'):
                    continue
                # Ignore the params for the time being
                elif line.startswith('%'):
                    continue
                # Tiles components
                else:
                    j -= 13  # for ignoring the previous 13 lines
                    for i, tile in enumerate(line.split(' ')):  # i is the col number
                        if tile == 'S':
                            continue
                        elif tile == 'B':  # Brick
                            self.brick = Brick(size='small')
                            self.brick.rect.x = S_GRID * i
                            self.brick.rect.y = S_GRID * j
                            self.all_sprites.add(self.brick)
                        elif tile == 'I':  # Iron
                            self.iron = Iron(size='small')
                            self.iron.rect.x = S_GRID * i
                            self.iron.rect.y = S_GRID * j
                            self.all_sprites.add(self.iron)
                        elif tile == 'C':  # Ice
                            pass
                        elif tile == 'R':  # River
                            pass
                        elif tile == 'T':  # Tree
                            pass
                        else:
                            pass

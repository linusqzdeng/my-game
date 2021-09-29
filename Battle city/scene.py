import pygame


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

    def __init__(self, size):
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


class Map:
    def __init__(self, stage):
        # Sprites groups
        # self.brick_sprites = pygame.sprite.Group()
        # self.ice_sprites = pygame.sprite.Group()
        # self.iron_sprites = pygame.sprite.Group()
        # self.river_sprites = pygame.sprite.Group()
        # self.tree_sprites = pygame.sprite.Group()

        self.all_sprites = pygame.sprite.Group()

        # Initialise the stage
        if stage == 1:
            self.stage_1()
        if stage == 2:
            self.stage_2()

    def stage_1(self):
        # Positions of bricks
        # Small bricks
        for i in [0, 1, 24, 25]:
            for j in [14]:
                self.brick = Brick(size='small')
                self.brick.rect.x = S_GRID * i
                self.brick.rect.y = S_GRID * j
                self.all_sprites.add(self.brick)

        for i in [11, 12, 13, 14]:
            for j in [23]:
                self.brick = Brick(size='small')
                self.brick.rect.x = S_GRID * i
                self.brick.rect.y = S_GRID * j
                self.all_sprites.add(self.brick)

        for i in [11, 14]:
            for j in [24, 25]:
                self.brick = Brick(size='small')
                self.brick.rect.x = S_GRID * i
                self.brick.rect.y = S_GRID * j
                self.all_sprites.add(self.brick)

        # Big bricks
        for i in [1, 3, 9, 11]:
            for j in set(range(1, 6)) | set(range(9, 12)):
                self.brick = Brick(size='big')
                self.brick.rect.x = L_GRID * i
                self.brick.rect.y = L_GRID * j
                self.all_sprites.add(self.brick)

        for i in [5, 7]:
            for j in [1, 2, 3, 4, 6, 8, 9, 10]:
                self.brick = Brick(size='big')
                self.brick.rect.x = L_GRID * i
                self.brick.rect.y = L_GRID * j
                self.all_sprites.add(self.brick)

        for i in [2, 3, 9, 10]:
            for j in [7]:
                self.brick = Brick(size='big')
                self.brick.rect.x = L_GRID * i
                self.brick.rect.y = L_GRID * j
                self.all_sprites.add(self.brick)

        for i in [6]:
            for j in [8.5]:
                self.brick = Brick(size='big')
                self.brick.rect.x = L_GRID * i
                self.brick.rect.y = L_GRID * j
                self.all_sprites.add(self.brick)

        # Positions of iron
        # Small iron
        for i in [0, 1, 24, 25]:
            for j in [15]:
                self.iron = Iron(size='small')
                self.iron.rect.x = S_GRID * i
                self.iron.rect.y = S_GRID * j
                self.all_sprites.add(self.iron)

        # Big iron
        for i in [6]:
            for j in [3]:
                self.iron = Iron(size='big')
                self.iron.rect.x = L_GRID * i
                self.iron.rect.y = L_GRID * j
                self.all_sprites.add(self.iron)

    def stage_2(self):
        pass

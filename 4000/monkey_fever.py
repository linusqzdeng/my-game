import pygame
import os
from pygame.locals import *


def load_image(name, colorkey=None):
    fullname = os.path.join(
        "/opt/homebrew/Caskroom/miniforge/base/envs/py4fun/lib/python3.8/site-packages/pygame/examples/data/", name
    )

    try:
        image = pygame.image.load(fullname)
    except pygame.error as msg:
        print("Cannot load image:", name)
        raise SystemExit + msg

    image = image.convert()  # convert the image format to match the display
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)

    return image, image.get_rect()


def load_sound(name):
    # return a dummy class if pygame.mixer() module is not imported properly
    class NoneSound:
        def play(self):
            pass
    if not pygame.mixer.Sound:
        return NoneSound()

    fullname = os.path.join(
        "/opt/homebrew/Caskroom/miniforge/base/envs/py4fun/lib/python3.8/site-packages/pygame/examples/data/", name
    )
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as msg:
        raise SystemExit + msg

    return sound


class Fist(pygame.sprite.Sprite):
    """Move a fist in the screen following the mouse position."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call pygame sprite initialiser
        self.image, self.rect = load_image("fist.bmp", -1)
        self.punching = 0

    def update(self):
        """Move the fist based on mouse position."""
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        if self.punching:
            self.rect.move_ip(5, 10)  # move fist position in place

    def punch(self, target):
        """Return true if the fist puch the target."""
        if not self.punching:
            self.punching = 1
            hitbox = self.rect.inflate(-5, 5)
            return hitbox.colliderect(target.rect)

    def unpunch(self):
        self.punching = 0


class Chimp(pygame.sprite.Sprite):
    """
    Move a monkey across the screen, spin it for a while
    when it is punched.
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("chimp.bmp", -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()  # an area that is as big as the screen
        self.rect.topleft = (10, 10)
        self.move = 9
        self.dizzy = 0  # 1 if the monkey has been punched

    def update(self):
        """Walk or spin, depending on the state of the monkey."""
        if self.dizzy:
            self._spin()
        else:
            self._walk()

    def _spin(self):
        """Spin the monkey when it is punched."""
        center = self.rect.center
        self.dizzy += 12  # rotate 12 degree clockwise

        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original  # reset the image to its original ones after rotated
        else:
            self.image = pygame.transform.rotate(self.original, self.dizzy)

        self.rect = self.image.get_rect()
        self.rect.center = center  # make sure the image would not move when spinning

    def _walk(self):
        """Move the monkey across the scree, turnaround when it reaches the end."""
        new_pos = self.rect.move((self.move, 0))  # move 9 pixel to the right per frame
        if self.rect.left < self.area.left or self.rect.right > self.area.right:
            self.move = -self.move  # move to the opposite direction when the chimp position exceeds the screen
            new_pos = self.rect.move((self.move, 0))
            self.image = pygame.transform.flip(
                self.image, 1, 0
            )  # mirror the chimp to make it looks like turning around
        self.rect = new_pos

    def punched(self):
        """Cause the monkey to start spinning."""
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image


def main():
    # initialising the game
    pygame.init()
    screen = pygame.display.set_mode((468, 60))
    pygame.display.set_caption("Monkey Fever")
    pygame.mouse.set_visible(0)  # disable mouse apperance on screen
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # preparing the game object
    # whiff_sound = load_sound("whiff.wav")
    # punch_sound = load_sound("punch.wav")
    chimp = Chimp()
    fist = Fist()
    all_sprites = pygame.sprite.RenderPlain((fist, chimp))  # sprite Group
    clock = pygame.time.Clock()

    # main loop
    while True:
        clock.tick(60)

        # event detaction
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == MOUSEBUTTONDOWN:
                if fist.punch(chimp):
                    # punch_sound.play()  # punch
                    chimp.punched()
                else:
                    # whiff_sound.play()  # miss
                    pass
            elif event.type == MOUSEBUTTONUP:
                fist.unpunch()

        # update all the sprites
        all_sprites.update()

        # draw all the entire screen
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)  # erase everything from the last frame
        pygame.display.flip()


if __name__ == "__main__":
    main()

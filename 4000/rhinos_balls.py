import pygame
from pygame.locals import *


display_flag = DOUBLEBUF
WIDTH, HEIGHT = 640, 480


def render_ball_simple(radius, color):
    """
    Returns (surf, rect) contains the picture
    of a circle with color given.
    """
    size = 2 * radius
    surf = pygame.Surface((size, size))
    pygame.draw.circle(surf, color, (radius, radius), radius)

    return surf, surf.get_rect()


def render_ball_funky(radius, color):
    """
    Returns (surf, rect) contains the picture
    of a slightly shaded ball of the radius with
    color given.
    """
    size = 2 * radius
    surf = pygame.Surface((size, size))

    # progressively draw smaller circles of different colors
    increment = radius // 4
    for x in range(4):
        iradius = radius - x * increment

        # if it is larger than 255, make it to 255
        icolor = [min(color[i] + x * 15, 255) for i in range(len(color))]
        pygame.draw.circle(surf, icolor, (radius, radius), iradius)

    return surf, surf.get_rect()


def render_ball(radius, color):
    """
    Returns (surf, rect) contains the picture of circles
    with color given. Use the funky one in this case.
    """
    return render_ball_funky(radius, color)


def is_collide(mask_a, mask_b, rect_a, rect_b):
    """Returns True if two rects are collided."""
    x_offset = rect_a[0] - rect_b[0]
    y_offset = rect_a[1] - rect_b[1]
    overlap = mask_a.overlap(mask_b, (x_offset, y_offset))

    return True if overlap else False


def main():
    pygame.init()

    if pygame.display.mode_ok((WIDTH, HEIGHT), flags=display_flag):
        screen = pygame.display.set_mode((WIDTH, HEIGHT), display_flag)

    clock = pygame.time.Clock()

    # draw balls on the surface
    ball1, ball1_rect = render_ball_simple(10, (50, 200, 200))
    ball2, ball2_rect = render_ball_funky(6, (50, 200, 200))

    # move the simple balls to the top center of the screen
    ball1_rect.x = 200

    over = 0
    while not over:
        events = pygame.event.get()

        for event in events:
            if event.type == QUIT or (event.type == KEYDOWN and event.key in [K_q, K_ESCAPE]):
                over = 1

        # add game play here
        screen.blit(ball1, ball1_rect)
        screen.blit(ball2, ball2_rect)

        pygame.display.flip()
        clock.tick(40)


if __name__ == "__main__":
    main()

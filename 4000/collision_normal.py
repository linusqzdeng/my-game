import pygame
from pygame.locals import *


def collision_normal(left_mask, right_mask, left_pos, right_pos):
    """
    Calculates the collision normal when two objects are collided
    """
    def vadd(x, y):
        """Vector adding"""
        return (x[0] + y[0], x[1] + y[1])

    def vsub(x, y):
        """Vector substraction"""
        return (x[0] - y[0], x[1] - y[1])

    def vdot(x, y):
        """Vector dot multiplication"""
        return (x[0] * y[0], x[1] * y[1])

    offset = list(map(int, vsub(left_pos, right_pos)))
    overlap = left_mask.overlap_area(right_mask, offset)

    if overlap == 0:
        return

    # calculate collision normal
    dx = (left_mask.overlap_area(right_mask, (offset[0] + 1, offset[1])) - left_mask.overlap_area(right_mask, offset[0] - 1, offset[1]))
    dy = (left_mask.overlap_area(right_mask, (offset[0], offset[1] + 1)) - left_mask.overlap_area(right_mask, offset[0], offset[1] - 1))

    if dx == 0 and dy == 0:  # one sprite is inside another
        return

    n = (dx, dy)

    return n

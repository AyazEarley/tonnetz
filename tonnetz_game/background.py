import pygame
import math

def lerp_color(color_a, color_b, t): 
    return tuple(a + (b - a) * t for a, b in zip(color_a, color_b))

def create_tilted_gradient(width, height, color_a, color_b, angle=12):
    """Builds a diagonal gradient surface tilted by `angle` degrees,
    sized to fully cover a (width, height) screen after rotation."""
    # make the source strip long enough that after rotating, it still
    # covers the whole screen with no gaps at the corners
    diag = int(math.hypot(width, height)) + 100

    # a 1px-tall gradient row, then stretch it into a tall band
    strip = pygame.Surface((diag, 1))
    for x in range(diag):
        t = x / (diag - 1)
        color = lerp_color(color_a, color_b, t)
        strip.set_at((x, 0), tuple(int(c) for c in color))
    strip = pygame.transform.scale(strip, (diag, diag))

    rotated = pygame.transform.rotate(strip, angle)

    # crop the centered width x height region out of the rotated band
    crop_rect = pygame.Rect(0, 0, width, height)
    crop_rect.center = rotated.get_rect().center

    result = pygame.Surface((width, height))
    result.blit(rotated, (0, 0), area=crop_rect)
    return result
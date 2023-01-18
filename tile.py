import pygame
from getting_data import get_frames


class Tile(pygame.sprite.Sprite):
    def __init__(self, groups: list,
                 size, x, y):
        super().__init__(*groups)
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, shift=0):
        self.rect.x += shift


class StaticTile(pygame.sprite.Sprite):
    def __init__(self, groups: list,
                 x, y, surface):
        super().__init__(*groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, shift=0):
        self.rect.x += shift

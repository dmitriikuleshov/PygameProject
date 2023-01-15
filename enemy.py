import pygame
from settings import *
from getting_data import get_frames


class EnemyBald(pygame.sprite.Sprite):
    def __init__(self, groups: list, x, y):
        super().__init__(*groups)
        self.path = 'data2/graphics/Sprites1/enemies/Sprites/2-Enemy-Bald Pirate/2-Run'
        self.frames = get_frames(self.path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.speed = 1

    def move(self):
        self.rect.x += self.speed

    def reverse(self):
        self.speed *= -1

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)

    def update(self, shift=0):
        self.animate()
        self.move()
        self.rect.x += shift


class EnemyBig(pygame.sprite.Sprite):
    def __init__(self, groups: list, x, y):
        super().__init__(*groups)
        self.path = 'data2/graphics/Sprites1/enemies/Sprites/4-Enemy-Big Guy/2-Run'
        self.frames = get_frames(self.path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.speed = 1

    def move(self):
        self.rect.x += self.speed

    def reverse(self):
        self.speed *= -1

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)

    def update(self, shift=0):
        self.animate()
        self.move()
        self.rect.x += shift

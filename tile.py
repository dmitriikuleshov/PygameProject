import random
import pygame
from settings import *
from getting_data import get_frames


class Tile(pygame.sprite.Sprite):
    def __init__(self, groups: list,
                 size, x, y):
        super().__init__(*groups)
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, shift=0):
        self.rect.x += shift


class KillBox(pygame.sprite.Sprite):
    def __init__(self, groups: list,
                 size, x, y):
        super().__init__(*groups)
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y - 5))

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


class Platform(pygame.sprite.Sprite):
    def __init__(self, groups: list,
                 x, y, surface):
        super().__init__(*groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=(x, y), height=25)

    def update(self, shift=0):
        self.rect.x += shift


class Barrel(pygame.sprite.Sprite):
    def __init__(self, groups: list,
                 size, x, y):
        super().__init__(*groups)
        self.image = pygame.transform.scale(
            pygame.image.load('data2/graphics/Sprites1/Merchant Ship/Sprites/Barrel/Idle/2.png'
                              ), (TILE_SIZE - 10, TILE_SIZE - 10)).convert_alpha()
        self.rect = self.image.get_rect(bottomleft=(x, y + size))

    def update(self, shift=0):
        self.rect.x += shift


class Bottle(pygame.sprite.Sprite):
    def __init__(self, groups: list,
                 size, x, y, path):
        super().__init__(*groups)
        self.image = pygame.transform.scale(
            pygame.image.load(path), (TILE_SIZE, TILE_SIZE)).convert_alpha()
        self.rect = self.image.get_rect(bottomleft=(x, y + size + 5))

    def update(self, shift=0):
        self.rect.x += shift


class Chest(pygame.sprite.Sprite):
    def __init__(self, groups: list,
                 size, x, y):
        super().__init__(*groups)
        self.image = pygame.image.load('data2/graphics/Sprites1/Merchant Ship/Sprites/Chest/Idle/2.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE - 12))
        self.rect = self.image.get_rect(bottomleft=(x, y + size))

    def update(self, shift=0):
        self.rect.x += shift


class Table(pygame.sprite.Sprite):
    def __init__(self, groups: list,
                 size, x, y):
        super().__init__(*groups)
        self.image = pygame.transform.scale(
            pygame.image.load('data2/graphics/Sprites1/enemies/Sprites/7-Objects/12-Other Objects/Table.png'
                              ), (TILE_SIZE, TILE_SIZE - 15)).convert_alpha()
        self.rect = self.image.get_rect(bottomleft=(x, y + size + 5))

    def update(self, shift=0):
        self.rect.x += shift


class Door(pygame.sprite.Sprite):
    def __init__(self, groups: list,
                 size, x, y):
        super().__init__(*groups)
        self.image = pygame.image.load(
            'data2/graphics/Sprites/11-Door/idle_big.png').convert_alpha()
        self.rect = self.image.get_rect(bottomleft=(x, y + size))

    def update(self, shift=0):
        self.rect.x += shift


class AnimatedTile(pygame.sprite.Sprite):
    def __init__(self, groups: list,
                 size, x, y, path):
        super().__init__(*groups)
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.frames = get_frames(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, shift=0):
        self.animate()
        self.rect.x += shift


class Coin(pygame.sprite.Sprite):
    def __init__(self, groups: list,
                 size, x, y, path):
        super().__init__(*groups)
        self.frames = get_frames(path, scale=2)
        self.grab_frames = get_frames('data2/graphics/Sprites1/Pirate Treasure/Sprites/Coin Effect', scale=2)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(x + size // 2, y + size // 2))
        self.sound = pygame.mixer.Sound('data2/sounds/Coin/mixkit-space-coin-win-notification-271.wav')
        self.grabbed = False

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def grab_animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.grab_frames):
            self.kill()
        else:
            self.image = self.grab_frames[int(self.frame_index)]

    def grab(self):
        if not self.grabbed:
            self.sound.play()
            self.frame_index = 0
            self.grabbed = True

    def update(self, shift=0):
        if self.grabbed is True:
            self.grab_animate()
        else:
            self.animate()
        self.rect.x += shift


class Candle(pygame.sprite.Sprite):
    def __init__(self, groups: list,
                 size, x, y, path):
        super().__init__(*groups)
        self.frames = get_frames(path, scale=2)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(x + size // 2, y + size // 2))

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, shift=0):
        self.animate()
        self.rect.x += shift


class Water(pygame.sprite.Sprite):
    def __init__(self, groups: list,
                 size, x, y, path):
        super().__init__(*groups)
        self.frames = get_frames(path, scale=2, size=TILE_SIZE)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(x + size // 2, y + size // 2))

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, shift=0):
        self.animate()
        self.rect.x += shift


class Chain(pygame.sprite.Sprite):
    def __init__(self, groups: list,
                 size, x, y, path):
        super().__init__(*groups)
        self.frames = get_frames(path, scale=2)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(x + size // 2, y + size // 2))
        self.animation_speed = random.choice((0.01, 0.005))

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, shift=0):
        self.animate()
        self.rect.x += shift

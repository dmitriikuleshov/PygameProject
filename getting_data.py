import os
import csv
import pygame
from settings import *


def get_level_markup(path):
    with open(path) as csv_file_obj:
        leve_data = list(csv.reader(csv_file_obj, delimiter=','))
        return leve_data


def get_cut_images(path):
    image = pygame.image.load(path).convert_alpha()
    horizontal_tile_num = int(image.get_size()[0] / TILE_SIZE)
    vertical_tile_num = int(image.get_size()[1] / TILE_SIZE)

    cut_tiles = []
    for row in range(vertical_tile_num):
        for col in range(horizontal_tile_num):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            tile_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA, 32)
            tile_surface.blit(image, (0, 0), pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            cut_tiles.append(tile_surface)
    return cut_tiles


def get_frames(path):
    images = list(os.walk(path))[0][2]
    frames = [pygame.image.load(f'{path}/{image}') for image in images]
    return frames

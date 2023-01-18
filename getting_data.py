import os
import csv
import pygame
from settings import *


def get_level_markup(path):
    with open(path) as csv_file_obj:
        leve_data = list(csv.reader(csv_file_obj, delimiter=','))
        return leve_data


def get_cut_images(path, real_size=TILE_SIZE):
    image = pygame.image.load(path).convert_alpha()
    horizontal_tile_num = int(image.get_size()[0] / real_size)
    vertical_tile_num = int(image.get_size()[1] / real_size)

    cut_tiles = []
    for row in range(vertical_tile_num):
        for col in range(horizontal_tile_num):
            x = col * real_size
            y = row * real_size
            tile_surface = pygame.Surface((real_size, real_size), pygame.SRCALPHA, 32)
            # stackoverflow делает брбрбрбрбрбрбрбрбрбрбрбр
            tile_surface.blit(image, (0, 0), pygame.Rect(x, y, real_size, real_size))
            tile_surface = pygame.transform.scale(tile_surface, (TILE_SIZE, TILE_SIZE))
            cut_tiles.append(tile_surface)
    return cut_tiles


def get_frames(path, scale=1, size=None):
    images = list(os.walk(path))[0][2]
    frames = [pygame.image.load(f'{path}/{image}') for image in images]
    frames = [pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale)) for image in frames]
    if size is not None:
        frames = [pygame.transform.scale(image, (size, size)) for image in frames]
    return frames

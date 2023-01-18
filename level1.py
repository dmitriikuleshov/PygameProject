import pygame

from getting_data import get_level_markup, get_cut_images
from settings import *
from tile import Tile, StaticTile
from enemy import Enemy
from player import Player


class Level1:
    level_markup = {
        'background_tiles': get_level_markup('data2/level1/level_markup/level1_background_tiles.csv'),
        'barrel_tiles': get_level_markup('data2/level1/level_markup/level1_barrel_tiles.csv'),
        'bottle_tiles': get_level_markup('data2/level1/level_markup/level1_bottle_tiles.csv'),
        'chest_tiles': get_level_markup('data2/level1/level_markup/level1_chest_tiles.csv'),
        'coin_tiles': get_level_markup('data2/level1/level_markup/level1_coin_tiles.csv'),
        'decoration_chain_tiles': get_level_markup('data2/level1/level_markup/level1_decoration_chain_tiles.csv'),
        'decoration_tiles': get_level_markup('data2/level1/level_markup/level1_decoration_tiles.csv'),
        'door_tiles': get_level_markup('data2/level1/level_markup/level1_door_tiles.csv'),
        'enemy_bald_tiles': get_level_markup('data2/level1/level_markup/level1_enemy_bald_tiles.csv'),
        'enemy_big_tiles': get_level_markup('data2/level1/level_markup/level1_enemy_big_tiles.csv'),
        'enemy_limits_tiles': get_level_markup('data2/level1/level_markup/level1_enemy_limits_tiles.csv'),
        'green_bottle_tiles': get_level_markup('data2/level1/level_markup/level1_green_bottle_tiles.csv'),
        'platform_tiles': get_level_markup('data2/level1/level_markup/level1_platform_tiles.csv'),
        'platform1_tiles': get_level_markup('data2/level1/level_markup/level1_platform1_tiles.csv'),
        'table_tiles': get_level_markup('data2/level1/level_markup/level1_table_tiles.csv'),
        'wall_tiles': get_level_markup('data2/level1/level_markup/level1_wall_tiles.csv'),
        'water_tiles': get_level_markup('data2/level1/level_markup/level1_water_tiles.csv'),
        'setup_tiles': get_level_markup('data2/level1/level_markup/level1_setup_tiles.csv')
    }

    def __init__(self, surface):
        self.display_surface = surface
        self.world_shift = 0
        self.background_sprites = self.create_tile_group(self.level_markup['background_tiles'], 'background_tiles')
        self.barrel_sprites = self.create_tile_group(self.level_markup['barrel_tiles'], 'barrel_tiles')
        self.bottle_sprites = self.create_tile_group(self.level_markup['bottle_tiles'], 'bottle_tiles')
        self.chest_sprites = self.create_tile_group(self.level_markup['chest_tiles'], 'chest_tiles')
        self.coin_sprites = self.create_tile_group(self.level_markup['coin_tiles'], 'coin_tiles')
        self.decoration_chain_sprites = self.create_tile_group(self.level_markup['decoration_chain_tiles'], 'decoration_chain_tiles')
        self.decoration_sprites = self.create_tile_group(self.level_markup['decoration_tiles'], 'decoration_tiles')
        self.door_sprites = self.create_tile_group(self.level_markup['door_tiles'], 'door_tiles')
        self.enemy_bald_sprites = self.create_tile_group(self.level_markup['enemy_bald_tiles'], 'enemy_bald_tiles')
        self.enemy_big_sprites = self.create_tile_group(self.level_markup['enemy_big_tiles'], 'enemy_big_tiles')
        self.enemy_limits_sprites = self.create_tile_group(self.level_markup['enemy_limits_tiles'], 'enemy_limits_tiles')
        self.green_bottle_sprites = self.create_tile_group(self.level_markup['green_bottle_tiles'], 'green_bottle_tiles')
        self.platform_sprites = self.create_tile_group(self.level_markup['platform_tiles'], 'platform_tiles')
        self.table_sprites = self.create_tile_group(self.level_markup['table_tiles'], 'table_tiles')
        self.wall_sprites = self.create_tile_group(self.level_markup['wall_tiles'], 'wall_tiles')
        self.water_sprites = self.create_tile_group(self.level_markup['water_tiles'], 'water_tiles')
        self.player_sprite = None
        self.player_sprites = pygame.sprite.GroupSingle()
        self.player_setup(self.level_markup['setup_tiles'])
        self.current_player_x = 0

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if val == '0':
                    self.player_sprite = Player(group=self.player_sprites, pos=(x, y))
                if val == '1':
                    hat_surface = pygame.image.load(
                        'data2/Treasure Hunters/Character/character/hat.png').convert_alpha()
                    hat_surface = pygame.transform.scale(hat_surface,
                                                         (hat_surface.get_width() / 2, hat_surface.get_height() / 2))
                    StaticTile([self.goal_sprites], x=x, y=y, surface=hat_surface)

    @staticmethod
    def create_tile_group(layout, tiles_type):
        sprite_group = pygame.sprite.Group()

        return sprite_group

    def enemy_collision_reverse(self):
        for enemy in self.enemy_bald_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.enemy_limits_sprites, False):
                enemy.reverse()

    def horizontal_movement_collisions(self):
        self.player_sprite.rect.x += self.player_sprite.direction.x * self.player_sprite.speed
        for sprite in self.wall_sprites.sprites():
            if sprite.rect.colliderect(self.player_sprite.rect):
                if self.player_sprite.direction.x < 0:
                    self.player_sprite.rect.left = sprite.rect.right
                    self.player_sprite.on_left = True
                    self.current_player_x = self.player_sprite.rect.left
                elif self.player_sprite.direction.x > 0:
                    self.player_sprite.rect.right = sprite.rect.left
                    self.player_sprite.on_right = True
                    self.current_player_x = self.player_sprite.rect.right

        if self.player_sprite.on_left and \
                (self.player_sprite.rect.left < self.current_player_x or self.player_sprite.direction.x >= 0):
            self.player_sprite.on_left = False
        if self.player_sprite.on_right and \
                (self.player_sprite.rect.left > self.current_player_x or self.player_sprite.direction.x <= 0):
            self.player_sprite.on_right = False

    def vertical_movement_collision(self):
        self.player_sprite.apply_gravity()
        for sprite in self.wall_sprites.sprites():
            if sprite.rect.colliderect(self.player_sprite.rect):
                if self.player_sprite.direction.y < 0:
                    self.player_sprite.rect.top = sprite.rect.bottom
                    self.player_sprite.direction.y = 0
                    self.player_sprite.on_ceiling = True
                elif self.player_sprite.direction.y > 0:
                    self.player_sprite.rect.bottom = sprite.rect.top
                    self.player_sprite.direction.y = 0
                    self.player_sprite.on_ground = True

        if self.player_sprite.on_ground and self.player_sprite.direction.y < 0 or self.player_sprite.direction.y > 1:
            self.player_sprite.on_ground = False
        if self.player_sprite.on_ceiling and self.player_sprite.direction.y > 0:
            self.player_sprite.on_ceiling = False

    def scroll_x(self):
        player_x = self.player_sprite.rect.centerx
        direction_x = self.player_sprite.direction.x

        if player_x < WIDTH / 4 and direction_x < 0:
            self.world_shift = 4
            self.player_sprite.speed = 0
        elif player_x > WIDTH - WIDTH / 4 and direction_x > 0:
            self.world_shift = -4
            self.player_sprite.speed = 0
        else:
            self.world_shift = 0
            self.player_sprite.speed = 4

    def run(self):
        self.player_sprites.draw(self.display_surface)
        self.player_sprites.update(self.world_shift)
        self.vertical_movement_collision()
        self.horizontal_movement_collisions()
        self.scroll_x()

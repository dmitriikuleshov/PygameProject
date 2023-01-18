import sys

import pygame

from getting_data import get_level_markup, get_cut_images
from settings import *
from tile import StaticTile, Coin, Barrel, Chest, Table, Door, Chain, Bottle, Candle, Water, Platform, Tile, KillBox
from player import Player
from enemy import EnemyBald, EnemyBig

pygame.mixer.pre_init(44100, -16, 1, 512)


class Level1:
    level_markup = {
        'background_tiles': get_level_markup('data2/level1/level_markup/level1_background_tiles.csv'),
        'barrel_tiles': get_level_markup('data2/level1/level_markup/level1_barrel_tiles.csv'),
        'bottle_tiles': get_level_markup('data2/level1/level_markup/level1_bottle_tiles.csv'),
        'chest_tiles': get_level_markup('data2/level1/level_markup/level1_chest_tiles.csv'),
        'coin_tiles': get_level_markup('data2/level1/level_markup/level1_coin_tiles.csv'),
        'decoration_chain_tiles': get_level_markup('data2/level1/level_markup/level1_decoration_chain_tiles.csv'),
        'decoration_candle_tiles': get_level_markup('data2/level1/level_markup/level1_decoration_candle_tiles.csv'),
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
        'setup_tiles': get_level_markup('data2/level1/level_markup/level1_setup_tiles.csv'),
        'water_kill_box_tiles': get_level_markup('data2/level1/level_markup/level1_water_kill_box_tiles.csv'),
        'door_end_box_tiles': get_level_markup('data2/level1/level_markup/level1_door_end_box_tiles.csv')
    }

    def __init__(self, game, surface):
        self.game = game
        self.display_surface = surface
        self.world_shift = 0
        self.background_sprites = self.create_tile_group(self.level_markup['background_tiles'], 'background_tiles')
        self.barrel_sprites = self.create_tile_group(self.level_markup['barrel_tiles'], 'barrel_tiles')
        self.bottle_sprites = self.create_tile_group(self.level_markup['bottle_tiles'], 'bottle_tiles')
        self.chest_sprites = self.create_tile_group(self.level_markup['chest_tiles'], 'chest_tiles')
        self.coin_sprites = self.create_tile_group(self.level_markup['coin_tiles'], 'coin_tiles')
        self.decoration_chain_sprites = self.create_tile_group(self.level_markup['decoration_chain_tiles'],
                                                               'decoration_chain_tiles')
        self.decoration_candle_sprites = self.create_tile_group(self.level_markup['decoration_candle_tiles'],
                                                                'decoration_candle_tiles')
        self.decoration_sprites = self.create_tile_group(self.level_markup['decoration_tiles'], 'decoration_tiles')
        self.door_sprites = self.create_tile_group(self.level_markup['door_tiles'], 'door_tiles')
        self.enemy_bald_sprites = self.create_tile_group(self.level_markup['enemy_bald_tiles'], 'enemy_bald_tiles')
        self.enemy_big_sprites = self.create_tile_group(self.level_markup['enemy_big_tiles'], 'enemy_big_tiles')
        self.enemy_limits_sprites = self.create_tile_group(self.level_markup['enemy_limits_tiles'],
                                                           'enemy_limits_tiles')
        self.water_kill_box_sprites = self.create_tile_group(self.level_markup['water_kill_box_tiles'],
                                                             'water_kill_box_tiles')
        self.green_bottle_sprites = self.create_tile_group(self.level_markup['green_bottle_tiles'],
                                                           'green_bottle_tiles')
        self.platform_sprites = self.create_tile_group(self.level_markup['platform_tiles'], 'platform_tiles')
        self.platform1_sprites = self.create_tile_group(self.level_markup['platform1_tiles'], 'platform1_tiles')
        self.table_sprites = self.create_tile_group(self.level_markup['table_tiles'], 'table_tiles')
        self.wall_sprites = self.create_tile_group(self.level_markup['wall_tiles'], 'wall_tiles')
        self.water_sprites = self.create_tile_group(self.level_markup['water_tiles'], 'water_tiles')

        self.collide_sprites = pygame.sprite.Group()
        self.collide_groups_list = [self.wall_sprites, self.table_sprites, self.platform_sprites,
                                    self.platform1_sprites, self.barrel_sprites, self.chest_sprites]
        self.door_end_box_sprites = self.create_tile_group(self.level_markup['door_end_box_tiles'],
                                                           'door_end_box_tiles')
        for group in self.collide_groups_list:
            for sprite in group.sprites():
                self.collide_sprites.add(sprite)

        self.water_kill_sound = pygame.mixer.Sound('data2/sounds/Water/mixkit-pouring-water-1302.wav')

        self.player_sprite = None
        self.player_sprites = pygame.sprite.GroupSingle()
        self.player_setup(self.level_markup['setup_tiles'])
        self.current_player_x = 0

        self.coin_counter = 0
        self.font = pygame.font.Font("assets/font.ttf", 50)
        self.coin_counter_text = self.font.render(str(self.coin_counter), True, "#b68f40")

        self.end_level_sound = pygame.mixer.Sound('data2/sounds/End/end.wav')

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if val == '0':
                    self.player_sprite = Player(group=self.player_sprites, pos=(x, y))

    @staticmethod
    def create_tile_group(layout, tiles_type):
        sprite_group = pygame.sprite.Group()

        if tiles_type == 'wall_tiles':
            tiles_list = get_cut_images('data2/graphics/Sprites/14-TileSets/Terrain (32x32).png', real_size=32)
            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row):
                    if val != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        tile_surface = tiles_list[int(val)]
                        StaticTile([sprite_group], x=x, y=y, surface=tile_surface)

        if tiles_type == 'background_tiles':
            tiles_list = get_cut_images('data2/graphics/Sprites/14-TileSets/Terrain (32x32).png', real_size=32)
            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row):
                    if val != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        tile_surface = tiles_list[int(val)]
                        StaticTile([sprite_group], x=x, y=y, surface=tile_surface)

        if tiles_type == 'platform_tiles':
            tiles_list = get_cut_images('data2/graphics/Sprites/14-TileSets/Decorations (32x32).png', real_size=32)
            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row):
                    if val != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        tile_surface = tiles_list[int(val)]
                        Platform([sprite_group], x=x, y=y, surface=tile_surface)

        if tiles_type == 'platform1_tiles':
            tiles_list = get_cut_images(
                'data2/graphics/Sprites1/Pirate Ship/Sprites/Tilesets/Terrain and Back Wall (32x32).png', real_size=32)
            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row):
                    if val != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        tile_surface = tiles_list[int(val)]
                        StaticTile([sprite_group], x=x, y=y, surface=tile_surface)

        if tiles_type == 'barrel_tiles':
            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row):
                    if val != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        Barrel([sprite_group], size=TILE_SIZE, x=x, y=y)

        if tiles_type == 'chest_tiles':
            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row):
                    if val != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        Chest([sprite_group], size=TILE_SIZE, x=x, y=y)

        if tiles_type == 'coin_tiles':
            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row):
                    if val != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        Coin([sprite_group], size=TILE_SIZE, x=x, y=y,
                             path='data2/Treasure Hunters/Pirate Treasure/Sprites/Gold Coin')

        if tiles_type == 'decoration_tiles':
            tiles_list = get_cut_images(
                'data2/graphics/Sprites/14-TileSets/Decorations (32x32).png', real_size=32)
            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row):
                    if val != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        tile_surface = tiles_list[int(val)]
                        StaticTile([sprite_group], x=x, y=y, surface=tile_surface)

        if tiles_type == 'table_tiles':
            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row):
                    if val != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        Table([sprite_group], size=TILE_SIZE, x=x, y=y)

        if tiles_type == 'door_tiles':
            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row):
                    if val != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        Door([sprite_group], size=TILE_SIZE, x=x, y=y)

        if tiles_type == 'decoration_chain_tiles':
            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row):
                    if val != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        Chain([sprite_group], size=TILE_SIZE, x=x, y=y,
                              path='data2/graphics/Sprites1/Pirate Ship/Sprites/Decorations/Chains/Big')

        if tiles_type == 'bottle_tiles':
            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row):
                    if val != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        if val == '1':
                            Bottle([sprite_group], size=TILE_SIZE, x=x, y=y,
                                   path='data2/graphics/Sprites1/Pirate Ship/'
                                        'Sprites/Decorations/Barrels and Bottles/03.png')
                        elif val == '2':
                            Bottle([sprite_group], size=TILE_SIZE, x=x, y=y,
                                   path='data2/graphics/Sprites1/Pirate Ship/'
                                        'Sprites/Decorations/Barrels and Bottles/04.png')
                        elif val == '3':
                            Bottle([sprite_group], size=TILE_SIZE, x=x, y=y,
                                   path='data2/graphics/Sprites1/Pirate Ship/'
                                        'Sprites/Decorations/Barrels and Bottles/05.png')

        if tiles_type == 'decoration_candle_tiles':
            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row):
                    if val != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        Candle([sprite_group], size=TILE_SIZE, x=x, y=y,
                               path='data2/graphics/Sprites1/Pirate Ship/Sprites/Decorations/Candle/Candle')

        if tiles_type == 'water_tiles':
            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row):
                    if val != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        Water([sprite_group], size=TILE_SIZE, x=x, y=y,
                              path='data2/graphics/Sprites1/Merchant Ship/Sprites/Water/Water/Top')

        if tiles_type == 'enemy_bald_tiles':
            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row):
                    if val != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        EnemyBald([sprite_group], x=x, y=y)

        if tiles_type == 'enemy_big_tiles':
            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row):
                    if val != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        EnemyBig([sprite_group], x=x, y=y)

        if tiles_type == 'enemy_limits_tiles':
            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row):
                    if val != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        Tile([sprite_group], TILE_SIZE, x=x, y=y)

        if tiles_type == 'water_kill_box_tiles':
            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row):
                    if val != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        KillBox([sprite_group], TILE_SIZE, x=x, y=y)

        if tiles_type == 'door_end_box_tiles':
            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row):
                    if val != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        Tile([sprite_group], TILE_SIZE, x=x, y=y)

        return sprite_group

    def enemy_collision_reverse(self):
        for enemy in self.enemy_bald_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.enemy_limits_sprites, False):
                enemy.reverse()
        for enemy in self.enemy_big_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.enemy_limits_sprites, False):
                enemy.reverse()

    @staticmethod
    def start_bg_music():
        pygame.mixer.music.load('data2/sounds/Bg/31 Flashback.mp3')
        pygame.mixer_music.play(-1)

    @staticmethod
    def end_bg_music():
        pygame.mixer_music.stop()

    def check_kill_boxes(self):
        if pygame.sprite.spritecollide(self.player_sprite, self.water_kill_box_sprites, False):
            self.end_bg_music()
            self.water_kill_sound.play()
            self.game.main_menu()
        if pygame.sprite.spritecollide(self.player_sprite, self.door_end_box_sprites, False):
            self.end_level_sound.play()
            self.end_bg_music()
            self.game.main_menu()

    def check_coin_collision(self):
        collision_coin_list = pygame.sprite.spritecollide(self.player_sprite, self.coin_sprites, False)
        for coin in collision_coin_list:
            if not coin.grabbed:
                self.coin_counter += 1
                self.change_coin_counter_text()
            coin.grab()

    def change_coin_counter_text(self):
        self.coin_counter_text = self.font.render(str(self.coin_counter), True, "#b68f40")

    def horizontal_movement_collisions(self):
        self.player_sprite.rect.x += self.player_sprite.direction.x * self.player_sprite.speed
        for sprite in self.collide_sprites.sprites():
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
        for sprite in self.collide_sprites.sprites():
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

        if player_x < WIDTH // 4 and direction_x < 0:
            self.world_shift = 8
            self.player_sprite.speed = 0
        elif player_x > WIDTH - WIDTH // 4 and direction_x > 0:
            self.world_shift = -8
            self.player_sprite.speed = 0
        else:
            self.world_shift = 0
            self.player_sprite.speed = 8

    def run(self):

        self.background_sprites.draw(self.display_surface)
        self.background_sprites.update(self.world_shift)

        self.wall_sprites.draw(self.display_surface)
        self.wall_sprites.update(self.world_shift)

        self.decoration_sprites.draw(self.display_surface)
        self.decoration_sprites.update(self.world_shift)

        self.door_sprites.draw(self.display_surface)
        self.door_sprites.update(self.world_shift)

        self.decoration_chain_sprites.draw(self.display_surface)
        self.decoration_chain_sprites.update(self.world_shift)

        self.decoration_candle_sprites.draw(self.display_surface)
        self.decoration_candle_sprites.update(self.world_shift)

        self.bottle_sprites.draw(self.display_surface)
        self.bottle_sprites.update(self.world_shift)

        self.platform_sprites.draw(self.display_surface)
        self.platform_sprites.update(self.world_shift)

        self.platform1_sprites.draw(self.display_surface)
        self.platform1_sprites.update(self.world_shift)

        self.barrel_sprites.draw(self.display_surface)
        self.barrel_sprites.update(self.world_shift)

        self.table_sprites.draw(self.display_surface)
        self.table_sprites.update(self.world_shift)

        self.chest_sprites.draw(self.display_surface)
        self.chest_sprites.update(self.world_shift)

        self.enemy_limits_sprites.update(self.world_shift)

        self.water_kill_box_sprites.update(self.world_shift)
        self.door_end_box_sprites.update(self.world_shift)

        self.player_sprites.draw(self.display_surface)
        self.player_sprites.update(self.world_shift)

        self.coin_sprites.draw(self.display_surface)
        self.coin_sprites.update(self.world_shift)

        self.enemy_bald_sprites.draw(self.display_surface)
        self.enemy_bald_sprites.update(self.world_shift)

        self.enemy_big_sprites.draw(self.display_surface)
        self.enemy_big_sprites.update(self.world_shift)

        self.water_sprites.draw(self.display_surface)
        self.water_sprites.update(self.world_shift)

        self.enemy_collision_reverse()
        self.check_coin_collision()
        self.check_kill_boxes()
        self.vertical_movement_collision()
        self.horizontal_movement_collisions()
        self.scroll_x()

        self.display_surface.blit(self.coin_counter_text, (50, 20))

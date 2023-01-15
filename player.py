import os
import pygame
from getting_data import get_frames


class Player(pygame.sprite.Sprite):
    frames_dict = {'idle': get_frames('data2/graphics/Sprites1/enemies/Sprites/1-Player-Bomb Guy/1-Idle'),
                   'run': get_frames('data2/graphics/Sprites1/enemies/Sprites/1-Player-Bomb Guy/2-Run'),
                   'jump': get_frames('data2/graphics/Sprites1/enemies/Sprites/1-Player-Bomb Guy/3-Jump Anticipation'),
                   'fall': get_frames('data2/graphics/Sprites1/enemies/Sprites/1-Player-Bomb Guy/5-Fall')}

    def __init__(self, group, pos):
        super().__init__(group)
        self.image = self.frames_dict['idle'][0]
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

        self.frame_index = 0
        self.animation_speed = 0.15
        self.status = 'idle'
        self.facing_right = True

        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        self.jump_sound = pygame.mixer.Sound('data2/sounds/Jump/mixkit-player-jumping-in-a-video-game-2043.wav')

    def animate(self):
        frames = self.frames_dict[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(frames):
            self.frame_index = 0

        image = frames[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)

        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
        self.jump_sound.play()

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

    def change_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        elif self.direction.y == 0 and self.direction.x != 0:
            self.status = 'run'
        elif self.direction.y == 0 and self.direction.x == 0:
            self.status = 'idle'

    def update(self, shift=0):
        self.get_input()
        self.animate()
        self.change_status()
        self.rect.x += shift

from math import sin

import pygame
from random import randint
from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, change_health, VOLUME):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.1
        self.image = self.animations['walk'][self.frame_index]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=pos)
        self.hit_sound = pygame.mixer.Sound('music/effects/hit.wav')
        self.jump_sound = pygame.mixer.Sound('music/effects/jump.wav')
        self.jump_sound_m = pygame.mixer.Sound('music/effects/jump_m.wav')
        self.jump_sound.set_volume(VOLUME)
        self.jump_sound_m.set_volume(VOLUME)
        self.hit_sound.set_volume(VOLUME)

        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 5
        self.gravity = 0.8
        self.jump_speed = -16
        self.jump_m = -22

        # player status
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        self.change_health = change_health
        self.invincible = False
        self.invincibility_duration = 500
        self.hurt_time = 0
        self.collision_rect = pygame.Rect(self.rect.topleft, (50, self.rect.height))

    def import_character_assets(self):
        character_path = 'picture/player/'
        self.animations = {'walk': [], 'run': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
        self.mask = pygame.mask.from_surface(self.image)

        if self.invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

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

        if keys[pygame.K_SPACE] and self.on_ground and not self.on_ceiling:
            self.jump()

    def get_damage(self):
        if not self.invincible:
            self.hit_sound.play()
            self.change_health(-10)
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()

    def invincibility_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def get_status(self):
        if self.direction.x != 0:
            self.status = 'run'
        else:
            self.status = 'walk'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
        self.jump_sound.play()

    def jump_mushroom(self):
        self.direction.y = self.jump_m
        self.jump_sound_m.play()

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.invincibility_timer()
        self.wave_value()


class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, x):
        self.rect.x += x


class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface
        self.mask = pygame.mask.from_surface(self.image)


class AnimatedTile(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, x):
        self.animate()
        self.rect.x += x


class Coins(AnimatedTile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, path)
        center_x = x + int(size / 2)
        center_y = y + int(size / 2)
        self.rect = self.image.get_rect(center=(center_x, center_y))


class Jump_m(AnimatedTile):
    def __init__(self, size, x, y, path):
        super().__init__(size + size, x, y, path)
        center_x, center_y = x + int(size) / 2, y + int(size / 2)
        self.rect = self.image.get_rect(center=(center_x, center_y))

    def animate(self):
        self.frame_index += 0.10
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)


class Moonflower(AnimatedTile):
    def __init__(self, size, x, y, path, offset):
        super().__init__(size, x, y, path)
        offset_y = y - offset
        self.rect.topleft = (x, offset_y)

    def update(self, x):
        self.rect.x += x


class Enemy(AnimatedTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, "picture/enemy")
        self.rect.y += size - self.image.get_size()[1]
        self.speed = randint(1, 3)

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)
            self.mask = pygame.mask.from_surface(self.image)

    def reverse(self):
        self.speed *= - 1

    def update(self, x):
        self.animate()
        self.rect.x += x
        self.move()
        self.reverse_image()

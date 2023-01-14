import pygame
from random import randint
from support import import_folder, load_image, import_picture


class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, x):
        self.rect.x -= x


# class Tile_con(Tile):
#     def __init__(self, size, x, y, surface):
#         super().__init__(size, x, y)
#         self.image = surface


class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface


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

    def update(self, x):
        self.animate()
        self.rect.x -= x


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


class Palm(AnimatedTile):
    def __init__(self, size, x, y, path, offset):
        super().__init__(size, x, y, path)
        offset_y = y - offset
        self.rect.topleft = (x, offset_y)


class Enemy(AnimatedTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, "Картинки/enemy")
        self.rect.y += size - self.image.get_size()[1]
        self.speed = randint(1, 2)

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= - 1

    def update(self, x):
        self.animate()
        self.rect.x -= x
        self.move()
        self.reverse_image()

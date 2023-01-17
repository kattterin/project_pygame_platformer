import pygame

from support import import_folder, load_image
from settings import *

from support import import_folder


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__()
        self.image = load_image("Картинки/player/walk/1.png")
        self.rect = self.image.get_rect()
        self.direction = pygame.math.Vector2(0, 0)
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def update(self):
        self.get_input()
        self.rect.x += self.direction.x * self.speed


#
class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - screen_width // 2)

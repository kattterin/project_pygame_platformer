import pygame

from support import import_folder, load_image
from settings import *


class Hero(pygame.sprite.Sprite):
    def __init__(self, terrain):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__()
        self.image = load_image("Картинки/player/walk/1.png")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 60
        self.x = terrain.copy()

    def update(self, event, x):
        global isjump, jump_count
        if not pygame.sprite.spritecollideany(self, self.x):
            if not pygame.sprite.spritecollideany(self, self.x):
                self.rect.y += 5
                if pygame.sprite.spritecollideany(self, self.x):
                    self.rect.y -= 5
                    isjump = False
                    jump_count = 0

            if pygame.key.get_pressed()[pygame.K_LEFT] and self.rect.x > 0:
                self.rect.x -= 10
                if pygame.sprite.spritecollideany(self, self.x):
                    self.rect.x += 10

            if pygame.key.get_pressed()[pygame.K_RIGHT] and self.rect.x < screen_width - self.image.get_rect().w:
                self.rect.x += 10
                if pygame.sprite.spritecollideany(self, self.x):
                    self.rect.x -= 10

            # if pygame.key.get_pressed()[pygame.K_DOWN] and self.rect.y < screen_height - self.image.get_rect().h:
            #     self.rect.y += 10
            #     if pygame.sprite.spritecollideany(self, self.x):
            #         self.rect.y -= 10
            # if pygame.key.get_pressed()[pygame.K_UP] and self.rect.y > 0:
            #     self.rect.y -= 10
            #     if pygame.sprite.spritecollideany(self, self.x):
            #         self.rect.y += 10
            self.rect.x -= x
            if pygame.key.get_pressed()[pygame.K_SPACE] and jump_count == 0:
                isjump = True
                jump_count = 1
            if isjump and 0 < jump_count < 15:
                self.rect.y -= 10

                jump_count += 1
        else:
            self.rect.y -= 10

class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - screen_width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - screen_height // 2)
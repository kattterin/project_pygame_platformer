from csv import reader
from itertools import product

from settings import tile_size
import pygame
import os
import sys
from PIL import Image


def import_picture(path):
    """
    промежуточная функция: изображение -> папка со спрайтами
    """
    im = Image.open(path)
    x = 0
    for i in range(8):
        im_crop = im.crop((x, 0, x + 64, 64))
        im_crop.save(f'picture/enemy/{str(i + 1)}.png', quality=95)
        x += 64


# import_picture("picture/claim.png")


def import_folder(path):
    surface_list = []
    for _, __, image_files in os.walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surf = load_image(full_path)
            surface_list.append(image_surf)

    return surface_list


def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map


def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size)

    cut_tiles = []

    for row, col in product(range(tile_num_y), range(tile_num_x)):
        x, y = col * tile_size, row * tile_size
        new_surf = pygame.Surface((tile_size, tile_size), flags=pygame.SRCALPHA)
        new_surf.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
        cut_tiles.append(new_surf)

    return cut_tiles


def load_image(name: str, colorkey=None) -> pygame.Surface:
    fullname = os.path.join(name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

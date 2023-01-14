import pygame

import random
from tile import *
from support import import_csv_layout, import_cut_graphics, load_image, import_folder
from settings import tile_size, screen_height, screen_width
from player import Hero, Camera

isjump = False
jump_count = 0


class Sky:
    def __init__(self, ):
        self.top = pygame.image.load('Картинки/фон.png').convert()
        self.top = pygame.transform.scale(self.top, (screen_width, tile_size * 15))

    def draw(self, surface):
        surface.blit(self.top, (0, 0))


class Water:
    def __init__(self, top, level_width):
        water_start = -screen_width
        water_tile_width = 192
        tile_x_amount = int((level_width + screen_width * 2) / water_tile_width)
        self.water_sprites = pygame.sprite.Group()

        for tile in range(tile_x_amount):
            x = tile * water_tile_width + water_start
            y = top
            sprite = AnimatedTile(192, x, y, 'Картинки/water')
            self.water_sprites.add(sprite)

    def draw(self, surface, shift):
        self.water_sprites.update(shift)
        self.water_sprites.draw(surface)


class Clouds:
    def __init__(self):
        self.top = load_image('Картинки/фон_деревья.png')
        self.top = pygame.transform.scale(self.top, (1000, 480))
        self.cloud_sprites = pygame.sprite.Group()
        sprite = StaticTile(0, 0, 0, self.top)
        self.cloud_sprites.add(sprite)

    def draw(self, surface, shift):
        self.cloud_sprites.draw(surface)


# class Hero(pygame.sprite.Sprite):
#     def __init__(self, terrain):
#         # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
#         # Это очень важно !!!
#         super().__init__()
#         self.image = load_image("boom.png")
#         self.rect = self.image.get_rect()
#         self.rect.x = 0
#         self.rect.y = 60
#         self.x = terrain.copy()
#
#     def update(self, event, x):
#         global isjump, jump_count
#         if not pygame.sprite.spritecollideany(self, self.x):
#             if not pygame.sprite.spritecollideany(self, self.x):
#                 self.rect.y += 5
#                 if pygame.sprite.spritecollideany(self, self.x):
#                     self.rect.y -= 5
#                     isjump = False
#                     jump_count = 0
#
#             if pygame.key.get_pressed()[pygame.K_LEFT] and self.rect.x > 0:
#                 self.rect.x -= 10
#                 if pygame.sprite.spritecollideany(self, self.x):
#                     self.rect.x += 10
#
#             if pygame.key.get_pressed()[pygame.K_RIGHT] and self.rect.x < screen_width - self.image.get_rect().w:
#                 self.rect.x += 10
#                 if pygame.sprite.spritecollideany(self, self.x):
#                     self.rect.x -= 10
#
#             # if pygame.key.get_pressed()[pygame.K_DOWN] and self.rect.y < screen_height - self.image.get_rect().h:
#             #     self.rect.y += 10
#             #     if pygame.sprite.spritecollideany(self, self.x):
#             #         self.rect.y -= 10
#             # if pygame.key.get_pressed()[pygame.K_UP] and self.rect.y > 0:
#             #     self.rect.y -= 10
#             #     if pygame.sprite.spritecollideany(self, self.x):
#             #         self.rect.y += 10
#             self.rect.x -= x
#             if pygame.key.get_pressed()[pygame.K_SPACE] and jump_count == 0:
#                 isjump = True
#                 jump_count = 1
#             if isjump and 0 < jump_count < 15:
#                 self.rect.y -= 10
#
#                 jump_count += 1
#         else:
#             self.rect.y -= 10


class Level:
    def __init__(self, level_data, surface):
        # general setup
        self.display_surface = surface
        self.world_shift = 2
        # self.current_x = None

        # player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        # self.player_setup(player_layout)
        # платформа
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')
        # природа
        nature = import_csv_layout(level_data['nature'])
        self.nature = self.create_tile_group(nature, 'nature')
        # coins
        coins_l = import_csv_layout(level_data['coins'])
        self.coins_l = self.create_tile_group(coins_l, 'coins')
        # constaints
        constaints_l = import_csv_layout(level_data['constraints'])
        self.constaints = self.create_tile_group(constaints_l, 'constraints')
        # traps
        traps = import_csv_layout(level_data['trap'])
        self.traps = self.create_tile_group(traps, 'trap')
        # enemies
        enemies_l = import_csv_layout(level_data['enemies'])
        self.enemies_l = self.create_tile_group(enemies_l, 'enemies')
        # # fg_palms
        jump = import_csv_layout(level_data['jump'])
        self.jump = self.create_tile_group(jump, 'jump')
        # # decoration
        self.sky = Sky()
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 20, level_width)
        self.clouds = Clouds()
        self.player_sp = self.create_tile_group(terrain_layout, 'pl')

        # self.player_sp = self.create_tile_group(terrain_layout, 'pl')

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        if type == 'pl':
            sprite = Hero(self.terrain_sprites)
            sprite_group.add(sprite)
            return sprite_group
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                sprite = ''
                if val != "-1":
                    x, y = col_index * tile_size, row_index * tile_size
                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics("Картинки/земелька.png")
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    if type == 'nature':
                        grass_tile_list = import_cut_graphics("Картинки/земелька2.png")
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    if type == 'jump':
                        if int(val) in [12, 14, 16, 18, 20, 22]:
                            sprite = Jump_m(tile_size, x, y - 10, "Картинки/jump_mushroom")
                    # if type == 'bg_palms':
                    #     sprite = Palm(tile_size, x, y, "maps/decor/terrain/palm_bg", 64)
                    if type == 'coins':
                        sprite = AnimatedTile(tile_size, x, y, "Картинки/berry_coins")
                    if type == 'constraints':
                        sprite = Tile(tile_size, x, y)
                    if type == 'enemies':
                        if int(val) in [0, 2, 4, 6, 8, 10, 12, 14]:
                            sprite = Enemy(tile_size, x, y + 36)
                    if type == 'trap':
                        traps = import_cut_graphics("Картинки/что-то непонятное.png")
                        tile_surface = traps[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    if sprite:
                        sprite_group.add(sprite)
        return sprite_group

    # def player_setup(self, layout):
    #     for row_index, row in enumerate(layout):
    #         for col_index, val in enumerate(row):
    #             x, y = col_index * tile_size, row_index * tile_size
    #
    #             if val == "0":
    #                 print('players goes here')
    #             if val == '1':
    #                 hat_surface = load_image("maps/decor/character/hat.png")
    #                 sprite = StaticTile(tile_size, x, y, hat_surface)
    #                 self.goal.add(sprite)

    def enemy_collision_reverse(self):
        for enemy in self.enemies_l.sprites():
            if pygame.sprite.spritecollide(enemy, self.constaints, False):
                enemy.reverse()

    def run(self, event):
        # camera = Camera()
        # for sprite in player:
        #     camera.apply(sprite)
        # decoration
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)
        # terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)
        # природа
        self.nature.update(self.world_shift)
        self.nature.draw(self.display_surface)
        self.water.draw(self.display_surface, self.world_shift)
        self.constaints.update(self.world_shift)
        # coins
        self.coins_l.update(self.world_shift)
        self.coins_l.draw(self.display_surface)
        # traps
        self.traps.update(self.world_shift)
        self.traps.draw(self.display_surface)
        # грибы
        self.jump.update(self.world_shift)
        self.jump.draw(self.display_surface)
        # enemies
        self.enemies_l.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemies_l.draw(self.display_surface)
        # player
        self.player_sp.draw(self.display_surface)
        self.player_sp.update(event, self.world_shift)
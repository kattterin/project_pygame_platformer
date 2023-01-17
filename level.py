import pygame

import random
from tile import *
from support import import_csv_layout, import_cut_graphics, load_image, import_folder
from settings import tile_size, screen_height, screen_width


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

    def draw(self, surface):
        self.cloud_sprites.draw(surface)


class Level:
    def __init__(self, level_data, surface):
        # general setup
        self.display_surface = surface
        self.world_shift = 2

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
        # portail
        portails = import_csv_layout(level_data['portail'])
        self.portails = self.create_tile_group(portails, 'portail')
        # enemies
        enemies_l = import_csv_layout(level_data['enemies'])
        self.enemies_l = self.create_tile_group(enemies_l, 'enemies')
        # # fg_palms
        jump = import_csv_layout(level_data['jump'])
        self.jump = self.create_tile_group(jump, 'jump')
        moonflower = import_csv_layout(level_data['bg'])
        self.moonflower = self.create_tile_group(moonflower, 'bg')
        # # decoration
        self.sky = Sky()
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 20, level_width)
        self.clouds = Clouds()
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()

        # self.player_sp = self.create_tile_group(terrain_layout, 'pl')

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
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
                    if type == 'portail':
                        sprite = Tile(tile_size, x, y)
                    if type == 'bg':
                        sprite = Moonflower(tile_size, x, y, "Картинки/flowers", 90)
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


    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def enemy_collision_reverse(self):
        for enemy in self.enemies_l.sprites():
            if pygame.sprite.spritecollide(enemy, self.constaints, False):
                enemy.reverse()

    def camera(self):
        player = self.player.sprite
        player_x = player.rect.x
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 5
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -5
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 5

    def horizontal(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites()
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False

    def run(self):
        # decoration
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface)
        self.moonflower.update(self.world_shift)
        self.moonflower.draw(self.display_surface)
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

        self.portails.update(self.world_shift)
        self.portails.draw(self.display_surface)
        # грибы
        self.jump.update(self.world_shift)
        self.jump.draw(self.display_surface)
        # enemies
        self.enemies_l.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemies_l.draw(self.display_surface)
        self.camera()

        self.player.update()
        self.horizontal()
        # self.get_player_on_ground()
        self.vertical()
        # self.create_landing_dust()
        self.player.draw(self.display_surface)

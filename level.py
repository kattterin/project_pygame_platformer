import sys

import pygame

from tile import Tile, StaticTile, AnimatedTile, Coins, Jump_m, Moonflower, Enemy, Player
from support import import_csv_layout, import_cut_graphics, load_image, import_folder
from settings import tile_size, screen_height, screen_width


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.5
        if type == 'explosion':
            self.frames = import_folder('picture/particles')
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift


class Sky:
    def __init__(self):
        self.top = pygame.image.load('picture/fons/fon.png').convert()

        # self.top = pygame.image.load('picture/fons/fortress.png').convert()
        # self.top = pygame.image.load('picture/fons/fon.png').convert()
        # self.top = pygame.image.load('picture/fons/desertnight.png').convert()

        self.top = pygame.transform.scale(self.top, (1408, tile_size * 15))

    def draw(self, surface):
        surface.blit(self.top, (-100, -150))


class Water:
    def __init__(self, top, level_width):
        water_start = -screen_width
        water_tile_width = 192
        tile_x_amount = int((level_width + screen_width * 2) / water_tile_width)
        self.water_sprites = pygame.sprite.Group()

        for tile in range(tile_x_amount):
            x = tile * water_tile_width + water_start
            y = top
            sprite = AnimatedTile(192, x, y - 10, 'picture/water')
            self.water_sprites.add(sprite)

    def draw(self, surface, shift):
        self.water_sprites.update(shift)
        self.water_sprites.draw(surface)


class Trees:
    def __init__(self):
        self.top = load_image('picture/fon_treets.png')
        self.top = pygame.transform.scale(self.top, (1200, 704))
        self.trees_sprites = pygame.sprite.Group()
        sprite = StaticTile(0, 0, 0, self.top)
        self.trees_sprites.add(sprite)

    def draw(self, surface):
        self.trees_sprites.draw(surface)


class Level:
    def __init__(self, level_data, surface, change_coins, change_health, life, VOLUME, change_level):
        self.display_surface = surface
        self.world_shift = -5
        self.change_coins = change_coins
        self.life = life
        self.coin_sound = pygame.mixer.Sound('music/effects/coin.wav')
        self.stomp_sound = pygame.mixer.Sound('music/effects/stomp.wav')
        self.coin_sound.set_volume(VOLUME)
        self.stomp_sound.set_volume(VOLUME)
        self.change_levels = change_level

        # платформа
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        sprite = Player((32, 320), change_health, VOLUME)
        self.player.add(sprite)

        # порталы
        portals = import_csv_layout(level_data['portail'])
        self.portals = self.create_tile_group(portals, 'portail')
        # частицы
        self.explosion_sprites = pygame.sprite.Group()
        # природа
        nature = import_csv_layout(level_data['nature'])
        self.nature = self.create_tile_group(nature, 'nature')
        nature2 = import_csv_layout(level_data['nature2'])
        self.nature2 = self.create_tile_group(nature2, 'nature2')
        # монеты
        coins_l = import_csv_layout(level_data['coins'])
        self.coins_l = self.create_tile_group(coins_l, 'coins')
        # ограничения
        constaints_l = import_csv_layout(level_data['constraints'])
        self.constaints = self.create_tile_group(constaints_l, 'constraints')
        # ловушки
        traps = import_csv_layout(level_data['trap'])
        self.traps = self.create_tile_group(traps, 'trap')
        # враги
        enemies_l = import_csv_layout(level_data['enemies'])
        self.enemies_l = self.create_tile_group(enemies_l, 'enemies')
        # прыжок
        jump = import_csv_layout(level_data['jump'])
        self.jump = self.create_tile_group(jump, 'jump')
        # декорации
        moonflower = import_csv_layout(level_data['bg'])
        self.moonflower = self.create_tile_group(moonflower, 'bg')
        self.sky = Sky()
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 20, level_width)
        self.trees = Trees()

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                sprite = ''
                if val != "-1":
                    x, y = col_index * tile_size, row_index * tile_size
                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics("picture/terrain.png")
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    if type == 'nature':
                        grass_tile_list = import_cut_graphics("picture/nature 1.png")
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'nature2':
                        grass_tile_list = import_cut_graphics("picture/nature2.png")
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    if type == 'jump':
                        sprite = Jump_m(tile_size, x, y + 5, "picture/jump_mushroom")
                    if type == 'bg':
                        sprite = Moonflower(tile_size, x, y, "picture/flowers", 60)
                    if type == 'portail':
                        sprite = Moonflower(tile_size, x, y, "picture/portails", 10)
                    if type == 'coins':
                        sprite = Coins(tile_size, x, y, "picture/berry_coins")
                    if type == 'constraints':
                        sprite = Tile(tile_size, x, y)
                    if type == 'enemies':
                        sprite = Enemy(tile_size, x, y + 5)
                    if type == 'trap':
                        traps = import_cut_graphics("picture/trap.png")
                        tile_surface = traps[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    if sprite:
                        sprite_group.add(sprite)
        return sprite_group

    def enemy_collision_reverse(self):
        for enemy in self.enemies_l.sprites():
            if pygame.sprite.spritecollide(enemy, self.constaints, False):
                enemy.reverse()

    def horizontal(self):
        "столкновение с горизонтальными элементами платформы"
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
        "столкновение с вертикальными элементами платформы"
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites()

        for sprite in collidable_sprites:
            # if pygame.sprite.collide_mask(sprite, player):
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 0:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False

    def camera(self):
        player = self.player.sprite
        player_x = player.rect.centerx
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

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def check_enemy_collisions(self):
        player = self.player.sprite
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemies_l, False)

        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = player.rect.bottom
                if enemy_top < player_bottom < enemy_center and player.direction.y >= 0:
                    self.stomp_sound.play()
                    player.direction.y = -15
                    explosion_sprite = ParticleEffect(enemy.rect.center, 'explosion')
                    self.explosion_sprites.add(explosion_sprite)
                    enemy.kill()
                else:
                    player.get_damage()

    def water_collisions(self):
        player = self.player.sprite
        collidable_sprites = self.water.water_sprites.sprites()

        for sprite in collidable_sprites:
            # if pygame.sprite.collide_mask(sprite, player):
            if sprite.rect.colliderect(player.rect):
                self.life()

    def coin_collisions(self):
        player = self.player.sprite

        for sprite1 in self.coins_l.sprites():
            if pygame.sprite.collide_mask(player, sprite1):
                self.coin_sound.play()
                self.change_coins(1)
                sprite1.kill()

    def portal_collisions(self):
        player = self.player.sprite

        for sprite1 in self.portals.sprites():
            if pygame.sprite.collide_mask(player, sprite1):
                self.change_levels()

    def jump_collissions(self):
        player = self.player.sprite

        for sprite1 in self.jump.sprites():
            if pygame.sprite.collide_mask(player, sprite1):
                player.jump_mushroom()

    def traps_collisions(self):
        collidable_sprites = self.traps.sprites()
        player = self.player.sprite

        for i in collidable_sprites:
            if pygame.sprite.collide_mask(i, player):
                player.get_damage()

        # if pygame.sprite.collide_mask(self.player.sprite, self.traps):
        #     print("kill")

        #
        # enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.traps, False)
        #
        # if enemy_collisions:
        #     print("kill")

    def run(self):
        # decoration
        self.sky.draw(self.display_surface)
        self.trees.draw(self.display_surface)
        self.moonflower.update(self.world_shift)
        self.moonflower.draw(self.display_surface)
        # terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)
        # природа
        self.nature.update(self.world_shift)
        self.nature.draw(self.display_surface)
        self.nature2.update(self.world_shift)
        self.nature2.draw(self.display_surface)
        self.water.draw(self.display_surface, self.world_shift)
        self.constaints.update(self.world_shift)
        # traps
        self.traps.update(self.world_shift)
        self.traps.draw(self.display_surface)
        # self.portails.update(self.world_shift)
        # self.portails.draw(self.display_surface)
        # грибы
        self.jump.update(self.world_shift)
        self.jump.draw(self.display_surface)
        # coins
        self.coins_l.update(self.world_shift)
        self.coins_l.draw(self.display_surface)
        # enemies
        self.explosion_sprites.update(self.world_shift)
        self.explosion_sprites.draw(self.display_surface)

        self.portals.update(self.world_shift)
        self.portals.draw(self.display_surface)

        self.enemies_l.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemies_l.draw(self.display_surface)

        self.player.update()
        self.horizontal()

        self.get_player_on_ground()
        self.vertical()
        self.check_enemy_collisions()
        self.coin_collisions()
        self.jump_collissions()
        self.traps_collisions()
        self.water_collisions()
        self.portal_collisions()

        self.player.draw(self.display_surface)
        self.camera()

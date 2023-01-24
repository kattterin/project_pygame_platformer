import pygame
import sys
from settings import *
from level import Level
from ui import UI

level_1 = {'terrain': "maps_levels/0/level_01_terrain.csv",
           'portail': "maps_levels/0/level_01_player.csv",
           'trap': "maps_levels/0/level_01_traps.csv",
           'nature': "maps_levels/0/level_01_nature.csv",
           'jump': "maps_levels/0/level_01_jump_mushroom.csv",
           'enemies': "maps_levels/0/level_01_enemy.csv",
           'constraints': "maps_levels/0/level_01_constaints.csv",
           'coins': "maps_levels/0/level_01_coins.csv",
           "bg": "maps_levels/0/level_01_bg.csv",
           "nature2": "maps_levels/0/level_01_nature2.csv"}


# Pygame setup
pygame.init()
max_health = 100
cur_health = 100
coins = 0

screen = pygame.display.set_mode((screen_width, screen_height))
ui = UI(screen)

clock = pygame.time.Clock()
level = Level(level_1, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    level.run()
    ui.show_health(cur_health, max_health)
    ui.show_coins(coins)

    pygame.display.update()
    clock.tick(60)

import pygame
import sys
from settings import *
from level import Level

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
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_1, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('grey')
    level.run()

    pygame.display.update()
    clock.tick(60)
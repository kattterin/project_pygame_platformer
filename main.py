import pygame
import sys
from settings import *
from level import *

FPS = 60
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Герой двигается!')
level_1 = {'terrain': "levels/0/level_01_terrain.csv",
           'portail': "levels/0/level_01_portail.csv",
           'trap': "levels/0/level_01_ловушечка.csv",
           'nature': "levels/0/level_01_растения.csv",
           'jump': "levels/0/level_01_прыжки.csv",
           'enemies': "levels/0/level_01_enemy.csv",
           'constraints': "levels/0/level_01_ограничения.csv",
           'coins': "levels/0/level_01_coins.csv",
           "bg": "levels/0/level_01_bg.csv"}

level_2 = {'terrain': "levels/1/level_02_terrain.csv",
           'portail': "levels/0/level_02_portail.csv",
           'trap': "levels/1/level_02_ловушечка.csv",
           'nature': "levels/1/level_02_растения.csv",
           'jump': "levels/1/level_02_прыжки.csv",
           'enemies': "levels/1/level_02_enemy.csv",
           'constraints': "levels/1/level_02_ограничения.csv",
           'coins': "levels/1/level_02_coins.csv",
           "bg": "levels/1/level_02_bg.csv"}
level = Level(level_1, screen)
clock = pygame.time.Clock()


def main():
    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # all_sprites.draw(screen)
        # all_sprites.update(event)
        screen.fill("black")
        level.run()

        # clock.tick(FPS)
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    # pygame.mouse.set_visible(False)

    main()

import os
import sqlite3

import pygame
import sys
from settings import *
from level import Level
import pygame_menu
from pygame_menu.examples import create_example_window

from random import randrange
from typing import Tuple, Any, Optional, List

from support import load_image


class UI:
    def __init__(self, surface):
        # setup
        self.display_surface = surface

        # health
        self.health_bar = pygame.image.load('picture/health_bar2.png').convert_alpha()

        self.health_bar_topleft = (54, 39)
        self.bar_max_width = 152
        self.bar_height = 4

        # coins
        self.coin = load_image('picture/berry_coins/1.png')
        self.coin_rect = self.coin.get_rect(topleft=(50, 61))

        self.font = pygame.font.Font('picture/ITC.ttf', 30)

    def show_health(self, current, full):
        self.display_surface.blit(self.health_bar, (20, 10))
        current_health_ratio = current / full
        current_bar_width = self.bar_max_width * current_health_ratio
        health_bar_rect = pygame.Rect(self.health_bar_topleft, (current_bar_width, self.bar_height))
        # pygame.draw.rect(self.display_surface, '#a840ff', health_bar_rect)
        pygame.draw.rect(self.display_surface, "#dc4949", health_bar_rect)

    def show_coins(self, amount):
        self.display_surface.blit(self.coin, self.coin_rect)
        coin_amount_surf = self.font.render(str(amount), False, (255, 255, 255))
        coin_amount_rect = coin_amount_surf.get_rect(midleft=(self.coin_rect.right + 4, self.coin_rect.centery))
        self.display_surface.blit(coin_amount_surf, coin_amount_rect)


level_1 = {'terrain': "maps_levels/1/1_level_terrain.csv",
           'portail': "maps_levels/1/1_level_player.csv",
           'trap': "maps_levels/1/1_level_traps.csv",
           'nature': "maps_levels/1/1_level_nature.csv",
           'jump': "maps_levels/1/1_level_jump_mushroom.csv",
           'enemies': "maps_levels/1/1_level_enemy.csv",
           'constraints': "maps_levels/1/1_level_constaints.csv",
           'coins': "maps_levels/1/1_level_coins.csv",
           "bg": "maps_levels/1/1_level_bg.csv",
           "nature2": "maps_levels/1/1_level_nature2.csv"}
level_2 = {'terrain': "maps_levels/2/2_level_terrain.csv",
           'portail': "maps_levels/2/2_level_player.csv",
           'trap': "maps_levels/2/2_level_traps.csv",
           'nature': "maps_levels/2/2_level_nature.csv",
           'jump': "maps_levels/2/2_level_jump_mushroom.csv",
           'enemies': "maps_levels/2/2_level_enemy.csv",
           'constraints': "maps_levels/2/2_level_constaints.csv",
           'coins': "maps_levels/2/2_level_coins.csv",
           "bg": "maps_levels/2/2_level_bg.csv",
           "nature2": "maps_levels/2/2_level_nature2.csv"}
level_3 = {'terrain': "maps_levels/3/3_level_terrain.csv",
           'portail': "maps_levels/3/3_level_player.csv",
           'trap': "maps_levels/3/3_level_traps.csv",
           'nature': "maps_levels/3/3_level_nature.csv",
           'jump': "maps_levels/3/3_level_jump_mushroom.csv",
           'enemies': "maps_levels/3/3_level_enemy.csv",
           'constraints': "maps_levels/3/3_level_constaints.csv",
           'coins': "maps_levels/3/3_level_coins.csv",
           "bg": "maps_levels/3/3_level_bg.csv",
           "nature2": "maps_levels/3/3_level_nature2.csv"}
level_4 = {'terrain': "maps_levels/4/4_level_terrain.csv",
           'portail': "maps_levels/4/4_level_player.csv",
           'trap': "maps_levels/4/4_level_traps.csv",
           'nature': "maps_levels/4/4_level_nature.csv",
           'jump': "maps_levels/4/4_level_jump_mushroom.csv",
           'enemies': "maps_levels/4/4_level_enemy.csv",
           'constraints': "maps_levels/4/4_level_constaints.csv",
           'coins': "maps_levels/4/4_level_coins.csv",
           "bg": "maps_levels/4/4_level_bg.csv",
           "nature2": "maps_levels/4/4_level_nature2.csv"}
menu_music = ''
CON = sqlite3.connect("game.db")
CUR = CON.cursor()
VOLUME = 0.5

levels = [level_1, level_2, level_3, level_4]

levels_selector = ['1 уровень', '2 уровень', '3 уровень', '4 уровень']


class Game:
    def __init__(self, screen):
        global DIFFICULTY
        # print(DIFFICULTY)
        # game attributes
        for i in range(DIFFICULTY + 1, 5):
            CUR.execute(f"UPDATE games_name SET '{int(i)}' = ''"
                        f" WHERE name == '{user_name.get_value()}'")
        CON.commit()
        change_username()

        data = CUR.execute(
            f"""SELECT "1", "2", "3", "4" FROM games_name WHERE name == '{user_name.get_value()}'""").fetchall()[0]
        # print(data, "DA")
        # print(DIFFICULTY, "уровень")
        dif = DIFFICULTY
        try:
            self.cur_health = int((data[dif - 1]).split(',')[0])
            self.coins = int((data[dif - 1]).split(',')[1])
        except Exception as e:
            self.cur_health = 100
            self.coins = 0
        # print(DIFFICULTY, "after")

        self.life = True
        self.max_health = 100

        # audio
        self.new_level = 0  # значения от 0 до 2: 0 - процесс, 1 - переход на след уровень, 2 - конец
        self.level_bg_music = pygame.mixer.Sound('music/level_music.wav')
        self.level_bg_music.set_volume(VOLUME)

        # user interface
        self.screen = screen
        self.ui = UI(self.screen)
        self.create_level(levels[DIFFICULTY])

    def create_level(self, current_level):
        self.level = Level(current_level, self.screen, self.change_coins, self.change_health, self.change_life, VOLUME,
                           self.change_level)

    def change_coins(self, amount):
        self.coins += amount

    def change_health(self, amount):
        self.cur_health += amount

    def change_life(self):
        """при попадании в воду ничего не меняется"""
        self.life = False

    def change_level(self):
        global DIFFICULTY
        if DIFFICULTY != 3:
            self.new_level = 1
            DIFFICULTY = DIFFICULTY + 1
            # print("level += 1")

        else:
            self.new_level = 2  # "конец"
            # print("ККККООООНННННЕЦЦЦЦ")

    def run(self):
        self.level.run()
        self.ui.show_health(self.cur_health, self.max_health)
        self.ui.show_coins(self.coins)
        # self.check_game_over()


# Constants and global variables
ABOUT = [f'pygame-menu {pygame_menu.__version__}',
         f'Author: kattterina_i']
DIFFICULTY = 0
FPS = 60
WINDOW_SIZE = (1200, 704)

clock: Optional['pygame.time.Clock'] = None
main_menu: Optional['pygame_menu.Menu'] = None
surface: Optional['pygame.Surface'] = None


def change_difficulty(value: Tuple[Any, int], difficulty) -> None:
    global DIFFICULTY
    DIFFICULTY = int(difficulty)


def random_color() -> Tuple[int, int, int]:
    """
    Return a random color.
    :return: Color tuple
    """
    return randrange(0, 255), randrange(0, 255), randrange(0, 255)


def Game_over(screen, coins):
    fon = pygame.transform.scale(load_image('picture/fons/fon0.jpg'), (screen_width, screen_height))
    screen.blit(fon, (0, 0))

    font = pygame.font.Font('picture/ITC.ttf', 80)
    string_rendered = font.render("Конец", False, (255, 255, 255))
    intro_rect = string_rendered.get_rect(center=(600, 300))
    screen.blit(string_rendered, intro_rect)

    font = pygame.font.Font('picture/ITC.ttf', 30)
    coin = load_image('picture/berry_coins/1.png')
    coin_amount_surf = font.render(f"Твой результат: {coins}", False, (255, 255, 255))
    coin_amount_rect = coin_amount_surf.get_rect(center=(600, 500))
    screen.blit(coin_amount_surf, coin_amount_rect)
    coin_rect = coin.get_rect(topleft=(coin_amount_rect.right + 4, coin_amount_rect.y + 6))
    screen.blit(coin, coin_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def play_function(level='', test: bool = False) -> None:
    global surface, main_menu, menu_music, user_name, selector, DIFFICULTY
    if not user_name.get_value():
        return
    # print(level, 'Level')
    # print("dafsf", DIFFICULTY)
    if level:
        DIFFICULTY = level
    """
    
    Main game function.
    :param difficulty: Difficulty of the game
    :param font: Pygame font
    :param test: Test method, if ``True`` only one loop is allowed
    """
    # pygame.quit()
    # pygame.init()
    # main_menu.close()
    # print(user_name.get_value())
    main_menu.disable()
    main_menu.full_reset()

    menu_music.stop()
    screen = pygame.display.set_mode((screen_width, screen_height))
    game = Game(screen)
    game.level_bg_music.play(loops=-1)

    pygame.display.set_caption('Платформер')
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                surface = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE, 32)
                menu_music.play(loops=-1)
                game.level_bg_music.stop()
                main_menu.enable()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    surface = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE, 32)
                    menu_music.play(loops=-1)
                    game.level_bg_music.stop()
                    main_menu.enable()
                    return
        game.run()
        if game.cur_health <= 0:
            # удаление данных об уровнях
            for i in range(len(levels_selector)):
                CUR.execute(f"UPDATE games_name SET '{str(i + 1)}' = '' WHERE name == '{user_name.get_value()}'")
            CON.commit()
            change_username()

            surface = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE, 32)
            menu_music.play(loops=-1)
            game.level_bg_music.stop()
            main_menu.enable()
            return
        if not game.life:
            surface = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE, 32)
            menu_music.play(loops=-1)
            game.level_bg_music.stop()
            main_menu.enable()
            return
        if game.new_level == 1:
            CUR.execute(f"UPDATE games_name SET '{int(DIFFICULTY)}' = '{game.cur_health},{game.coins}'"
                        f" WHERE name == '{user_name.get_value()}'")
            CON.commit()
            change_username()
            game.level_bg_music.stop()
            play_function()
            # selector.set_value(levels_selector[DIFFICULTY + 1])
            return
        if game.new_level == 2:
            # print(int(DIFFICULTY), "END")
            CUR.execute(f"UPDATE games_name SET '{int(DIFFICULTY) + 1}' = '{game.cur_health},{game.coins}'"
                        f" WHERE name == '{user_name.get_value()}'")
            CON.commit()
            CUR.execute(f"UPDATE games_name SET 'total' = {game.coins}"
                        f" WHERE name == '{user_name.get_value()}'")
            CON.commit()
            Game_over(screen, game.coins)
            menu_music.play(loops=-1)
            game.level_bg_music.stop()
            main_menu.enable()
            return
        clock.tick(60)

        if main_menu.is_enabled():
            main_menu.update(pygame.event.get())
            # Continue playing
        pygame.display.flip()


def change_data(*args, **kwargs) -> None:
    global VOLUME, menu_music

    VOLUME = args[0] / 100
    menu_music.set_volume(VOLUME)
    pass


def main_background() -> None:
    """
    Function used by menus, draw on background while menu is active.
    """
    global surface
    fon = pygame.transform.scale(load_image('picture/fons/fon0.jpg'), (screen_width, screen_height))
    surface.blit(fon, (0, 0))
    # surface.fill((128, 0, 128))


def change_username(*args):
    global user_name, selector, DIFFICULTY
    data = CUR.execute(f"""SELECT * FROM games_name WHERE name == '{user_name.get_value()}'""").fetchall()
    # print(1)
    BUTTONS[0].show()
    if not data:
        for i in BUTTONS[1::]:
            i.hide()
        CUR.execute(
            f"""INSERT INTO games_name(name) VALUES('{user_name.get_value()}')""")
        DIFFICULTY = 0
        CON.commit()
        selector.hide()
    else:
        # print(data[0][1:-2], "есть")
        for i, j in enumerate(data[0][1:-2]):
            if j:
                BUTTONS[i].show()
            else:
                # print('нет уровня', i)
                # START_GAME = i
                BUTTONS[i].show()
                [x.hide() for x in BUTTONS[i::]]
                selector.hide()
                DIFFICULTY = i - 1
                return
        selector.show()


BUTTONS = []



def main(test: bool = False) -> None:
    """
    Main program.
    :param test: Indicate function is being tested
    """

    # -------------------------------------------------------------------------
    # Globals
    # -------------------------------------------------------------------------
    global clock
    global main_menu
    global surface, menu_music, user_name, selector
    # -------------------------------------------------------------------------
    # Create window
    # -------------------------------------------------------------------------
    surface = create_example_window('Платформер', WINDOW_SIZE)
    clock = pygame.time.Clock()
    menu_music = pygame.mixer.Sound('music/menu.wav')
    menu_music.set_volume(VOLUME)
    menu_music.play(loops=-1)

    # -------------------------------------------------------------------------
    # Create menus: Play Menu
    # -------------------------------------------------------------------------

    mytheme = pygame_menu.themes.THEME_DEFAULT.copy()
    mytheme.title_background_color = (0, 0, 0)
    mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
    mytheme.background_color = (190, 190, 190, 5)
    mytheme.widget_font_color  = (190, 190, 190)
    # -------------------------------------------------------------------------
    # Create menus:About
    # -------------------------------------------------------------------------
    about_theme = mytheme.copy()
    about_theme.widget_margin = (0, 0)

    about_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.6,
        theme=about_theme,
        title='О программе',
        width=WINDOW_SIZE[0] * 0.6
    )

    for m in ABOUT:
        about_menu.add.label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
    about_menu.add.vertical_margin(30)
    about_menu.add.button('Вернуться', pygame_menu.events.BACK)

    # -------------------------------------------------------------------------
    # Create menus: Main
    # -------------------------------------------------------------------------
    # main_theme = pygame_menu.themes.THEME_DEFAULT.copy()

    main_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.7,
        theme=mytheme,
        title='Главное меню',
        width=WINDOW_SIZE[0] * 0.7
    )

    main_menu.add.button('Начать', play_function)
    user_name = main_menu.add.text_input('Имя: ', default='', onreturn=change_username, maxchar=10)
    main_menu.add.button('О программе', about_menu)
    play_submenu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.5,
        theme=mytheme,
        title='Уровни',
        width=WINDOW_SIZE[0] * 0.7
    )
    for i in range(4):
        BUTTONS.append(play_submenu.add.button(f'Уровень {i + 1}', play_function, i))

    # for i in range(4):
    #     if i in [0]:
    #         play_submenu.add.button(f'Level {i + 1}', pygame_menu.events.BACK, i, font_color=(234, 44, 66))
    #     else:
    #         play_submenu.add.button(f'Level {i + 1}', play_function, i)

    play_submenu.add.button('Вернуться', pygame_menu.events.RESET)

    selector = main_menu.add.selector('Уровни',
                                      [('1 уровень', 0),
                                       ('2 уровень', 1),
                                       ('3 уровень', 2),
                                       ('4 уровень', 3)],
                                      onchange=change_difficulty,
                                      selector_id='select_difficulty')
    main_menu.add.range_slider('Громкость', 50, (0, 100), 1,
                               rangeslider_id='range_slider',
                               value_format=lambda x: str(int(x)),
                               onchange=change_data)
    main_menu.add.button('Уровни', play_submenu)

    main_menu.add.button('Выход', pygame_menu.events.EXIT)

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:

        # Tick
        clock.tick(FPS)

        # Paint background
        main_background()

        # Application events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        # Main menu
        if main_menu.is_enabled():
            main_menu.mainloop(surface, main_background, disable_loop=test, fps_limit=FPS)

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break


if __name__ == '__main__':
    main()

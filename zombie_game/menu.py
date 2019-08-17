from os import path

from zombie_game.drawable import Drawable
from zombie_game.functions import quit_game
from zombie_game.settings import *


class MenuMob(Drawable, pg.sprite.Sprite):

    def __init__(self, game, x, y, width=20, height=20):
        super(MenuMob, self).__init__(width, height, x, y)
        pg.sprite.Sprite.__init__(self)
        self.image = self.surface
        self.game = game
        self.width = width
        self.height = height
        self.pic = None

    def animate(self, destination, area):
        self.pic = pg.image.load(path.join(self.game.img_folder, INTRO_IMG))
        self.pic = pg.transform.scale(self.pic, (self.width, self.height))
        self.surface.blit(self.pic, destination, area)


class Menu:

    def __init__(self, game):
        self.game = game
        self.pos_x = 0
        self.pos_y = 0
        self.i = 0

    def game_intro(self):
        self.i = 0.56
        self.set_mob_limit(0.1, 337, 480, INTRO_SPRITE_POS_X, self.game.board.draw_menu, self.game_options, 40)
        if 335 < self.pos_y < 337:
            self.game_choose_character()
        elif 385 < self.pos_y < 397:
            self.game_options()
        elif 455 < self.pos_y < 457:
            self.game_options()
        else:
            quit_game()

    def game_options(self):
        self.i = 0.31
        self.set_mob_limit(0.15, 196, 366, OPTIONS_SPRITE_POS_X, self.game.board.draw_options, self.game_intro)
        if 185 < self.pos_y < 187:
            # controls
            pass
        elif 275 < self.pos_y < 277:
            pass
            # audio
        else:
            self.game_intro()

    def game_choose_character(self):
        self.i = 0.45
        self.set_mob_limit(0.15, 275, 445, OPTIONS_SPRITE_POS_X, self.game.board.draw_choose_character, self.game_intro)
        if 265 < self.pos_y < 275:
            self.game.character_type = 'hitman1_'
            self.game_choosing_difficulty()
        elif 355 < self.pos_y < 365:
            self.game.character_type = 'womanGreen_'
            self.game_choosing_difficulty()
        else:
            self.game.character_type = 'soldier1_'
            self.game_choosing_difficulty()

    def game_choosing_difficulty(self):
        self.i = 0.16
        self.set_mob_limit(0.2, 97, 455, OPTIONS_SPRITE_POS_X, self.game.board.draw_choosing_difficulty, self.game_choose_character)
        if 95 < self.pos_y < 97:
            difficult = "easy"
        elif 215 < self.pos_y < 217:
            difficult = "normal"
        elif 335 < self.pos_y < 337:
            difficult = "hard"
        else:
            difficult = "hell"
        self.game_input(difficult)

    def game_input(self, difficult):
        word = ""
        while True:
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit_game()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.game_choosing_difficulty()
                    if event.unicode.isalpha():
                        word += event.unicode
                    if event.key == pg.K_BACKSPACE:
                        word = word[:-1]
                    if event.key == pg.K_RETURN:
                        if len(word) > 0:
                            self.game.run(difficult, word)
                self.game.board.draw_input(word, self.game.width / 2, self.game.height / 2)

    def game_over(self, scoreboard, message):
        while True:
            self.game.board.draw_game_over(scoreboard, message)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit_game()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE or event.key == pg.K_RETURN:
                        self.game_intro()

    def set_mob_limit(self, i_value, top, bottom, pos, draw, previous, size=50):
        while True:
            self.set_position(pos)
            draw(self.set_the_mob(size))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit_game()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        quit_game()
                    if event.key == pg.K_ESCAPE or event.key == pg.K_BACKSPACE:
                        previous()
                    if event.key == pg.K_UP or event.key == pg.K_w:
                        if self.pos_y > top:
                            self.i -= i_value
                    if event.key == pg.K_DOWN or event.key == pg.K_s:
                        if self.pos_y < bottom:
                            self.i += i_value
                    if event.key == pg.K_SPACE or event.key == pg.K_RETURN:
                        return False

    def set_position(self, x):
        self.pos_y = self.game.height * self.i
        self.pos_x = self.game.width * x

    def set_the_mob(self, size=50):
        intro_object = MenuMob(self.game, self.pos_x, self.pos_y, size, size)
        intro_object.animate((0, 0), (0, 0, self.pos_x, self.pos_y))
        return intro_object


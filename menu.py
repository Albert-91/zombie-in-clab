from os import path
from drawable import Drawable
from settings import *
from functions import quit


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


class Menu(Drawable):

    def __init__(self, game):
        self.game = game

    def game_intro(self):
        i = 0.56
        while True:
            mark_pos_y = self.game.height * i
            mark_pos_x = self.game.width * INTRO_SPRITE_POS_X
            intro_object = MenuMob(self.game, mark_pos_x, mark_pos_y, 40, 40)
            intro_object.animate((0, 0), (0, 0, mark_pos_x, mark_pos_y))
            self.game.board.draw_menu(intro_object)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        quit()
                    if event.key == pg.K_UP or event.key == pg.K_w:
                        if mark_pos_y > 337:
                            i -= 0.1
                    if event.key == pg.K_DOWN or event.key == pg.K_s:
                        if mark_pos_y < 455:
                            i += 0.1
                    if event.key == pg.K_SPACE or event.key == pg.K_RETURN:
                        if 335 < mark_pos_y < 337:
                            self.game_choosing_difficulty()
                        elif 385 < mark_pos_y < 397:
                            self.game_options()
                        else:
                            quit()

    def game_options(self):
        i = 0.31
        while True:
            mark_pos_y = self.game.height * i
            mark_pos_x = self.game.width * OPTIONS_SPRITE_POS_X
            intro_object = MenuMob(self.game, mark_pos_x, mark_pos_y, 50, 50)
            intro_object.animate((0, 0), (0, 0, mark_pos_x, mark_pos_y))
            self.game.board.draw_options(intro_object)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE or event.key == pg.K_BACKSPACE:
                        self.game_intro()
                    if event.key == pg.K_UP or event.key == pg.K_w:
                        if mark_pos_y > 196:
                            i -= 0.15
                    if event.key == pg.K_DOWN or event.key == pg.K_s:
                        if mark_pos_y < 366:
                            i += 0.15
                    if event.key == pg.K_SPACE or event.key == pg.K_RETURN:
                        if 185 < mark_pos_y < 187:
                            """controls"""
                        elif 275 < mark_pos_y < 277:
                            """audio"""
                        else:
                            self.game_intro()

    def game_choosing_difficulty(self):
        i = 0.16
        while True:
            mark_pos_y = self.game.height * i
            mark_pos_x = self.game.width * DIFFICULT_SPRITE_POS_X
            intro_object = MenuMob(self.game, mark_pos_x, mark_pos_y, 50, 50)
            intro_object.animate((0, 0), (0, 0, mark_pos_x, mark_pos_y))
            self.game.board.draw_choosing_difficulty(intro_object)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE or event.key == pg.K_BACKSPACE:
                        self.game_intro()
                    if event.key == pg.K_UP or event.key == pg.K_w:
                        if mark_pos_y > 97:
                            i -= 0.2
                    if event.key == pg.K_DOWN or event.key == pg.K_s:
                        if mark_pos_y < 455:
                            i += 0.2
                    if event.key == pg.K_SPACE or event.key == pg.K_RETURN:
                        if 95 < mark_pos_y < 97:
                            difficult = "easy"
                        elif 215 < mark_pos_y < 217:
                            difficult = "normal"
                        elif 335 < mark_pos_y < 337:
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
                    quit()
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

    def game_over(self, word, scoreboard):
        while True:
            self.game.board.draw_game_over(word)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE or event.key == pg.K_RETURN:
                        self.game_intro()

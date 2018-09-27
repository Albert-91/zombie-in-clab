from drawable import Drawable
from player import Player
from settings import *
from functions import quit


class Menu(Drawable):

    def __init__(self, game):
        self.game = game
        self.name = ""
        self.intro_img = game.intro_img

    def game_intro(self):
        i = 0.56
        while True:
            mark_pos_y = self.game.height * i
            mark_pos_x = self.game.width * INTRO_SPRITE_POS_X
            intro_object = Player(self.game, mark_pos_x, mark_pos_y)
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
            intro_object = Player(self.game, mark_pos_x, mark_pos_y)
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
            intro_object = Player(self.game, mark_pos_x, mark_pos_y)
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
                            difficulty = "easy"
                        elif 215 < mark_pos_y < 217:
                            difficulty = "normal"
                        elif 335 < mark_pos_y < 337:
                            difficulty = "hard"
                        else:
                            difficulty = "hell"

                        self.game_input(difficulty)

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
                            self.name = word
                            return self.game.run(difficult)
                self.game.board.draw_input(word, self.game.width / 2, self.game.height / 2)

    def game_over(self):
        while True:
            self.game.board.draw_game_over(self.name)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE or event.key == pg.K_RETURN:
                        self.game_intro()

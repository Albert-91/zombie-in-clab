import pygame
from settings import *


class Board:

    def __init__(self, width, height):
        self.surface = pygame.display.set_mode((width, height), 0, 32)
        pygame.display.set_caption('Zombie in CLab')
        self.width = width
        self.height = height
        self.intro_bg = pygame.image.load("images/intro.jpg")
        my_font = "font/Exquisite Corpse.ttf"
        self.menu_font = pygame.font.Font(my_font, 45)
        self.options_font = pygame.font.Font(my_font, 65)
        self.title_font = pygame.font.Font(my_font, 90)
        self.difficulty_font = pygame.font.Font(my_font, 70)
        self.game_over_font = pygame.font.Font(my_font, 150)

    def draw_menu(self, object):
        self.intro_bg = pygame.transform.scale(self.intro_bg, (self.width, self.height))
        self.surface.blit(self.intro_bg, (0, 0), (0, 0, self.width, self.height))
        self.draw_text(self.surface, "Zombie in CLab", self.width / 2, self.height * 0.3,
                       self.title_font)
        self.draw_text(self.surface, "Play", self.width / 2, self.height * 0.6, self.menu_font)
        self.draw_text(self.surface, "Options", self.width / 2, self.height * 0.7, self.menu_font)
        self.draw_text(self.surface, "Quit", self.width / 2, self.height * 0.8, self.menu_font)
        object.draw_on(object.surface)
        pygame.display.update()

    def draw_options(self, *args):
        self.intro_bg = pygame.transform.scale(self.intro_bg, (self.width, self.height))
        self.surface.blit(self.intro_bg, (0, 0), (0, 0, self.width, self.height))
        self.draw_text(self.surface, "Controls", self.width / 2, self.height * 0.35, self.options_font)
        self.draw_text(self.surface, "Audio", self.width / 2, self.height * 0.5, self.options_font)
        self.draw_text(self.surface, "Return", self.width / 2, self.height * 0.65, self.options_font)
        # for drawable in args:
        #     drawable.draw_on(self.surface)

        pygame.display.update()

    def draw_game_over(self, name, *args):
        background = (0, 0, 0)
        self.surface.fill(background)
        self.draw_text(self.surface, "Game over", self.width / 2, self.height * 0.4,
                       self.game_over_font)
        # for drawable in args:
        #     drawable.draw_on(self.surface)

        pygame.display.update()

    def draw_choosing_difficulty(self, *args):
        self.intro_bg = pygame.transform.scale(self.intro_bg, (self.width, self.height))
        self.surface.blit(self.intro_bg, (0, 0), (0, 0, self.width, self.height))
        self.draw_text(self.surface, "Easy", self.width / 2, self.height * 0.2, self.difficulty_font)
        self.draw_text(self.surface, "Normal", self.width / 2, self.height * 0.4, self.difficulty_font)
        self.draw_text(self.surface, "Hard", self.width / 2, self.height * 0.6, self.difficulty_font)
        self.draw_text(self.surface, "Zombie hell!", self.width / 2, self.height * 0.8, self.difficulty_font)
        # for drawable in args:
        #     drawable.draw_on(self.surface)

        pygame.display.update()

    def draw_input(self, word, x, y):
        self.surface.fill((0, 0, 0))
        self.draw_text(self.surface, "Please enter your name:", self.width / 2, self.height / 3, self.menu_font)
        text = self.menu_font.render("{}".format(word), True, MENU_FONT_COLOR)
        rect = text.get_rect()
        rect.center = x, y
        pygame.display.update()
        return self.surface.blit(text, rect)

    @staticmethod
    def draw_text(surface, text, x, y, font):
        text = font.render(text, True, MENU_FONT_COLOR)
        rect = text.get_rect()
        rect.center = x, y
        surface.blit(text, rect)

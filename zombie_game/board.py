from zombie_game.settings import *


class Board:

    def __init__(self, width: int, height: int):
        self.surface = pg.display.set_mode((width, height), 0, 32)
        pg.display.set_caption('Zombie in CLab')
        self.width = width
        self.height = height
        self.intro_bg = pg.image.load("images/intro.jpg")
        my_font = "font/Exquisite Corpse.ttf"
        self.menu_font = pg.font.Font(my_font, 45)
        self.bonus_font = pg.font.Font(my_font, 30)
        self.options_font = pg.font.Font(my_font, 65)
        self.title_font = pg.font.Font(my_font, 90)
        self.difficulty_font = pg.font.Font(my_font, 70)
        self.game_over_font = pg.font.Font(my_font, 120)

    def draw_menu(self, *args):
        self.intro_bg = pg.transform.scale(self.intro_bg, (self.width, self.height))
        self.surface.blit(self.intro_bg, (0, 0), (0, 0, self.width, self.height))
        self.draw_text(self.surface, "Zombie in CLab", self.width / 2, self.height * 0.3, self.title_font)
        self.draw_text(self.surface, "Play", self.width / 2, self.height * 0.6, self.menu_font)
        self.draw_text(self.surface, "Ranking", self.width / 2, self.height * 0.7, self.menu_font)
        self.draw_text(self.surface, "Options", self.width / 2, self.height * 0.8, self.menu_font)
        self.draw_text(self.surface, "Quit", self.width / 2, self.height * 0.9, self.menu_font)
        for drawable in args:
            drawable.draw_on(self.surface)
        pg.display.update()

    def draw_options(self, *args):
        self.intro_bg = pg.transform.scale(self.intro_bg, (self.width, self.height))
        self.surface.blit(self.intro_bg, (0, 0), (0, 0, self.width, self.height))
        self.draw_text(self.surface, "Controls", self.width / 2, self.height * 0.35, self.options_font)
        self.draw_text(self.surface, "Audio", self.width / 2, self.height * 0.5, self.options_font)
        self.draw_text(self.surface, "Return", self.width / 2, self.height * 0.65, self.options_font)
        for drawable in args:
            drawable.draw_on(self.surface)
        pg.display.update()

    def draw_choose_character(self, *args):
        self.intro_bg = pg.transform.scale(self.intro_bg, (self.width, self.height))
        self.surface.blit(self.intro_bg, (0, 0), (0, 0, self.width, self.height))
        self.draw_text(self.surface, "Choose your character:", self.width / 2, self.height * 0.2, self.difficulty_font)
        self.draw_text(self.surface, "Hitman", self.width / 2, self.height * 0.5, self.options_font)
        self.draw_text(self.surface, "Girl", self.width / 2, self.height * 0.65, self.options_font)
        self.draw_text(self.surface, "Soldier", self.width / 2, self.height * 0.8, self.options_font)
        for drawable in args:
            drawable.draw_on(self.surface)
        pg.display.update()

    def draw_game_over(self, scoreboard: list, message: str, *args):
        background = (0, 0, 0)
        self.surface.fill(background)
        self.draw_text(self.surface, message, self.width / 2, self.height * 0.2, self.game_over_font)
        self.draw_text(self.surface, "Players with the best accuracy:", self.width / 2, self.height * 0.4, self.menu_font)
        pos = 0.5
        for player in scoreboard:
            self.draw_text(self.surface, player[0], self.width / 3, self.height * pos, self.bonus_font)
            self.draw_text(self.surface, player[1], self.width * 2 / 3, self.height * pos, self.bonus_font)
            pos += 0.08
        for drawable in args:
            drawable.draw_on(self.surface)
        pg.display.update()

    def draw_choosing_difficulty(self, *args):
        self.intro_bg = pg.transform.scale(self.intro_bg, (self.width, self.height))
        self.surface.blit(self.intro_bg, (0, 0), (0, 0, self.width, self.height))
        self.draw_text(self.surface, "Easy", self.width / 2, self.height * 0.2, self.difficulty_font)
        self.draw_text(self.surface, "Normal", self.width / 2, self.height * 0.4, self.difficulty_font)
        self.draw_text(self.surface, "Hard", self.width / 2, self.height * 0.6, self.difficulty_font)
        self.draw_text(self.surface, "Zombie hell!", self.width / 2, self.height * 0.8, self.difficulty_font)
        for drawable in args:
            drawable.draw_on(self.surface)

        pg.display.update()

    def draw_input(self, word: str, x: int, y: int):
        self.surface.fill((0, 0, 0))
        self.draw_text(self.surface, "Please enter your name:", self.width / 2, self.height / 3, self.menu_font)
        text = self.menu_font.render("{}".format(word), True, MENU_FONT_COLOR)
        rect = text.get_rect()
        rect.center = x, y
        pg.display.update()
        return self.surface.blit(text, rect)

    def draw_pause(self):
        self.draw_text(self.surface, "Paused", self.width / 2, self.height / 2, self.title_font)

    def draw_zombies_left(self, left: int):
        self.draw_text(self.surface, "Zombies: {}".format(left), self.width - 100, 25, self.bonus_font)

    def draw_bonus(self, bonus: str):
        self.draw_text(self.surface, bonus, self.width - 300, 25, self.bonus_font)

    def draw_ammo_quantity(self, ammo: str):
        self.draw_text(self.surface, ammo, 400, 25, self.bonus_font)

    def draw_money(self):
        self.draw_text(self.surface, "9 800 zl", self.width - 100, 60, self.bonus_font)

    @staticmethod
    def draw_adds(surface, x, y, image, amount=1):
        for i in range(amount):
            img_rect = image.get_rect()
            img_rect.x = x + 30 * i
            img_rect.y = y
            surface.blit(image, img_rect)

    @staticmethod
    def draw_text(surface, text, x, y, font):
        if text is not None:
            text = font.render(text, True, MENU_FONT_COLOR)
            rect = text.get_rect()
            rect.center = x, y
            surface.blit(text, rect)

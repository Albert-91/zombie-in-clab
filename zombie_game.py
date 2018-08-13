import pygame
from random import randint
import math
from player import Player
from rooms import Rooms
from zombie import Zombie


class Board:

    def __init__(self, width, height):
        self.surface = pygame.display.set_mode((width, height), 0, 32)
        pygame.display.set_caption('Zombie in CLab')
        self.bg = pygame.image.load("images/terrain_atlas.png")
        self.intro_bg = pygame.image.load("images/intro.jpg")
        my_font = "font/Exquisite Corpse.ttf"
        self.menu_font = pygame.font.Font(my_font, 45)
        self.options_font = pygame.font.Font(my_font, 65)
        self.title_font = pygame.font.Font(my_font, 90)
        self.difficulty_font = pygame.font.Font(my_font, 70)
        self.game_over_font = pygame.font.Font(my_font, 150)

    def draw(self, *args):
        background = (255, 255, 255)
        self.surface.fill(background)
        self.surface.blit(self.bg, (200, 200), (0, 0, 90, 150))
        for drawable in args:
            drawable.draw_on(self.surface)

    def draw_menu(self, *args):
        self.intro_bg = pygame.transform.scale(self.intro_bg, (TheGame.game_width, TheGame.game_height))
        self.surface.blit(self.intro_bg, (0, 0), (0, 0, TheGame.game_width, TheGame.game_height))
        self.draw_text(self.surface, "Zombie in CLab", TheGame.game_width / 2, TheGame.game_height * 0.3,
                       self.title_font)
        self.draw_text(self.surface, "Play", TheGame.game_width / 2, TheGame.game_height * 0.6, self.menu_font)
        self.draw_text(self.surface, "Options", TheGame.game_width / 2, TheGame.game_height * 0.7, self.menu_font)
        self.draw_text(self.surface, "Quit", TheGame.game_width / 2, TheGame.game_height * 0.8, self.menu_font)
        for drawable in args:
            drawable.draw_on(self.surface)

        pygame.display.update()

    def draw_options(self, *args):
        self.intro_bg = pygame.transform.scale(self.intro_bg, (TheGame.game_width, TheGame.game_height))
        self.surface.blit(self.intro_bg, (0, 0), (0, 0, TheGame.game_width, TheGame.game_height))
        self.draw_text(self.surface, "Controls", TheGame.game_width / 2, TheGame.game_height * 0.35, self.options_font)
        self.draw_text(self.surface, "Audio", TheGame.game_width / 2, TheGame.game_height * 0.5, self.options_font)
        self.draw_text(self.surface, "Return", TheGame.game_width / 2, TheGame.game_height * 0.65, self.options_font)
        for drawable in args:
            drawable.draw_on(self.surface)

        pygame.display.update()

    def draw_game_over(self, *args):
        background = (0, 0, 0)
        self.surface.fill(background)
        self.draw_text(self.surface, "Game over", TheGame.game_width / 2, TheGame.game_height * 0.4,
                       self.game_over_font)
        for drawable in args:
            drawable.draw_on(self.surface)

        pygame.display.update()

    def draw_choosing_difficulty(self, *args):
        self.intro_bg = pygame.transform.scale(self.intro_bg, (TheGame.game_width, TheGame.game_height))
        self.surface.blit(self.intro_bg, (0, 0), (0, 0, TheGame.game_width, TheGame.game_height))
        self.draw_text(self.surface, "Easy", TheGame.game_width / 2, TheGame.game_height * 0.2, self.difficulty_font)
        self.draw_text(self.surface, "Normal", TheGame.game_width / 2, TheGame.game_height * 0.4, self.difficulty_font)
        self.draw_text(self.surface, "Hard", TheGame.game_width / 2, TheGame.game_height * 0.6, self.difficulty_font)
        self.draw_text(self.surface, "Zombie hell!", TheGame.game_width / 2, TheGame.game_height * 0.8,
                       self.difficulty_font)
        for drawable in args:
            drawable.draw_on(self.surface)

        pygame.display.update()

    @staticmethod
    def draw_text(surface, text, x, y, font):
        text = font.render(text, True, (255, 0, 0))
        rect = text.get_rect()
        rect.center = x, y
        surface.blit(text, rect)


class TheGame:
    game_width = None
    game_height = None

    def __init__(self, width, height):
        pygame.init()
        self.set_angle = 180
        self.turn_to_shoot = "down"
        TheGame.game_width = width
        TheGame.game_height = height
        self.width = width
        self.height = height
        self.number_of_zombies = 20
        self.board = Board(width, height)
        self.fps_clock = pygame.time.Clock()
        self.room = Rooms(0, 0)
        self.player = Player(width / 2, height / 2, 26, 26)
        self.zombie_group = pygame.sprite.Group()
        self.all_sprites_group = pygame.sprite.Group()
        self.other_group = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.all_sprites_group.add(self.player)
        for i in range(self.number_of_zombies):
            x = randint(self.player.width, TheGame.game_width - self.player.width)
            y = randint(self.player.height, TheGame.game_height - self.player.height)
            self.zombie_person = Zombie(x, y, self.player, 23, 28, self.width, self.height)
            self.zombie_group.add(self.zombie_person)
            self.other_group.add(self.zombie_person)
            self.all_sprites_group.add(self.zombie_person)

    def game_intro(self):
        i = 0.56
        while True:
            mark_pos_y = TheGame.game_height * i
            mark_pos_x = TheGame.game_width * 0.37
            intro_object = Player(mark_pos_x, mark_pos_y, 40, 40)
            intro_object.animation("images/menu_head.png", (0, 0), (0, 0, mark_pos_x, mark_pos_y), False)
            self.board.draw_menu(intro_object)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        if mark_pos_y > 337:
                            i -= 0.1
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if mark_pos_y < 455:
                            i += 0.1
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        if 335 < mark_pos_y < 337:
                            game.game_choosing_difficulty()
                        elif 385 < mark_pos_y < 397:
                            game.game_options()
                        else:
                            pygame.quit()

    def game_options(self):
        i = 0.31
        while True:
            mark_pos_y = TheGame.game_height * i
            mark_pos_x = TheGame.game_width * 0.3
            intro_object = Player(mark_pos_x, mark_pos_y, 45, 45)
            intro_object.animation("images/menu_head.png", (0, 0), (0, 0, mark_pos_x, mark_pos_y), False)
            self.board.draw_options(intro_object)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                        game.game_intro()
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        if mark_pos_y > 196:
                            i -= 0.15
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if mark_pos_y < 366:
                            i += 0.15
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        if 185 < mark_pos_y < 187:
                            """controls"""
                        elif 275 < mark_pos_y < 277:
                            """audio"""
                        else:
                            game.game_intro()

    def game_choosing_difficulty(self):
        i = 0.16
        while True:
            mark_pos_y = TheGame.game_height * i
            mark_pos_x = TheGame.game_width * 0.25
            intro_object = Player(mark_pos_x, mark_pos_y, 40, 40)
            intro_object.animation("images/menu_head.png", (0, 0), (0, 0, mark_pos_x, mark_pos_y), False)
            self.board.draw_choosing_difficulty(intro_object)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                        game.game_intro()
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        if mark_pos_y > 97:
                            i -= 0.2
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if mark_pos_y < 455:
                            i += 0.2
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        if 95 < mark_pos_y < 97:
                            difficulty = "easy"
                        elif 215 < mark_pos_y < 217:
                            difficulty = "normal"
                        elif 335 < mark_pos_y < 337:
                            difficulty = "hard"
                        else:
                            difficulty = "hell"

                        game.run(difficulty)

    def game_over(self):
        while True:
            self.board.draw_game_over()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        return False

    def run(self, difficulty):
        max_distance = 170
        if difficulty == "easy":
            zombie_speed = 1
            zombie_attack = 1
        elif difficulty == "normal":
            zombie_speed = 1.2
            zombie_attack = 2
        elif difficulty == "hard":
            zombie_speed = 1.5
            zombie_attack = 3
        else:
            zombie_speed = 1.7
            zombie_attack = 4
        while True:
            dead = False
            self.handle_events()
            for self.zombie_person in self.zombie_group:
                self.zombie_person.animation("images/zombies.png", (0, 0), (5, 1, 23, 29))
                distance = (self.zombie_person.rect.x - self.player.rect.x) ** 2 + \
                           (self.zombie_person.rect.y - self.player.rect.y) ** 2
                distance = math.sqrt(distance)
                if distance > max_distance:
                    self.zombie_person.zombie_natural_moves()
                elif distance <= max_distance and not pygame.sprite.collide_rect(self.zombie_person, self.player):
                    self.zombie_person.zombie_follows(zombie_speed)
                else:
                    self.zombie_person.zombie_attacks(zombie_attack)
                for bullet in self.bullets:
                    if pygame.sprite.collide_rect(self.zombie_person, bullet):
                        self.zombie_person.kill()
                        dead = True
                for other_zombie in self.other_group:
                    if other_zombie != self.zombie_person and \
                            pygame.sprite.collide_rect(self.zombie_person, other_zombie):
                        if other_zombie.rect.x > self.zombie_person.rect.x:
                            other_zombie.move_x(- zombie_speed, TheGame.game_width)
                            self.zombie_person.move_x(zombie_speed, TheGame.game_width)
                        else:
                            other_zombie.move_x(zombie_speed, TheGame.game_width)
                            self.zombie_person.move_x(- zombie_speed, TheGame.game_width)
                        if other_zombie.rect.y > self.zombie_person.rect.y:
                            other_zombie.move_y(- zombie_speed, TheGame.game_height)
                            self.zombie_person.move_y(zombie_speed, TheGame.game_height)
                        else:
                            other_zombie.move_y(zombie_speed, TheGame.game_height)
                            self.zombie_person.move_y(- zombie_speed, TheGame.game_height)

            self.board.draw(self.room)
            self.player.animation("images/character.png", (0, 0), (14, 11, 20, 39))
            self.all_sprites_group.draw(self.board.surface)
            self.all_sprites_group.update(self.turn_to_shoot, dead, self.width, self.height)
            self.bullets.update(self.turn_to_shoot, dead, self.width, self.height)
            pygame.display.flip()
            self.fps_clock.tick(80)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                return True

            elif event.type == pygame.KEYUP:
                """activate continuous moves by pressing buttons"""
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    pygame.key.set_repeat(50, 25)
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    pygame.key.set_repeat(50, 25)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    pygame.key.set_repeat(50, 25)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    pygame.key.set_repeat(50, 25)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return True

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player.move_x(self.player.max_speed, TheGame.game_width)
                    self.set_angle = 90
                    self.turn_to_shoot = "left"

                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player.move_x(-self.player.max_speed, TheGame.game_width)
                    self.set_angle = 270
                    self.turn_to_shoot = "right"

                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.move_y(self.player.max_speed, TheGame.game_height)
                    self.set_angle = 0
                    self.turn_to_shoot = "up"

                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.player.move_y(-self.player.max_speed, TheGame.game_height)
                    self.set_angle = 180
                    self.turn_to_shoot = "down"

                if event.key == pygame.K_SPACE:
                    pygame.key.set_repeat(50, 25)
                    self.all_sprites_group.add(self.player.shoot(self.set_angle))
                    self.bullets.add(self.player.shoot(self.set_angle))


if __name__ == "__main__":
    game = TheGame(1000, 600)
    # game.game_intro()
    game.run("easy")

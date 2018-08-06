import pygame
from random import randint
import math
from player import Player
from rooms import Rooms
from zombie import Zombie


class Board:
    """Class responsible for drawing window game"""

    def __init__(self, width, height):
        self.surface = pygame.display.set_mode((width, height), 0, 32)
        pygame.display.set_caption('Zombie in CLab')
        self.bg = pygame.image.load("images/terrain_atlas.png")
        self.intro_bg = pygame.image.load("images/intro.jpg")
        my_font = "font/Exquisite Corpse.ttf"
        self.menu_font = pygame.font.Font(my_font, 45)
        self.options_font = pygame.font.Font(my_font, 65)
        self.title_font = pygame.font.Font(my_font, 90)

    def draw(self, *args):
        """param args: list of object to draw"""
        background = (255, 255, 255)
        self.surface.fill(background)
        self.surface.blit(self.bg, (200, 200), (0, 0, 90, 150))

        for drawable in args:
            drawable.draw_on(self.surface)

    def draw_menu(self, *args):
        background = (0, 0, 0)
        self.surface.fill(background)
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
        background = (0, 0, 0)
        self.surface.fill(background)
        self.intro_bg = pygame.transform.scale(self.intro_bg, (TheGame.game_width, TheGame.game_height))
        self.surface.blit(self.intro_bg, (0, 0), (0, 0, TheGame.game_width, TheGame.game_height))
        self.draw_text(self.surface, "Controls", TheGame.game_width / 2, TheGame.game_height * 0.35, self.options_font)
        self.draw_text(self.surface, "Audio", TheGame.game_width / 2, TheGame.game_height * 0.5, self.options_font)
        self.draw_text(self.surface, "Return", TheGame.game_width / 2, TheGame.game_height * 0.65, self.options_font)
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
        self.set_bullet_angle = 180
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
            self.zombie_person = Zombie(x, y, self.player, self.player.width - 6, self.player.height - 6)
            self.zombie_group.add(self.zombie_person)
            self.other_group.add(self.zombie_person)
            self.all_sprites_group.add(self.zombie_person)

    def game_intro(self):
        intro = True
        i = 0.58
        while intro:
            mark_play_pos = 0.58
            mark_quit_pos = 0.77
            mark_pos_y = TheGame.game_height * i
            mark_pos_x = TheGame.game_width * 0.38
            intro_object = Player(mark_pos_x, mark_pos_y, 26, 26)
            intro_object.animation(0, "images/menu_head.png", (0, 0), (0, 0, mark_pos_x, mark_pos_y))
            self.board.draw_menu(intro_object)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()

                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        if i > mark_play_pos:
                            i -= 0.1

                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if mark_play_pos <= i <= mark_quit_pos:
                            i += 0.1

                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        if i <= mark_play_pos:
                            intro = False
                            game.run()
                        elif i >= mark_quit_pos:
                            pygame.quit()
                        else:
                            game.game_options()

            pygame.display.flip()
            self.fps_clock.tick(100)

    def game_options(self):
        option = True
        i = 0.325
        while option:
            mark_up_opt_pos = 0.325
            mark_down_opt_pos = 0.625
            mark_pos_y = TheGame.game_height * i
            mark_pos_x = TheGame.game_width * 0.32
            intro_object = Player(mark_pos_x, mark_pos_y, 30, 30)
            intro_object.animation("images/menu_head.png", (0, 0), (0, 0, mark_pos_x, mark_pos_y))
            self.board.draw_options(intro_object)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        option = False
                        game.game_intro()
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        if i > mark_up_opt_pos:
                            """without multiplying and dividing by 1000, i in top position has 0.324(9)"""
                            i *= 1000
                            i -= 0.15 * 1000
                            i /= 1000

                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if mark_up_opt_pos <= i < mark_down_opt_pos:
                            i += 0.15

                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        if i == mark_up_opt_pos:
                            """controlls"""
                            pass
                        elif i >= mark_down_opt_pos:
                            game.game_intro()
                        else:
                            """audio"""
                            pass

            pygame.display.flip()
            self.fps_clock.tick(30)

    def run(self):
        """Main loop of game"""
        max_distance = 170
        while True:
            dead = False
            self.handle_events()
            for self.zombie_person in self.zombie_group:
                self.zombie_person.animation(0, "images/zombies.png", (0, 0), (6, 2, 22, 30))
                distance = (self.zombie_person.rect.x - self.player.rect.x) ** 2 + \
                           (self.zombie_person.rect.y - self.player.rect.y) ** 2
                distance = math.sqrt(distance)
                if distance > max_distance:
                    self.zombie_person.zombie_natural_moves()
                elif distance <= max_distance and not pygame.sprite.collide_rect(self.zombie_person, self.player):
                    self.zombie_person.zombie_follows()
                else:
                    self.zombie_person.zombie_attacks()
                for bullet in self.bullets:
                    if pygame.sprite.collide_rect(self.zombie_person, bullet):
                        self.zombie_person.kill()
                        dead = True
                for other_zombie in self.other_group:
                    if other_zombie != self.zombie_person and \
                            pygame.sprite.collide_rect(self.zombie_person, other_zombie):
                        if other_zombie.rect.x > self.zombie_person.rect.x:
                            other_zombie.move_x(-self.zombie_person.max_speed, TheGame.game_width)
                            self.zombie_person.move_x(self.zombie_person.max_speed, TheGame.game_width)
                        else:
                            other_zombie.move_x(self.zombie_person.max_speed, TheGame.game_width)
                            self.zombie_person.move_x(-self.zombie_person.max_speed, TheGame.game_width)
                        if other_zombie.rect.y > self.zombie_person.rect.y:
                            other_zombie.move_y(-self.zombie_person.max_speed, TheGame.game_height)
                            self.zombie_person.move_y(self.zombie_person.max_speed, TheGame.game_height)
                        else:
                            other_zombie.move_y(self.zombie_person.max_speed, TheGame.game_height)
                            self.zombie_person.move_y(-self.zombie_person.max_speed, TheGame.game_height)

            self.board.draw(self.room)
            self.player.animation(0, "images/character.png", (0, 0), (14, 9, 33, 39))
            self.all_sprites_group.draw(self.board.surface)
            self.all_sprites_group.update(self.turn_to_shoot, dead, self.width, self.height)
            self.bullets.update(self.turn_to_shoot, dead, self.width, self.height)
            pygame.display.flip()
            self.fps_clock.tick(50)

    def handle_events(self):
        """handling the system events, like keyboard buttons or quit the game"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                return True

            elif event.type == pygame.KEYUP:
                """turning on continuous moves by pressing buttons"""
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
                    self.set_bullet_angle = 90

                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player.move_x(-self.player.max_speed, TheGame.game_width)
                    self.set_bullet_angle = 270

                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.move_y(self.player.max_speed, TheGame.game_height)
                    self.set_bullet_angle = 0

                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.player.move_y(-self.player.max_speed, TheGame.game_height)
                    self.set_bullet_angle = 180

                if event.key == pygame.K_SPACE:
                    pygame.key.set_repeat(50, 25)
                    self.all_sprites_group.add(self.player.shoot(self.set_bullet_angle))
                    self.bullets.add(self.player.shoot(self.set_bullet_angle))


if __name__ == "__main__":
    game = TheGame(1000, 600)
    game.game_intro()
    # game.run()

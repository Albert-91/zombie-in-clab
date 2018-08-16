from os import path
import pygame
from random import randint
import math
from board import Board
from player import Player
from walls import Wall
from zombie import Zombie


class TheGame:
    # game_width = None
    # game_height = None

    def __init__(self, width, height):
        pygame.init()
        self.set_angle = 180
        self.turn_to_shoot = "down"
        # TheGame.game_width = width
        # TheGame.game_height = height
        self.width = width
        self.height = height
        self.number_of_zombies = 20
        self.board = Board(width, height)
        self.fps_clock = pygame.time.Clock()
        self.player = Player(self, width / 2, height / 2, 26, 26)
        self.zombie_group = pygame.sprite.Group()
        self.all_sprites_group = pygame.sprite.Group()
        self.other_group = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.all_sprites_group.add(self.player)
        self.walls = pygame.sprite.Group()
        self.map_data = []
        self.load_data()
        self.new()
        for i in range(self.number_of_zombies):
            x = randint(self.player.width, self.width - self.player.width)
            y = randint(self.player.height, self.height - self.player.height)
            self.zombie_person = Zombie(x, y, self.player, 23, 28, self.width, self.height)
            self.zombie_group.add(self.zombie_person)
            self.other_group.add(self.zombie_person)
            self.all_sprites_group.add(self.zombie_person)

    def game_intro(self):
        i = 0.56
        while True:
            mark_pos_y = self.height * i
            mark_pos_x = self.width * 0.37
            intro_object = Player(self, mark_pos_x, mark_pos_y, 40, 40)
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
            mark_pos_y = self.height * i
            mark_pos_x = self.width * 0.3
            intro_object = Player(self, mark_pos_x, mark_pos_y, 45, 45)
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
            mark_pos_y = self.height * i
            mark_pos_x = self.width * 0.25
            intro_object = Player(self, mark_pos_x, mark_pos_y, 40, 40)
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

    def game_input(self):
        word = ""
        self.board.draw_input("Please enter your name: ", 300, 400)
        pygame.display.flip()
        done = True
        while done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        word += str(chr(event.key))
                    if event.key == pygame.K_b:
                        word += chr(event.key)
                    if event.key == pygame.K_c:
                        word += chr(event.key)
                    if event.key == pygame.K_d:
                        word += chr(event.key)
                    if event.key == pygame.K_RETURN:
                        done = False
                    # events...
        return text1(word, 700, 30)

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
            self.zombie_behavior(max_distance, zombie_speed, zombie_attack)
            self.board.draw()
            self.player.animation("images/character.png", (0, 0), (14, 11, 20, 39))
            self.all_sprites_group.draw(self.board.surface)
            self.all_sprites_group.update(self.turn_to_shoot, self.width, self.height)
            self.bullets.update(self.turn_to_shoot, self.width, self.height)
            pygame.display.flip()
            self.fps_clock.tick(80)

    def zombie_behavior(self, max_distance, zombie_speed, zombie_attack):
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
                        other_zombie.move(dx=-zombie_speed)
                        self.zombie_person.move(dx=zombie_speed)
                    else:
                        other_zombie.move(dx=zombie_speed)
                        self.zombie_person.move(dx=-zombie_speed)
                    if other_zombie.rect.y > self.zombie_person.rect.y:
                        other_zombie.move(dy=-zombie_speed)
                        self.zombie_person.move(dy=zombie_speed)
                    else:
                        other_zombie.move(dy=zombie_speed)
                        self.zombie_person.move(dy=-zombie_speed)

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
                    self.player.move(dx=-self.player.max_speed)
                    self.set_angle = 90
                    self.turn_to_shoot = "left"

                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player.move(dx=self.player.max_speed)
                    self.set_angle = 270
                    self.turn_to_shoot = "right"

                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.move(dy=-self.player.max_speed)
                    self.set_angle = 0
                    self.turn_to_shoot = "up"

                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.player.move(dy=self.player.max_speed)
                    self.set_angle = 180
                    self.turn_to_shoot = "down"

                if event.key == pygame.K_SPACE:
                    pygame.key.set_repeat(50, 25)
                    self.all_sprites_group.add(self.player.shoot(self.set_angle))
                    self.bullets.add(self.player.shoot(self.set_angle))

    def load_data(self):
        game_folder = path.dirname(__file__)
        with open(path.join(game_folder, 'map.txt'), 'rt') as lines:
            for line in lines:
                self.map_data.append(line)

    def new(self):
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                # if tile == 'P':
                #     self.player = Player(self, col, row)


if __name__ == "__main__":
    game = TheGame(1000, 600)
    game.game_intro()
    # game.run("easy")

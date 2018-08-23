import sys
import pygame
import math
from random import randint
from os import path
from board import Board
from bullet import Bullet
from player import Player
from screen import Camera, Map
from walls import Wall
from zombie import Zombie
from settings import *


class TheGame:

    def __init__(self, width, height):
        pygame.init()
        self.set_angle = 180
        self.width = width
        self.height = height
        self.number_of_zombies = QUANTITY_OF_ZOMBIES
        self.all_sprites_group = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        game_folder = path.dirname(__file__)
        self.map = Map(path.join(game_folder, 'map.txt'))
        self.map_data = self.map.get_map()
        self.new()
        self.camera = Camera(self.map.width, self.map.height)
        self.board = Board(width, height)
        self.fps_clock = pygame.time.Clock()
        self.dt = None
        self.player = Player(self, width / 2, height / 2, PLAYER_WIDTH, PLAYER_HEIGHT, max_speed=PLAYER_SPEED)
        self.zombie_group = pygame.sprite.Group()
        self.other_group = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.all_sprites_group.add(self.player)
        for i in range(self.number_of_zombies):
            x = randint(self.player.width, self.width - self.player.width)
            y = randint(self.player.height, self.height - self.player.height)
            self.zombie_person = Zombie(x, y, ZOMBIE_WIDTH, ZOMBIE_HEIGHT)
            self.zombie_group.add(self.zombie_person)
            self.other_group.add(self.zombie_person)
            self.all_sprites_group.add(self.zombie_person)

    def game_intro(self):
        i = 0.56
        while True:
            mark_pos_y = self.height * i
            mark_pos_x = self.width * INTRO_SPRITE_POS_X
            intro_object = Player(self, mark_pos_x, mark_pos_y, INTRO_SPRITE_WIDTH, INTRO_SPRITE_HEIGHT)
            intro_object.animation("images/menu_head.png", (0, 0), (0, 0, mark_pos_x, mark_pos_y), False)
            self.board.draw_menu(intro_object)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit()
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
                            self.quit()

    def game_options(self):
        i = 0.31
        while True:
            mark_pos_y = self.height * i
            mark_pos_x = self.width * OPTIONS_SPRITE_POS_X
            intro_object = Player(self, mark_pos_x, mark_pos_y, OPTIONS_SPRITE_WIDTH, OPTIONS_SPRITE_HEIGHT)
            intro_object.animation("images/menu_head.png", (0, 0), (0, 0, mark_pos_x, mark_pos_y), False)
            self.board.draw_options(intro_object)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
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
            mark_pos_x = self.width * DIFFICULT_SPRITE_POS_X
            intro_object = Player(self, mark_pos_x, mark_pos_y, DIFFICULT_SPRITE_WIDTH, DIFFICULT_SPRITE_HEIGHT)
            intro_object.animation("images/menu_head.png", (0, 0), (0, 0, mark_pos_x, mark_pos_y), False)
            self.board.draw_choosing_difficulty(intro_object)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
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

                        game.game_input(difficulty)

    def game_input(self, difficult):
        word = ""
        while True:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game.game_choosing_difficulty()
                    if event.unicode.isalpha():
                        word += event.unicode
                    if event.key == pygame.K_BACKSPACE:
                        word = word[:-1]
                    if event.key == pygame.K_RETURN:
                        if len(word) > 0:
                            return self.run(word, difficult)
                self.board.draw_input(word, self.width / 2, self.height / 2)

    def game_over(self):
        while True:
            self.board.draw_game_over()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        return False

    def run(self, name, difficulty):
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
            self.dt = self.fps_clock.tick(FPS) / 1000
            self.handle_events()
            self.zombie_behavior(max_distance, zombie_speed, zombie_attack)
            self.draw()
            self.player.animation("images/character.png", (0, 0), (14, 11, 20, 39))
            self.all_sprites_group.update(self.width, self.height)
            self.bullets.update(self.map.width, self.map.height)
            self.camera.update(self.player)
            pygame.display.flip()

    def zombie_behavior(self, max_distance, zombie_speed, zombie_attack):
        for self.zombie_person in self.zombie_group:
            self.zombie_person.animation("images/zombies.png", (0, 0), (5, 1, 23, 29))
            distance = (self.zombie_person.rect.x - self.player.rect.x) ** 2 + \
                       (self.zombie_person.rect.y - self.player.rect.y) ** 2
            distance = math.sqrt(distance)
            if distance > max_distance and self.zombie_person.state is False:
                self.zombie_person.natural_moves()
            if (distance <= max_distance and not pygame.sprite.collide_rect(self.zombie_person, self.player)) or \
                    self.zombie_person.state is True:
                self.zombie_person.follows_by_victim(zombie_speed, self.player)
            else:
                self.zombie_person.attack(zombie_attack)
            for bullet in self.bullets:
                if pygame.sprite.collide_rect(self.zombie_person, bullet):
                    self.zombie_person.shield -= bullet.attack
                    bullet.kill()
                    self.zombie_person.state = True
                    self.zombie_person.follows_by_victim(zombie_speed, self.player)
                    if self.zombie_person.shield <= 0:
                        self.zombie_person.kill()
            for other_zombie in self.other_group:
                if other_zombie != self.zombie_person and \
                        pygame.sprite.collide_rect(self.zombie_person, other_zombie):
                    if other_zombie.rect.x > self.zombie_person.rect.x:
                        other_zombie.move(dx=zombie_speed)
                        self.zombie_person.move(dx=-zombie_speed)
                    else:
                        other_zombie.move(dx=-zombie_speed)
                        self.zombie_person.move(dx=zombie_speed)
                    if other_zombie.rect.y > self.zombie_person.rect.y:
                        other_zombie.move(dy=zombie_speed)
                        self.zombie_person.move(dy=-zombie_speed)
                    else:
                        other_zombie.move(dy=-zombie_speed)
                        self.zombie_person.move(dy=zombie_speed)

    def handle_events(self):
        self.set_angle = self.player.refresh()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                if event.key == pygame.K_SPACE:
                    attack_list = [0, 1, 1, 2, 2, 2, 2, 2, 3, 3]
                    attack_pos = randint(0, len(attack_list) - 1)
                    attack_value = attack_list[attack_pos]
                    bullet = Bullet(self.player.rect.x + self.player.width / 2,
                                    self.player.rect.y + self.player.height / 2,
                                    self.set_angle, attack_value)
                    self.all_sprites_group.add(bullet)
                    self.bullets.add(bullet)

    def new(self):
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                # if tile == 'P':
                #     self.player = Player(self, col, row)

    def draw(self):
        self.board.surface.fill((255, 255, 255))
        for sprite in self.all_sprites_group:
            self.board.surface.blit(sprite.image, self.camera.apply(sprite))

    def quit(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = TheGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    # game.game_intro()
    game.run('Albert', "easy")

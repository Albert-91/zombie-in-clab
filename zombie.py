from random import randint
import pygame

from functions import collide_with_object
from player import Player, vector
from settings import *


class Zombie(Player, pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, color=(255, 0, 0), max_speed=1, state=False):
        super(Player, self).__init__(width, height, x, y, color)
        pygame.sprite.Sprite.__init__(self)
        self.max_speed = max_speed
        self.image = self.surface
        self.rect = self.image.get_rect(x=x, y=y)
        self.picture = None
        self.shield = 8
        self.state = state

    def natural_moves(self):
        moves_list = [0, 0, 0, 0, 1, 0, 0, 0, -1, 0, 0, 0, 0, 0]
        x = randint(0, len(moves_list) - 1)
        y = randint(0, len(moves_list) - 1)
        self.move(dx=moves_list[x], dy=moves_list[y])

    def follows_by_victim(self, speed, victim):
        if self.rect.x > victim.rect.x:
            x = - speed
        else:
            x = speed
        self.move(dx=x)
        if self.rect.y > victim.rect.y:
            y = - speed
        else:
            y = speed
        self.move(dy=y)

    def attack(self, attack, victim):
        victim.shield -= attack


class Monster(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites_group, game.monsters
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.zombie_img
        self.rect = self.image.get_rect()
        self.position = vector(x, y) * WALL_SIZE
        self.rect.center = self.position
        self.hit_rect = ZOMBIE_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.vel = vector(0, 0)
        self.acc = vector(0, 0)
        self.rotation = 0

    def update(self, width, height):
        self.rotation = (self.game.player.position - self.position).angle_to(vector(1, 0))
        self.image = pygame.transform.rotate(self.game.zombie_img, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.acc = vector(ZOMBIE_SPEED_EASY, 0).rotate(-self.rotation)
        self.acc += self.vel * (-1)
        self.vel += self.acc * self.game.dt
        self.position += self.vel * self.game.dt + (self.acc * self.game.dt ** 2) / 2
        self.hit_rect.centerx = self.position.x
        collide_with_object(self, self.game.walls, 'x')
        collide_with_object(self, self.game.all_sprites_group, 'x')
        self.hit_rect.centery = self.position.y
        collide_with_object(self, self.game.walls, 'y')
        collide_with_object(self, self.game.all_sprites_group, 'y')
        self.rect.center = self.hit_rect.center





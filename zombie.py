from random import randint
import pygame
from player import Player


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

    def attack(self, attack):
        pass

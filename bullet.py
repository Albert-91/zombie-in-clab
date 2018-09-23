from random import uniform

import pygame

from functions import vector
from settings import BULLET_SPEED, GUN_SPREAD


class Bullet(pygame.sprite.Sprite):

    def __init__(self, game, position, direction):
        self.groups = game.all_sprites, game.bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = game.bullet_img
        self.rect = self.image.get_rect()
        self.position = vector(position)
        self.game = game
        self.rect.center = position
        spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = direction.rotate(spread) * BULLET_SPEED
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.position += self.vel * self.game.dt
        self.rect.center = self.position
        if pygame.sprite.spritecollideany(self, self.game.walls):
            self.kill()


import pygame

from functions import vector
from settings import BULLET_SPEED


class Bullet(pygame.sprite.Sprite):

    def __init__(self, game, position, direction):
        self.groups = game.all_sprites_group, game.bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = game.bullet_img
        self.rect = self.image.get_rect()
        self.position = vector(position)
        self.game = game
        self.rect.center = position
        self.vel = direction * BULLET_SPEED
        self.spawn_time = pygame.time.get_ticks()

    def update(self, max_width, max_height):
        self.position += self.vel * self.game.dt
        self.rect.center = self.position



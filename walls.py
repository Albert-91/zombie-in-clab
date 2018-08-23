import pygame
from settings import *


class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites_group, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((WALL_SIZE, WALL_SIZE))
        self.image.fill(WALL_COLOR)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * WALL_SIZE
        self.rect.y = y * WALL_SIZE

import pygame
from bullet import Bullet
from drawable import Drawable
from settings import *


class Player(Drawable, pygame.sprite.Sprite):

    def __init__(self, game, x, y, width=20, height=20, color=(0, 0, 255), max_speed=4, angle=180):
        super(Player, self).__init__(width, height, x, y, color)
        pygame.sprite.Sprite.__init__(self)
        self.max_speed = max_speed
        self.game = game
        self.angle = angle
        self.image = self.surface
        self.width = width
        self.height = height
        self.rect = self.image.get_rect(x=x, y=y)
        self.picture = None
        self.lives = PLAYER_LIVES
        self.shield = PLAYER_SHIELD

    def animation(self, image_file, blit_destination, blit_area, serial=True):
        self.picture = pygame.image.load(image_file)
        if serial:
            self.surface.blit(self.picture, blit_destination, blit_area)
            self.picture = pygame.transform.scale(self.picture, (self.width, self.height))
        else:
            self.picture = pygame.transform.scale(self.picture, (self.width, self.height))
            self.surface.blit(self.picture, blit_destination, (0, 0, self.width, self.height))

    def move(self, dx=0, dy=0):
        # if not self.collide_with_walls(dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.rect.x + dx and wall.y == self.rect.y + dy:
                return True
        return False

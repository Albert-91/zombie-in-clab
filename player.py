import pygame
from drawable import Drawable
from settings import *


class Player(Drawable, pygame.sprite.Sprite):

    def __init__(self, game, x, y, width=20, height=20, color=(0, 0, 255), max_speed=4, angle=180):
        super(Player, self).__init__(width, height, x, y, color)
        pygame.sprite.Sprite.__init__(self)
        self.max_speed = max_speed
        self.game = game
        self.angle = angle
        self.turn_to_shoot = "down"
        self.image = self.surface
        self.width = width
        self.height = height
        self.rect = self.image.get_rect(x=x, y=y)
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
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
        self.rect.x += dx
        self.rect.y += dy

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = - self.max_speed
            self.angle = 90
            self.turn_to_shoot = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = self.max_speed
            self.angle = 270
            self.turn_to_shoot = "right"
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vy = -self.max_speed
            self.angle = 0
            self.turn_to_shoot = "up"
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vy = self.max_speed
            self.angle = 180
            self.turn_to_shoot = "down"
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
        return self.turn_to_shoot

    def collide_with_walls(self, direction):
        hits = pygame.sprite.spritecollide(self, self.game.walls, False)
        if direction == 'x':
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if direction == 'y':
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def refresh(self):
        self.turn_to_shoot = self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        return self.turn_to_shoot

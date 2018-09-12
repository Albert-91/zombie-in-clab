import pygame
from drawable import Drawable
from settings import *
vector = pygame.math.Vector2


class Player(Drawable, pygame.sprite.Sprite):

    def __init__(self, game, x, y, width=20, height=20, color=(0, 0, 255), max_speed=4, angle=180):
        pygame.sprite.Sprite.__init__(self)
        self.max_speed = max_speed
        self.game = game
        self.angle = angle
        self.image = game.player_img
        self.width = width
        self.height = height
        self.rect = self.image.get_rect(x=x, y=y)
        self.vel = vector(0, 0)
        self.position = vector(x, y)
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
        self.vel = vector(0, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel.x = - self.max_speed
            self.angle = 90
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel.x = self.max_speed
            self.angle = 270
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vel.y = -self.max_speed
            self.angle = 0
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vel.y = self.max_speed
            self.angle = 180
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def collide_with_object(self, direction, object_to_collide):
        hits = pygame.sprite.spritecollide(self, object_to_collide, False)
        if direction == 'x':
            if hits:
                if self.vel.x > 0:
                    self.position.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.position.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.position.x
        if direction == 'y':
            if hits:
                if self.vel.y > 0:
                    self.position.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.position.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.position.y

    def refresh(self):
        self.get_keys()
        self.position += self.vel * self.game.dt
        self.rect.x = self.position.x
        self.collide_with_object('x', self.game.walls)
        self.rect.y = self.position.y
        self.collide_with_object('y', self.game.walls)
        return self.angle

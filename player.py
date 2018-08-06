import pygame
from bullet import Bullet
from drawable import Drawable


class Player(Drawable, pygame.sprite.Sprite):

    def __init__(self, x, y, width=20, height=20, color=(0, 0, 255), max_speed=4, angle=180):
        super(Player, self).__init__(width, height, x, y, color)
        pygame.sprite.Sprite.__init__(self)
        self.max_speed = max_speed
        self.angle = angle
        self.image = self.surface
        self.width = width
        self.height = height
        self.rect = self.image.get_rect(x=x, y=y)
        self.picture = None

    def animation(self, angle=0, image_file=0, blit_destination=0, blit_area=0):
        self.picture = pygame.image.load(image_file)
        self.image.blit(self.picture, blit_destination, blit_area)
        self.picture = pygame.transform.scale(self.picture, (self.width, self.height))

    def move_x(self, x, x_limit):
        if x != 0:
            delta_x = x - self.rect.x
            if abs(delta_x) <= x_limit - self.width and delta_x <= 0:
                delta_x = -self.max_speed
                if x > 0:
                    self.rect.x += delta_x
                else:
                    self.rect.x -= delta_x

    def move_y(self, y, y_limit):
        if y != 0:
            delta_y = y - self.rect.y
            if abs(delta_y) <= y_limit - self.height and delta_y <= 0:
                delta_y = -self.max_speed
                if y > 0:
                    self.rect.y += delta_y
                else:
                    self.rect.y -= delta_y

    def shoot(self, angle):
        bullet = Bullet(self.rect.centerx, self.rect.centery, angle)
        return bullet

import pygame
from bullet import Bullet
from drawable import Drawable


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
        self.lives = 3
        self.shield = 100

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

    def move_x(self, dx, x_limit):
        if dx != 0:
            delta_x = dx - self.rect.x
            if abs(delta_x) <= x_limit-self.width / 2 and delta_x <= 0:
                delta_x = - abs(dx)
                if dx > 0:
                    self.rect.x += delta_x
                else:
                    self.rect.x -= delta_x

    def move_y(self, dy, y_limit):
        if dy != 0:
            delta_y = dy - self.rect.y
            if abs(delta_y) <= y_limit - self.height and delta_y <= 0:
                delta_y = - abs(dy)
                if dy > 0:
                    self.rect.y += delta_y
                else:
                    self.rect.y -= delta_y

    def shoot(self, angle):
        bullet = Bullet(self.rect.centerx, self.rect.centery, angle)
        return bullet

    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.rect.x + dx and wall.y == self.rect.y + dy:
                return True
        return False

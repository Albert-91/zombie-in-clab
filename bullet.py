import pygame


class Bullet(pygame.sprite.Sprite):
    bullet_img = pygame.image.load("images/bullet.png")

    def __init__(self, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.width = 5
        self.height = 10
        self.angle = angle
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.image = Bullet.bullet_img
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect.centerx = x
        self.rect.centery = y
        self.max_speed = 5

    def update(self, direction, dead, max_width, max_height):
        if self.angle == 180:
            self.rect.y += self.max_speed
        elif self.angle == 0:
            self.rect.y -= self.max_speed
        elif self.angle == 270:
            self.rect.x += self.max_speed
        elif self.angle == 90:
            self.rect.x -= self.max_speed
        # kill if it moves off the top of the screen
        if self.rect.top < 0 or \
                        self.rect.bottom > max_height or \
                        self.rect.right > max_width or \
                        self.rect.left < 0:
            self.kill()
        if dead:
            self.kill()

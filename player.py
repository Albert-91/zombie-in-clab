from bullet import Bullet
from drawable import Drawable
from functions import collide_with_object
from settings import *
from smoke import Smoke


class Player(Drawable, pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect(x=x, y=y)
        self.rect.center = (x, y)
        self.surface = pygame.Surface([PLAYER_WIDTH, PLAYER_HEIGHT], pygame.SRCALPHA, 32)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vector(0, 0)
        self.position = vector(x, y)
        self.picture = None
        self.lives = PLAYER_LIVES
        self.shield = PLAYER_SHIELD
        self.rotation = 0
        self.rotation_speed = 0
        self.last_shot = 0

    def move(self, dx=0, dy=0):
        self.rect.x += dx
        self.rect.y += dy

    def get_keys(self):
        self.vel = vector(0, 0)
        self.rotation_speed = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rotation_speed = PLAYER_ROTATION_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rotation_speed = - PLAYER_ROTATION_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vel = vector(PLAYER_SPEED, 0).rotate(-self.rotation)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vel = vector(-PLAYER_SPEED/2, 0).rotate(-self.rotation)
        if keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                direction = vector(1, 0).rotate(-self.rotation)
                position = self.position + BARREL_OFFSET.rotate(-self.rotation)
                Bullet(self.game, position, direction)
                self.vel = vector(-KICKBACK, 0).rotate(-self.rotation)
                Smoke(self.game, position)

    def update(self):
        self.get_keys()
        self.rotation = (self.rotation + self.rotation_speed * self.game.dt) % 360
        self.image = pygame.transform.rotate(self.game.player_img, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.position += self.vel * self.game.dt
        self.hit_rect.centerx = self.position.x
        collide_with_object(self, self.game.walls, 'x')
        self.hit_rect.centery = self.position.y
        collide_with_object(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def add_shield(self, amount):
        self.shield += amount
        if self.shield > PLAYER_SHIELD:
            self.shield = PLAYER_SHIELD

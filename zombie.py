from random import randint, choice
from functions import collide_with_object
from settings import *


class Zombie(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.zombies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.zombie_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.position = vector(x, y)
        self.rect.center = self.position
        self.hit_rect = ZOMBIE_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.vel = vector(0, 0)
        self.acc = vector(0, 0)
        self.rotation = 0
        self.shield = ZOMBIE_SHIELD
        self.shield_bar = None
        self.speed = choice(ZOMBIE_SPEEDS_EASY)

    def natural_moves(self):
        moves_list = [0, 0, 0, 0, 1, 0, 0, 0, -1, 0, 0, 0, 0, 0]
        x = randint(0, len(moves_list) - 1)
        y = randint(0, len(moves_list) - 1)
        self.move(dx=moves_list[x], dy=moves_list[y])

    def update(self):
        self.rotation = (self.game.player.position - self.position).angle_to(vector(1, 0))
        self.image = pygame.transform.rotate(self.game.zombie_img, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.acc = vector(1, 0).rotate(-self.rotation)
        self.avoid_other_zombies()
        self.acc.scale_to_length(self.speed)
        self.acc += self.vel * (-1)
        self.vel += self.acc * self.game.dt
        self.position += self.vel * self.game.dt + (self.acc * self.game.dt ** 2) / 2
        self.hit_rect.centerx = self.position.x
        collide_with_object(self, self.game.walls, 'x')
        self.hit_rect.centery = self.position.y
        collide_with_object(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        if self.shield <= 0:
            self.kill()

    def draw_shield(self):
        if self.shield > 60:
            color = GREEN
        elif self.shield > 30:
            color = YELLOW
        else:
            color = RED
        width = int(self.rect.width * self.shield / ZOMBIE_SHIELD)
        self.shield_bar = pygame.Rect(0, 0, width, 7)
        if self.shield < ZOMBIE_SHIELD:
            pygame.draw.rect(self.image, color, self.shield_bar)

    def avoid_other_zombies(self):
        for zombie in self.game.zombies:
            if zombie != self:
                distance = self.position - zombie.position
                if 0 < distance.length() < AVOID_RADIUS:
                    self.acc += distance.normalize()


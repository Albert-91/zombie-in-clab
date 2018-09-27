from random import randint, choice, random
from functions import collide_with_object
from settings import *
from smoke import Smoke


class Zombie(pg.sprite.Sprite):

    def __init__(self, game, x, y):
        self._layer = ZOMBIE_LAYER
        self.groups = game.all_sprites, game.zombies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.zombie_img.copy()
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
        self.target = game.player

    def natural_moves(self):
        moves_list = [0, 0, 0, 0, 1, 0, 0, 0, -1, 0, 0, 0, 0, 0]
        x = randint(0, len(moves_list) - 1)
        y = randint(0, len(moves_list) - 1)
        self.move(dx=moves_list[x], dy=moves_list[y])

    def update(self):
        target_distance = self.target.position - self.position
        if target_distance.length_squared() < DETECT_RADIUS ** 2:
            if random() < 0.002:
                choice(self.game.zombie_moan_sound).play()
            self.rotation = (self.game.player.position - self.position).angle_to(vector(1, 0))
            self.image = pg.transform.rotate(self.game.zombie_img, self.rotation)
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
            size = randint(70, 120)
            Smoke(self.game, self.rect.center, self.game.zombie_death_smoke, size)
            self.kill()

    def draw_shield(self):
        if self.shield > 60:
            color = GREEN
        elif self.shield > 30:
            color = YELLOW
        else:
            color = RED
        width = int(self.rect.width * self.shield / ZOMBIE_SHIELD)
        self.shield_bar = pg.Rect(0, 0, width, 7)
        if self.shield < ZOMBIE_SHIELD:
            pg.draw.rect(self.image, color, self.shield_bar)

    def avoid_other_zombies(self):
        for zombie in self.game.zombies:
            if zombie != self:
                distance = self.position - zombie.position
                if 0 < distance.length() < AVOID_RADIUS:
                    self.acc += distance.normalize()


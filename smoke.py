from random import randint, choice
from settings import *


class Smoke(pg.sprite.Sprite):

    def __init__(self, game, position):
        self._layer = SMOKE_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = randint(20, 50)
        self.image = pg.transform.scale(choice(game.gun_smoke), (size, size))
        self.rect = self.image.get_rect()
        self.position = position
        self.rect.center = position
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > SMOKE_DURATION:
            self.kill()

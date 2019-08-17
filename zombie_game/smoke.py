from random import choice

from zombie_game.settings import *


class Smoke(pg.sprite.Sprite):

    def __init__(self, game, position, smoke_list, size):
        self._layer = SMOKE_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.scale(choice(smoke_list), (size, size))
        self.rect = self.image.get_rect()
        self.position = position
        self.rect.center = position
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > SMOKE_DURATION:
            self.kill()

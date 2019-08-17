from random import uniform

from zombie_game.settings import *


class Bullet(pg.sprite.Sprite):

    def __init__(self, game, position, direction):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = game.bullet_images[WEAPONS[game.player.weapon]['bullet_size']]
        self.rect = self.image.get_rect()
        self.position = vector(position)
        self.game = game
        self.rect.center = position
        self.vel = direction * WEAPONS[game.player.weapon]['bullet_speed'] * uniform(0.9, 1.1)
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.position += self.vel * self.game.dt
        self.rect.center = self.position
        self.image = pg.transform.rotate(self.game.bullet_images['large'], self.game.player.rotation - 90)
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        try:
            if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.game.player.weapon]['bullet_lifetime']:
                self.kill()
        except KeyError:
            if pg.time.get_ticks() - self.spawn_time > 1000:
                self.kill()

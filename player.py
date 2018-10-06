from os import path
from random import randint, choice, uniform
from bullet import Bullet
from functions import collide_with_object
from settings import *
from smoke import Smoke


class Player(pg.sprite.Sprite):

    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect(x=x, y=y)
        self.rect.center = (x, y)
        self.surface = pg.Surface([PLAYER_WIDTH, PLAYER_HEIGHT], pg.SRCALPHA, 32)
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
        self.weapon = None
        self.all_weapons = []
        self.damaged = False
        self.damage_alpha = None
        self.has_key = False
        self.has_id = False
        self.speed = PLAYER_SPEED
        self.bonus = None
        self.ammo = AMMO
        self.money = False
        self.total_bullets = 0
        self.accurate_shot = 1
        self.total_accuracy = 0

    def get_keys(self):
        self.vel = vector(0, 0)
        self.rotation_speed = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rotation_speed = PLAYER_ROTATION_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rotation_speed = - PLAYER_ROTATION_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vector(self.speed, 0).rotate(-self.rotation)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vector(-self.speed, 0).rotate(-self.rotation)
        if keys[pg.K_SPACE]:
            if self.weapon is not None:
                if self.ammo[self.weapon] > 0:
                    self.shoot()
                else:
                    self.game.sound_effects['out_of_ammo'].play()
        if keys[pg.K_1]:
            self.weapon = None
        if keys[pg.K_2]:
            if 'pistol' in self.all_weapons and self.weapon is not 'pistol':
                self.select_weapon('pistol')
        if keys[pg.K_3]:
            if 'shotgun' in self.all_weapons and self.weapon is not 'shotgun':
                self.select_weapon('shotgun')
        if keys[pg.K_4]:
            if 'uzi' in self.all_weapons and self.weapon is not 'uzi':
                self.select_weapon('uzi')
        if keys[pg.K_5]:
            if 'rifle' in self.all_weapons and self.weapon is not 'rifle':
                self.select_weapon('rifle')

    def select_weapon(self, weapon):
        self.game.sound_effects[weapon].play()
        self.weapon = weapon

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > WEAPONS[self.weapon]['rate']:
            self.last_shot = now
            direction = vector(1, 0).rotate(-self.rotation)
            position = self.position + BARREL_OFFSET.rotate(-self.rotation)
            self.vel = vector(-WEAPONS[self.weapon]['kickback'], 0).rotate(-self.rotation)
            self.ammo[self.weapon] -= WEAPONS[self.weapon]['bullet_count']
            if self.ammo[self.weapon] < 0:
                self.ammo[self.weapon] = 0
            for i in range(WEAPONS[self.weapon]['bullet_count']):
                spread = uniform(-WEAPONS[self.weapon]['spread'], WEAPONS[self.weapon]['spread'])
                Bullet(self.game, position, direction.rotate(spread))
                self.total_bullets += 1
                self.total_accuracy = round((self.accurate_shot / self.total_bullets) * 100, 2)
                print(self.total_accuracy)
                sound = choice(self.game.weapon_sounds[self.weapon])
                if sound.get_num_channels() > 2:
                    sound.stop()
                sound.play()
            size = randint(20, 50)
            Smoke(self.game, position, self.game.gun_smoke, size)

    def update(self):
        self.get_keys()
        if self.weapon is None:
            self.game.player_img = pg.image.load(path.join(self.game.img_folder,
                                                           self.game.character_type + PLAYER_IMAGE_NAKED))
        elif self.weapon == 'shotgun' or self.weapon == 'rifle':
            self.game.player_img = pg.image.load(path.join(self.game.img_folder,
                                                           self.game.character_type + PLAYER_IMAGE_SHOTGUN))
        elif self.weapon == 'pistol':
            self.game.player_img = pg.image.load(path.join(self.game.img_folder,
                                                           self.game.character_type + PLAYER_IMAGE_PISTOL))
        elif self.weapon == 'uzi':
            self.game.player_img = pg.image.load(path.join(self.game.img_folder,
                                                           self.game.character_type + PLAYER_IMAGE_UZI))
        self.rotation = (self.rotation + self.rotation_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rotation)
        if self.damaged:
            try:
                self.image.fill((255, 0, 0, next(self.damage_alpha)), special_flags=pg.BLEND_RGB_MULT)
            except StopIteration:
                self.damaged = False
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

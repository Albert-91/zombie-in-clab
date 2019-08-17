import sys
from itertools import chain

from zombie_game.settings import *

vector = pg.math.Vector2


def get_hit(character):
    alphas = [i for i in range(0, 255, 25)]
    character.damaged = True
    character.damage_alpha = chain(alphas * 2)


def quit_game():
    pg.quit()
    sys.exit()


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two)


def collide_with_object(sprite, group, direction):
    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if direction == 'x' and hits:
        if hits[0].rect.centerx > sprite.hit_rect.centerx:
            sprite.position.x = hits[0].rect.left - sprite.hit_rect.width / 2
        if hits[0].rect.centerx < sprite.hit_rect.centerx:
            sprite.position.x = hits[0].rect.right + sprite.hit_rect.width / 2
        sprite.vel.x = 0
        sprite.hit_rect.centerx = sprite.position.x
    if direction == 'y' and hits:
        if hits[0].rect.centery > sprite.hit_rect.centery:
            sprite.position.y = hits[0].rect.top - sprite.hit_rect.height / 2
        if hits[0].rect.centery < sprite.hit_rect.centery:
            sprite.position.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
        sprite.vel.y = 0
        sprite.hit_rect.centery = sprite.position.y


def draw_player_health(surface, x, y, picture):
    if picture < 0:
        picture = 0
    fill = picture * 100
    outline_rect = pg.Rect(x, y, 100, 20)
    fill_rect = pg.Rect(x, y, fill, 20)
    if picture > 0.6:
        color = (0, 255, 0)
    elif picture > 0.3:
        color = (255, 255, 0)
    else:
        color = (255, 0, 0)
    pg.draw.rect(surface, color, fill_rect)
    pg.draw.rect(surface, (255, 255, 255), outline_rect, 2)

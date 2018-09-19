import pygame


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two)


def collide_with_object(sprite, group, direction):
    hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if direction == 'x':
        if hits:
            if sprite.vel.x > 0:
                sprite.position.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if sprite.vel.x < 0:
                sprite.position.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.position.x
    if direction == 'y':
        if hits:
            if sprite.vel.y > 0:
                sprite.position.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if sprite.vel.y < 0:
                sprite.position.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.position.y
